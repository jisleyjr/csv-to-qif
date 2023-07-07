# CSV to QIF

## Overview

The point of this project is to take csv files from Wex HSA Investment and create a QIF file that is importable into Quicken.

# WEX

There could be several different source CSVs that could be converted but going to start with WEX, here is the input.

```
Date,FundName,TransName,Units,Amount,Price,Source  
04/06/23,AMERICAN GROWTH FND OF AMER R6,Investment Purchase,5.327000,289.670000,54.380000,
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
