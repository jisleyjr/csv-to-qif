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