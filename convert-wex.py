import csv
import sys
import time

# Load the mappings out of the filename
def load_mappings(inputsource):
  mappings = {}

  with open('input/mappings.csv', newline='\n') as mappingfile:
    reader = csv.DictReader(mappingfile)

    for row in reader:
      if (row['InputSource'] == inputsource):
        mappings[row['Source']] = row['Destination']

  # return mappings
  return mappings

# Format the date into the needed format
def format_date(date):
  month = date[0:2]
  monthInt = int(month)
  day = date[3:5]
  dayInt = int(day)
  year = date[6:8]
  formattedDate = 'D' + str(monthInt) + '/'

  # Pad the day with a empty space if less then 10
  if (dayInt < 10):
    formattedDate += ' '

  formattedDate += str(dayInt) + '\'' + year

  return formattedDate

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

  with open('output/' + str(int(time.time())) + '.qif', 'w') as outputfile:
    # Write the header
    outputfile.write('!Type:Invst\n')

    # Date,FundName,TransName,Units,Amount,Price,Source
    for row in reader:
      # FundName needs to be in the mappings
      if (row['FundName'] in mappings):
        # Load up the properties
        date = format_date(row['Date'])
        fundname = mappings[row['FundName']]
        units = row['Units']
        amount = row['Amount']
        price = row['Price']

        if (row['TransName'] == 'Investment Purchase'):
          action = 'Buy'
          # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^'
          outputfile.write(transaction + '\n')

        elif (row['TransName'] == 'Custodial Management Fee'):
          # TODO : Handle Custodial Management Fee
          print('This not handled yet: ' + row['TransName'])

        elif (row['TransName'] == 'Custodial Management Fee - Cash disbursement'):
          # TODO : Handle Custodial Management Fee - Cash disbursement
          print('This not handled yet: ' + row['TransName'])

        elif (row['TransName'] == 'Reinvested Dividend'):
          action = 'ReinvDiv'
           # Putting it all together
          transaction = date + '\nN' + action + '\nY' + fundname + '\nI' + price + '\nQ' + units + '\nU' + amount + '\nT' + amount + '\n^'
          outputfile.write(transaction + '\n')
        elif (row['TransName'] == 'Dividend Received - Cash receipt'):
          # Not going to handle Dividend Received - Cash receipt
          print('Not going to handle Dividend Received - Cash receipt')
        else:
          print('Unhandled TransName: ' + row['TransName'])

      elif (row['FundName'] != 'Cash'):
        print('FundName not found in mappings: ' + row['FundName'])

      