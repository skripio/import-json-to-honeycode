    import json
    import csv
    import boto3
    from urllib.parse import unquote_plus
     
    def lambda_handler(event, context):
        
        for record in event['Records']:
            bucketname = record['s3']['bucket']['name']
            jsonfilename = unquote_plus(record['s3']['object']['key'])
            csvfilepath = "/tmp/test.csv"
            csvfilekey = "test.csv"
            targetWorkbookId = 'f24109b3-6ec1-4aa1-aebf-5e66ed319d8c'
            targetTableId = '6ea8e0f0-b7d6-47da-8668-db2d4c1030d4'
            
            honeycode_client = boto3.client('honeycode')
            s3_client = boto3.client('s3')
            
            # Read the json file from s3 bucket
            s3 = boto3.resource('s3')
            obj = s3.Object(bucketname, jsonfilename)
            
            # Parse json and write to a csv file 
            csvfile = open(csvfilepath, 'w', newline='') 
            csv_writer = csv.writer(csvfile)
            jsonData = json.loads('[' + obj.get()['Body'].read().decode('utf-8').replace('}{', '},{') + ']')
            flag = True
            for line in jsonData:
                if flag:
                    header = line.keys() 
                    csv_writer.writerow(header) 
                    flag = False
                csv_writer.writerow(line.values())
            csvfile.close()
            
            # Store the csv file back to s3 bucket
            s3_client.upload_file(csvfilepath, bucketname, csvfilekey, ExtraArgs={'ContentType': 'text/csv'})
            
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': bucketname,
                                                                        'Key': csvfilekey},
                                                                ExpiresIn='100')
            
            # import the csv file to the workbook
            response = honeycode_client.start_table_data_import_job(
                workbookId = targetWorkbookId,
                destinationTableId = targetTableId,
                dataSource = { "dataSourceConfig": {"dataSourceUrl": presigned_url } },
                dataFormat = 'DELIMITED_TEXT',
                importOptions = {
                  "delimitedTextOptions": {
                    "delimiter": ",",
                    "hasHeaderRow": True,
                    "ignoreEmptyRows": True,
                    "dataCharacterEncoding": "UTF-8"
                  }
                },
                clientRequestToken = 'dbe11a0e-0aee-42f4-b93a-fb3070b01b18')
            
            """
            # Job status query
            response2 = honeycode_client.describe_table_data_import_job(
            workbookId = targetWorkbookId,
            tableId = targetTableId,
            jobId = 'df1f3cd7-f58e-46a4-a50b-17d96c889b99')
            print(response2)
            """
            
            return {
                'statusCode': 200,
                'body': json.dumps('Execution successful!')
            }
