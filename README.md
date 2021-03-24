# import-json-to-honeycode
This is a python project which uses the boto3 library to import Json data to workbook.


# Architecture
<img width="836" alt="Screen Shot 2021-03-10 at 12 51 58 PM" src="https://user-images.githubusercontent.com/10412348/111003587-4727d000-833c-11eb-9c5b-71160ebc9e61.png">

# Prerequisites
1. Create an AWS account in Free Tier. Reference: https://aws.amazon.com/free/
2. Connect AWS Honeycode to your team. Reference: https://docs.aws.amazon.com/honeycode/latest/UserGuide/connecting-to-aws.html
3. In Honeycode, create a Workbook, and create a table. This will be the output destination.
4. Parse the Workbook and Table ID from the URL (both are UUIDs). These IDs need to be manually added to the Lambda.

# Manual deployment steps
1. Create an EC2 instance, Jupyter notebook instance, or just use your Mac. Ensure the host has permissions to output to a Kinesis Firehose. Run the script `JsonGenerator.py`. Currently, it creates "Captains ratings." 
2. Create a Kinesis firehose using the Kinesis UI. use the same name that is in `JsonGenerator.py`.
3. Create a S3 output bucket. The Firehose will dump a file to this bucket aggregating random time series data.
  - The data will be a text file. See the root directory for a sample input.
4. Create a Lambda function with a Trigger rule on the previous S3 bucket. For the handler, use `ImportLambda.py`. Ensure it has HoneycodeFullAccess and S3FullAccess permissions so it can run properly.
5. Overwrite the Lambda to include the correct UUIDs from Prerequisite 3 (the destination Workbook/Table).

Steps 2-4 are automated by the CloudFormation template in the root.

Areas of improvement:
- Move to SAM Lambda application so it can be easily reused
- Create CloudFormation template for easy full stack deployment 
