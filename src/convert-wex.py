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
mappings = load_mappings('WEX')

with open('input/' + filename, newline='\n') as csvfile:
  reader = csv.DictReader(csvfile)

  with open('output/' + str(int(time.time())) + '-WEX.QIF', 'w') as outputfile:
    # Write the header
    outputfile.write('!Type:Invst\n')

    # Date,FundName,TransName,Units,Amount,Price,Source
    for row in reader:
      # FundName needs to be in the mappings
      if (row['FundName'] in mappings):
        # Load up the properties
        date = format_date_yy(row['Date'])
        fundname = mappings[row['FundName']]
        units = row['Units']
        amount = row['Amount']
        price = row['Price']

        if (row['TransName'] == 'Investment Purchase'):
          action = 'Buy'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)
          
        elif (row['TransName'] == 'Investment Withdrawal'):
          action = 'Sell'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)

        elif (row['TransName'] == 'Custodial Management Fee'):
          action = 'Sell'
          # Putting it all together
          # Units and amount have a - as a prefix
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units.replace("-", "") + '\nO' + amount.replace("-", "") + '\n^\n'
          outputfile.write(transaction)

        elif (row['TransName'] == 'Custodial Management Fee - Cash disbursement'):
          # TODO : Handle Custodial Management Fee - Cash disbursement
          print('This not handled yet: ' + row['TransName'])

        elif (row['TransName'] == 'Reinvested Dividend'):
          action = 'ReinvDiv'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)

        elif (row['TransName'] == 'Dividend Received - Cash receipt'):
          # Not going to handle Dividend Received - Cash receipt
          print('Not going to handle Dividend Received - Cash receipt')
        else:
          print('Unhandled TransName: ' + row['TransName'])

      elif (row['FundName'] != 'Cash'):
        print('FundName not found in mappings: ' + row['FundName'])

print('Done')
      