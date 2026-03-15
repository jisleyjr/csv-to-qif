import csv
import json
import sys
import time
from datetime import datetime

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

# Load the json mappings for payees
def load_payee_mappings() -> dict:
  with open('input/payee-mappings.json', 'r') as f:
    return json.load(f)

# Format the date into the needed format
def format_date_yy(date):
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

def format_date_yyyy(date):
  month = date[0:2]
  monthInt = int(month)
  day = date[3:5]
  dayInt = int(day)
  year = date[8:10]
  formattedDate = 'D' + str(monthInt) + '/'

  # Pad the day with a empty space if less then 10
  if (dayInt < 10):
    formattedDate += ' '

  formattedDate += str(dayInt) + '\'' + year

  return formattedDate

def convert_coinbase_date(old: str) -> str:
  """
  Convert 'Feb 11, 2026' → '2/11'26'
  """
  # Parse the original format
  dt = datetime.strptime(old, "%b %d, %Y")
  # Build the new format: month/day'YY
  return f"{dt.month}/{dt.day:02d}'{dt.year % 100:02d}"
