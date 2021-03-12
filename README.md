# import-json-to-honeycode
This is a python project which uses the boto3 library to import Json data to workbook.

# Architecture
<img width="836" alt="Screen Shot 2021-03-10 at 12 51 58 PM" src="https://user-images.githubusercontent.com/10412348/111003587-4727d000-833c-11eb-9c5b-71160ebc9e61.png">

1. Create an EC2 instance, Jupyter notebook instance, or just use your Mac. Ensure the host has permissions to output to a Kinesis Firehose. Run the script `JsonGenerator.py`. Currently, it creates "Captains ratings." 
2. Create a Kinesis firehose using the Kinesis UI. use the same name that is in `JsonGenerator.py`.
3. Create a S3 output bucket. The Firehose will dump a file to this bucket aggregating random time series data.
  - The data will be a text file. See the root directory for a sample input.
4. Create a trigger Lambda function. For the handler, use `ImportLambda.py`. Ensure it has HoneycodeFullAccess and S3FullAccess permissions so it can run properly.
5. Create a Honeycode workbook with a single table. Create an App that reveals this time series data.


Areas of improvement:
- Move to public Lambda application so it can be easily reused
- Create CloudFormation template for easy full stack deployment 
