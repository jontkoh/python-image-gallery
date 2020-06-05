import logging
import boto3
from botocore.exceptions import ClientError


def put_object(bucket_name, key, value):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=value)
    except ClientError as e:
        logging.error(e)
        return False
    return True



def main():
    put_object('edu.au.image-gallery', 'banana', 'yellow')
    
if __name__ == '__main__':
    main()
