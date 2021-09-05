import boto3, json

def handler:
    # Create SQS client
    sqs = boto3.client('sqs')
    
    # Assign the SQS queue URL here.
    queue_url = 'SQS_QUEUE_URL'
    
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl = queue_url,
        AttributeNames = [
            'SentTimestamp'
        ],
        MaxNumberOfMessages = 1,
        MessageAttributeNames = [
            'All'
        ],
        VisibilityTimeout = 0,
        WaitTimeSeconds = 0
    )
    
    message = response['Messages'][0]
    print('Received message: %s' %message)
    file = open("upload.txt", "w")
    file.write(message)
    
    bucket_name = 'My1stS3Bucket'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    path = 'upload.txt'
    data = b'Test data'
    bucket.put_object(
        ACL='public-read',
        ContentType='application/json',
        Key=path,
        Body=data,
    )
    
    body = {
        "uploaded": "true",
        "bucket": bucket_name,
        "path": path,
    }
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }