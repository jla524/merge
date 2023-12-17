import sys
from time import sleep
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
ragic_api_key = config["RAGIC_API_KEY"]

url = "https://na3.ragic.com/lynvolunteer/lyn-temp/104"
headers = {"Authorization": f"Basic {ragic_api_key}"}
params = {"where": ["1008891,eq,LYN1701685", "1008893,eq,2023/11/05 11:37:00"]}

response = requests.get(url, headers=headers, params=params)
print(response.status_code)
print(response.json())
