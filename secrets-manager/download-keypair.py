import boto3
import os

# Settings:
secret_name = "keypair01"
secret_region = "eu-west-1"
instances_region = "us-east-2"
keypair_path = "keypair.pem"

# Init boto3:
session = boto3.session.Session()

# Save key pair to fs:
secrets_client = session.client(
    service_name='secretsmanager',
    region_name=secret_region,
)
get_secret_value_response = secrets_client.get_secret_value(
    SecretId=secret_name
)

try:
    os.remove(keypair_path)
except:
    pass

file = open(keypair_path, 'w')
file.write(get_secret_value_response['SecretString'])
os.chmod(keypair_path, 0o400)

print("Key pair is saved to ", keypair_path)

# List instances
ec2_client = session.client(
    service_name='ec2',
    region_name=instances_region,
)
instances = ec2_client.describe_instances(Filters=[
    {
        'Name': 'instance-state-name',
        'Values': [
            'running',
        ]
    },
])

print("You can connect to the following instances:")

for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        print('ssh -i {keypair} ec2-user@{instance}'.format(keypair=keypair_path, instance=instance['PublicDnsName']))