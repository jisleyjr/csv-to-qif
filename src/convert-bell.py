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

# Load the mappings for BELL
mappings = load_mappings('BELL')

with open('input/' + filename, newline='\n') as csvfile:
  reader = csv.DictReader(csvfile)

  with open('output/' + str(int(time.time())) + '-BELL.QIF', 'w') as outputfile:
    # Write the header
    outputfile.write('!Type:Invst\n')

    # BELL columns: Fund Type, Fund Name, Transaction Date, Type, Dollars, Price, Shares Purchased/Sold, Total Shares, Market Price, Market Value
    for row in reader:
      # Normalize column keys and values by stripping whitespace
      row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
      
      # Fund Name needs to be in the mappings
      if (row['Fund Name'] in mappings):
        # Load up the properties
        date = format_bell_date(row['Transaction Date'])
        fundname = mappings[row['Fund Name']]
        units = row['Shares Purchased/Sold']
        amount = strip_currency(row['Dollars'])
        price = strip_currency(row['Price'])

        if (row['Type'] == 'Contributions'):
          action = 'Buy'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)
          
        elif (row['Type'] == 'Earnings'):
          action = 'ReinvDiv'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^\n'
          outputfile.write(transaction)

        elif (row['Type'] == 'Third Party Fee'):
          action = 'Sell'
          # Putting it all together
          # For fees, amount is negative in the CSV
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units.replace("-", "") + '\nO' + amount.replace("-", "") + '\n^\n'
          outputfile.write(transaction)

        else:
          print('Unhandled Type: ' + row['Type'])

      elif (row['Fund Name'] != 'Cash'):
        print('Fund Name not found in mappings: ' + row['Fund Name'])

print('Done')
      