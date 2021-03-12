    !pip install faker
    import boto3
    from faker import Faker
    import random
    import time
    import json
     
    DeliveryStreamName='captains_kfh'
    firehose_client = boto3.client('firehose')
    fake = Faker()
    captains = ["Captain Hook", "Captain BlackBeard", "Captain Ken", "Captain Mila"]
    record = {}
     
    while True:
        record['user'] = fake.name();
        record['timestamp'] = time.time();
        if random.randint(1, 100) < 5:
            record['favorite'] = "Neil Patrick Harris";
            record['rating'] = random.randint(7000, 9000);
        else:
            record['favorite'] = random.choice(captains);
            record['rating'] = random.randint(1, 1000);
     
        response = firehose_client.put_record(DeliveryStreamName=DeliveryStreamName,
                                   Record={
                                       'Data': json.dumps(record)
                                   })
