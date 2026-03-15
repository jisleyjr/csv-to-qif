# CSV to QIF

## Overview

The point of this project is to take csv files from Wex HSA Investment and create a QIF file that is importable into Quicken.

# WEX

There could be several different source CSVs that could be converted but going to start with WEX, here is the input.

```
Date,FundName,TransName,Units,Amount,Price,Source  
04/06/23,AMERICAN GROWTH FND OF AMER R6,Investment Purchase,5.327000,289.670000,54.380000,
```

# Capital Group

Here is a sample of Captial Group. I had to download to Excel format and then save as a csv.

```
Trade date,Account number,Fund name,Activity type,Activity detail,Transaction amount,Sale charge %¹,Sales charge amount,Share price,Shares this transaction,Share balance
06/30/2023,81114613,American High-Income Trust - A (21),Dividends - reinvested,INCOME DIVIDEND,$39.48,,,$9.15,4.3150,871.584
```

# Coinbase Credit Card

I haven't found a way to import the transactions for a Coinbase CC, so I created a script to read through the PDF, convert the description and create a QIF,

Sample transaction text

```
Transactions
Date Description Amount
Feb 11, 2026 PY *POUNDS 000003683 344 2ST AVE N Anytown $23.47
Anytown 11111 564 123
Feb 12, 2026 CASH WISE #3045 00000000 222 1 AVE EAST $37.70
Anytown 11111 564 123
Feb 13, 2026 SP BRUNT WORKWEAR 54 CONCORD STREET $57.08
Anytown 11111 564 123
Feb 16, 2026 DRUNKEN NOODLE SLURP RAM 414 Main St NW $16.88
Anytown 11111 564 123
```

A payee_mappings.json file needs to placed in the input folder along with all the mappings from the Transaction sample above to what you want in Quicken. If not found it'll default to 'Miscellanous' for the Category.

## Quicken QIF

Here is an example of the above transaction converted.

```
D4/ 6'23
NBuy
YAmerican Funds Growth Fund Of Amer R6
I54.380
Q5.327 
U289.67
T289.67
^
```

# How to run
## convert-wex.py
```
python3 convert-wex.py filename-in-inputs-folder.csv
```
This will create a QIF file in the output folder with WEX suffix.

## convert-cbcc-statement.py
```
python convert-cbcc-statement.py input/statement.pdf
```
This will create a QIF file in the output folder. pdfplumber will need to be installed.

### Running on Ubuntu 20
Using venv to specify 3.12 version.
```
python -m venv myenv
source myenv/bin/activate
```