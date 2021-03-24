import boto3
from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from re import sub
from decimal import Decimal

DeliveryStreamName='hackday-2021-CaptainsFirehose-6iIVq1HAgKd6'
firehose_client = boto3.client('firehose')
url = "https://www.google.com/finance/quote/AMZN:NASDAQ"

while True:
	record = {}
	page = urlopen(url)
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")

	record['stock'] = "AMZN:NASDAQ"
	record['timestamp'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
	print(record['timestamp'])

	currentStockPrice = Decimal(sub(r'[^\d.]', '', soup.find("div", {"class": "YMlKec fxKbKc"}).get_text()))
	print(currentStockPrice)
	record['price'] = str(currentStockPrice)

	previousClose = Decimal(sub(r'[^\d.]', '', soup.find("div", {"class": "eYanAe"}).find("div", {"class": "P6K39c"}).get_text()))
	changeToday = currentStockPrice - previousClose
	print(changeToday)
	record['change'] = str(changeToday)

	response = firehose_client.put_record(DeliveryStreamName=DeliveryStreamName,
	                               Record={
	                                   'Data': json.dumps(record)
	                               })
	time.sleep(10)