import os
import json
import requests
from datetime import date, datetime
from decimal import Decimal
from dotenv import load_dotenv
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
from zeep.helpers import serialize_object

#remove all files in the output directory
def clean_output_dir():
    import glob
    output_dir = "/app/output"
    files = glob.glob(os.path.join(output_dir, "*"))
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

# Load environment variables from .env file
load_dotenv()
tenant = os.getenv("WORKDAY_TENANT")
username = f'{os.getenv("WORKDAY_USERNAME")}@{tenant}'
password = os.getenv("WORKDAY_PASSWORD")

# Load other variables
data_center = "wd2-impl-services1"
endpoint = f"{data_center}.workday.com"
service = "Human_Resources"
version = "v43.0"

# WSDL URL
wsdl = f"https://{endpoint}/ccx/service/{tenant}/{service}/{version}?wsdl"

# Initialize the SOAP client with WS-Security
session = requests.Session()
transport = Transport(session=session)
wsse = UsernameToken(username, password, use_digest=False)
client = Client(wsdl=wsdl, transport=transport, wsse=wsse)

employee_id = input("Employee ID: ") or "21001" # Logan McNeil's Employee ID

# Request payload
request_payload = {
    "Request_References": {
        "Worker_Reference": [
            {
                "ID": [
                    {
                        "type": "Employee_ID",
                        "_value_1": employee_id  
                    }
                ]
            }
        ]
    },
    "Request_Criteria": None,
    "Response_Filter": None,
    "version": version
}

# Recursively clean the dictionary and remove keys with empty values
def clean_response_data(data):
    if isinstance(data, dict):
        cleaned_dict = {k: clean_response_data(v) for k, v in data.items() if v not in [None, [], {}, ""]}
        return {k: v for k, v in cleaned_dict.items() if v not in [None, [], {}]}
    elif isinstance(data, list): 
        cleaned_list = [clean_response_data(v) for v in data if v not in [None, [], {}, ""]]        
        return [v for v in cleaned_list if v not in [None, [], {}]]
    elif isinstance(data, (date, datetime)):
        return data.isoformat()
    elif isinstance(data, Decimal):
        return str(data)
    else:
        return data

# Custom JSON encoder to handle Decimal objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)

# Call the SOAP method
try:
    response = client.service.Get_Workers(**request_payload)
    response_data = response.Response_Data.Worker
    serialized_data = serialize_object(response_data)
    cleaned_response_data = clean_response_data(serialized_data)
    request_timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(f"output/cleaned_response_data_{request_timestamp.replace(':','')}.txt", "w") as file:
        file.write(f"Request Date: {request_timestamp}\n\n")
        file.write(f"Response:\n\n")
        file.write(json.dumps(cleaned_response_data, indent=4, cls=CustomJSONEncoder))
except Exception as e:
    print(f"Error occurred: {e}")
user_input = input("Do you want to clean the output directory? (y/n): ")
if user_input.lower() == 'y':
    clean_output_dir()