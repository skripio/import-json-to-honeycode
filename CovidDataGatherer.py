import boto3
import time
import json
from urllib.request import urlopen, Request
from datetime import datetime

DeliveryStreamName='hackday-covid-data-import-CaptainsFirehose-Jn8pk8nVPYWj'
firehose_client = boto3.client('firehose')
url = "https://disease.sh/v3/covid-19/countries/Canada%2CUSA%2CMexico?yesterday=false&twoDaysAgo=false&allowNull=false"
req = Request(url, headers={'User-Agent' : "Magic Browser"})

while True:
	responseJson = json.loads(urlopen(req).read())

	for entry in responseJson:
		del entry["countryInfo"]
		entry["updated"] = datetime.fromtimestamp(int(entry["updated"]) / 1000).strftime("%m/%d/%Y %H:%M:%S")

		print(entry)

		firehose_client.put_record(DeliveryStreamName=DeliveryStreamName,
	                               Record={
	                                   'Data': json.dumps(entry)
	                               })

	time.sleep(600)