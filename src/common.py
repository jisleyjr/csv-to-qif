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
  # Build the new format: month/day'YY with space before single-digit days
  day_str = f" {dt.day}" if dt.day < 10 else str(dt.day)
  return f"{dt.month}/{day_str}'{dt.year % 100:02d}"

def strip_currency(value: str) -> str:
  """
  Convert currency string to plain number.
  Examples: "$187.46" → "187.46", "($30.94)" → "-30.94"
  """
  # Remove spaces
  value = value.strip()
  # Handle parentheses for negative values
  if value.startswith('(') and value.endswith(')'):
    value = '-' + value[1:-1]
  # Remove dollar sign and commas
  value = value.replace('$', '').replace(',', '')
  return value

def format_bell_date(date: str) -> str:
  """
  Convert BELL date format M/D/YYYY or MM/DD/YYYY to QIF format DM/DD'YY
  Example: "8/30/2024" → "D8/30'24"
  """
  parts = date.split('/')
  month = int(parts[0])
  day = int(parts[1])
  year = parts[2][-2:]  # Get last 2 digits of year
  
  formattedDate = 'D' + str(month) + '/'
  # Pad the day with a space if less than 10
  if day < 10:
    formattedDate += ' '
  formattedDate += str(day) + '\'' + year
  
  return formattedDate
