import csv
import sys
import time
from common import *

# --------------------------------------------
# Main program starts here

# Check if the filename was provided
if (len(sys.argv) == 1):
  print("Filename was not provided!")
  exit()

print('Get the filename to import')
filename = sys.argv[1]

# Load the mappings for WEX
mappings = load_mappings('CAPITALGROUP')

# encoding='utf-8-sig' added to help with '\ufeffTrade date' for first column
with open(filename, newline='\n', encoding='utf-8-sig') as csvfile:
  reader = csv.DictReader(csvfile)
  
  with open('output/' + str(int(time.time())) + '-CAPITALGROUP.QIF', 'w') as outputfile:
    # Write the header
    outputfile.write('!Type:Invst\n')

    # Trade date,Account number,Fund name,Activity type,Activity detail,Transaction amount
    # Sale charge %¹,Sales charge amount,Share price,Shares this transaction,Share balance
    for row in reader:
      # FundName needs to be in the mappings
      if (row['Fund name'] in mappings):
        # Load up the properties
        date = format_date_yyyy(row['Trade date'])
        fundname = mappings[row['Fund name']]
        units = row['Shares this transaction'] # Number of shares
        amount = row['Transaction amount'] # Total Amount
        price = row['Share price']
        transactionType = row['Activity type']
        
        if (transactionType == 'Dividends - reinvested'):
          action = 'ReinvDiv'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)
        
        elif (transactionType == 'Withdrawals'):
          action = 'Sell'
          # Putting it all together
          # Units and amount have a - as a prefix
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units.replace("-", "") + '\nO' + amount.replace("-", "") + '\n^\n'
          outputfile.write(transaction)
        
        elif (transactionType == 'Capital gains - reinvested'):
          action = 'ReinvDiv'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)
          
        else:
          print('Unhandled transaction type: ' + transactionType)
        
      elif (row['FundName'] != 'Cash'):
        print('FundName not found in mappings: ' + row['FundName'])
  
  