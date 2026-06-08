import csv
import sys
import time
from common import *
from pathlib import Path

# --------------------------------------------
# Main program starts here

# Check if the filename was provided
if (len(sys.argv) == 1):
  print("Filename was not provided!")
  exit()

print('Get the filename to import')
filename = sys.argv[1]

# Load the payee mappings
payee_mappings = load_payee_mappings()

payees_not_found_list = []
payees_found_list = []

with open('input/' + filename, newline='\n', encoding='utf-8-sig') as csvfile:
  reader = csv.reader(csvfile, delimiter='\t')
  
  # Iterate through the rows in the CSV file converting the payee, 
  # if any are not found record a log of them, along with a boolean to check later
  for row in reader:
    date = row[0].strip()
    amount = row[1].strip('$')
    payee = row[2][:25].strip() # Take only the first 25 characters, the remainder is city and state
    
    if payee == "ONLINE PAYMENT":
      continue
    
    entry = payee_mappings.get(payee, {})
    if entry:
      payee = entry.get("name", payee)
      category = entry.get("category", "Miscellaneous")
      payees_found_list.append({"date": date, "amount": amount, "payee": payee, "category": category})
    else:
      payees_not_found_list.append(payee)
      category = "Miscellaneous"
    
    print(f"{date},{amount},{payee},{category}")

if payees_not_found_list:
  print("\nPayees not found:")
  for payee in payees_not_found_list:
    print(f"  {payee}")
elif len(payees_found_list) > 0:
  output_path = Path("output") / f"{str(int(time.time()))}-BBCC.QIF"
  
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
  
  # Now create the output QIF file
  out = Path(output_path)
  with out.open("w", encoding="utf-8") as f:
    f.write("!Type:CCard\n")

    for tx in payees_found_list:
      f.write(f"{format_date_yyyy(tx['date'])}\n")
      f.write(f"U-{tx['amount']}\n")
      f.write(f"T-{tx['amount']}\n")
      f.write("C*\n")
      f.write(f"P{tx['payee']}\n")
      f.write(f"L{tx['category']}\n")
      f.write("^\n")
    
print('Done')
      