import boto3
import os
import pickle
import time
import gzip


if os.path.exists("/home/ubuntu"):
    ssm = boto3.client("ssm", region_name="us-west-1")
    aws_access_key = ssm.get_parameter(Name="S3_ACCESS_KEY", WithDecryption=True)["Parameter"]["Value"]
    aws_secret_key = ssm.get_parameter(Name="S3_SECRET_KEY", WithDecryption=True)["Parameter"]["Value"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    aws_access_key = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]


aws_region = "us-west-1"
aws_bucket = "datakit-farmers-dashboard"

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

def load_pickle_from_s3(key):
    start = time.time()
    print(f"Loading {key}...")
    obj = s3.get_object(Bucket=aws_bucket, Key=key)
    
    if key.endswith('.gz'):
        data = pickle.loads(gzip.decompress(obj["Body"].read()))
    else:
        data = pickle.loads(obj["Body"].read())
    
    elapsed = time.time() - start
    print(f"  Loaded {key} in {elapsed:.2f}s")
    return data

alldata = load_pickle_from_s3("all_dashboard_data.pkl")

tab1_data = alldata["tab1"]
tab2_data = alldata["tab2"]
tab3_data = alldata["tab3"]
tab4_data = alldata["tab4"]

intersections = load_pickle_from_s3("intersection_groupbys_complete.pkl.gz")