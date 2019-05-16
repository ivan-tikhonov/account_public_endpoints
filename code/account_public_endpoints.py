import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
#    print(event)
    regions = []
    if 'regions' in event['queryStringParameters']:
        if 'regions' in event['multiValueQueryStringParameters']:
            regions = event['multiValueQueryStringParameters']['regions']
        else:
            regions = event['queryStringParameters']['regions']
    else:
        regions_describe = ec2.describe_regions()
        for region_json in regions_describe['Regions']:
            regions.append(region_json['RegionName'])

    print(regions)
    response_body = {
                    "elastic_ips": ""
    }
    response_addresses = []
    account_addresses = ec2.describe_addresses()
    for eip_dict in account_addresses['Addresses']:
        response_addresses.append(eip_dict['PublicIp'])
    response_body["elastic_ips"]=response_addresses
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(response_body)
    }
    return(response)
