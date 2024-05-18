import os
from pyairtable import Api

API_KEY = os.environ.get('AIRTABLE_API_KEY')
BASE_KEY = os.environ.get('VERIC_BASE_KEY')

if not (API_KEY and BASE_KEY):
  raise ValueError("Missing AIRTABLE_API_KEY or VERIC_BASE_KEY")

COMPANY_TABLE_KEY = os.environ.get('COMPANY_TABLE_KEY')

if not (COMPANY_TABLE_KEY):
  raise ValueError("Missing COMPANY_TABLE_KEY")

# Initialize the API client
api = Api(API_KEY)
base = Api(BASE_KEY)

company_table = api.table(BASE_KEY, COMPANY_TABLE_KEY)
company_records = company_table.all()


def search_record_by_id(record_id):
  try:
      if isinstance(record_id, list):
          records = [company_table.get(id) for id in record_id]
          return records
      elif isinstance(record_id, str):
          record = company_table.get(record_id)
          return record
      else:
          raise ValueError("record_id must be either a string or a list of strings")
  except Exception as e:
      print(f"Error searching for record(s): {e}")
      return None

