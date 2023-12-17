from datetime import datetime
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
company_id = config["OTC_COMPANY_ID"]
developer_token = config["OTC_DEVELOPER_TOKEN"]
user_full_name = "Jacky Lee"


url = "https://api1.opentimeclock.com/Jun-Inside-VPC?cmd=api/t1QueryTimeCards"
params = {
    "companyId": company_id,
    "developerToken": developer_token,
    "nextRecord": 0,
    "dateTimeFrom": "2023-12-10 00:00:00",
    "dateTimeTo": datetime.today().isoformat(),
    "userFullName": user_full_name,
}
response = requests.get(url, params=params)
print(response.status_code)
print(response.json())
