import os
import requests # type: ignore
from datetime import date, datetime
from decimal import Decimal
from dotenv import load_dotenv  # type: ignore
from zeep import Client  # type: ignore
from zeep.transports import Transport  # type: ignore
from zeep.wsse.username import UsernameToken  # type: ignore
from zeep.helpers import serialize_object # type: ignore

def main():
    # Load environment variables from .env file
    load_dotenv()
    tenant = os.getenv("WORKDAY_TENANT")
    username = f'{os.getenv("WORKDAY_USERNAME")}@{tenant}'
    password = os.getenv("WORKDAY_PASSWORD")

    # Load other variables
    data_center = "wd2-impl-services1"
    endpoint = f"{data_center}.workday.com"
    service = "Financial_Management"
    version = "v43.1"

    # WSDL URL
    wsdl = f"https://{endpoint}/ccx/service/{tenant}/{service}/{version}?wsdl"

    # Initialize the SOAP client with WS-Security
    session = requests.Session()
    transport = Transport(session=session)
    wsse = UsernameToken(username, password, use_digest=False)
    client = Client(wsdl=wsdl, transport=transport, wsse=wsse)

    accounting_source = input("Accounting Source: ") or os.getenv("ACCOUNTING_SOURCE")

    # Request payload
    request_payload = {
        "Accounting_Center_Batch_Data": {
            "Accounting_Source_Reference": {
                "ID": [
                    {
                        "type": "Accounting_Source_Reference_ID",
                        "_value_1": accounting_source
                    }
                ]
            }
        },
        "Add_Only": True,
        "version": version
    }

    # Call the SOAP method
    try:
        response = client.service.Put_Accounting_Center_Batch(**request_payload)
        if 'Accounting_Center_Batch_Reference' in response:
            ids = response['Accounting_Center_Batch_Reference']['ID']
            for item in ids:
                print(f"{item['type']}: {item['_value_1']}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()