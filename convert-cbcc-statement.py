import argparse
from datetime import datetime
import sys
import pdfplumber
import re
from pathlib import Path
from typing import List, Dict
from common import *

DATE_RE = re.compile(r"^[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}")  # e.g. Feb 11, 2026
AMOUNT_RE = re.compile(r"^\$?\d+(?:\.\d{2})?$")  # e.g. $23.47

def read_transaction_section(lines: List[str]) -> List[str]:
    """Return the lines between 'Transactions' and 'Total new charges...'."""
    start = end = None
    for i, line in enumerate(lines):
        if start is None and "Transactions" in line:
            start = i + 1  # start after the header line
        if start is not None and "Total new charges in this period" in line:
            end = i
            break
    if start is None or end is None:
        raise ValueError("Could not locate the transaction section.")
    return lines[start:end]

def parse_transactions(lines: List[str]) -> List[Dict[str, str]]:
    txs = []
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip page‑break or unrelated text
        if not DATE_RE.match(line) and not AMOUNT_RE.search(line):
            continue

        # New transaction starts with a date
        if DATE_RE.match(line):
            if current:
                txs.append(current)
            # Split into tokens
            tokens = line.split()
            # Date is first three tokens
            date = " ".join(tokens[:3])
            # Find the token that starts with $ (amount)
            amount_idx = next((i for i, t in enumerate(tokens) if t.startswith("$")), None)
            if amount_idx is None:
                # If amount is missing on this line, we'll capture it later
                amount = None
                description_tokens = tokens[3:]
            else:
                amount = tokens[amount_idx]
                description_tokens = tokens[3:amount_idx]
            description = " ".join(description_tokens)
            current = {"date": convert_coinbase_date(date), "description": description, "amount": amount.strip("$")}
            continue

        # If the line doesn't start with a date, it's either an address line or a stray line
        if current:
            # Append to description if it doesn't contain a $ (i.e., not an amount line)
            if not AMOUNT_RE.search(line):
                current["description"] += " " + line
            else:
                # Line contains an amount but no date – treat it as the amount for the current tx
                current["amount"] = line

    # Add the last transaction
    if current:
        txs.append(current)

    return txs

def extract_text(pdf_path: str):
    # Grab all the text from the PDF and return it
    txs = ""
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Opened PDF: {pdf_path}, number of pages: {len(pdf.pages)}")
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                print("No text found on page, skipping.")
                continue

            # Grab all the text
            txs += text + "\n"
            
    return txs

def main():
    parser = argparse.ArgumentParser(
        description="Parse Coinbase statement file."
    )
    parser.add_argument(
        "input_path",
        help="Path to a file or directory containing Coinbase transactions."
    )
    args = parser.parse_args()

    if not args.input_path.lower().endswith(".pdf"):
        print("Error: Only PDF files are accepted.", file=sys.stderr)
        sys.exit(1)

    # Now lets extract transactions from the PDF
    raw_lines = extract_text(args.input_path)
    section = read_transaction_section(raw_lines.splitlines())
    transactions = parse_transactions(section)

    print(f"Extracted transactions: {len(transactions)}")

    # Now create the output CSV file into the output directory with a timestamped name
    output_path = Path("output") / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-CBCC.QIF"
    
    """
    Write transactions in the “CCard” format.

    Each block looks like:
        D<month>/<day>'<YY
        U-<amount>
        T-<amount>
        C*
        P<description>
        L<category>
        ^
    """
    out = Path(output_path)
    with out.open("w", encoding="utf-8") as f:
        f.write("!Type:CCard\n")

        for tx in transactions:
            # Date: month/day'YY
            date_str = tx["date"]          # e.g. "2/11'26"
            amount = tx["amount"]          # e.g. "23.47"
            description = tx["description"].replace("\n", " ").strip()
            category = tx.get("category", "Unknown")

            f.write(f"{date_str}\n")
            f.write(f"U-{amount}\n")
            f.write(f"T-{amount}\n")
            f.write("C*\n")
            f.write(f"P{description}\n")
            f.write(f"L{category}\n")
            f.write("^\n")

    print(f"Written output to: {output_path}")

if __name__ == "__main__":
    main()