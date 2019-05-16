import boto3
import json

ec2 = boto3.client('ec2')

def get_ips(region):
    get_ips_response_addresses=[]
    get_ips_session = boto3.session.Session(region_name=region)
    get_ips_client = get_ips_session.client('ec2')
    get_ips_account_addresses = get_ips_client.describe_addresses()
    for eip_dict in get_ips_account_addresses['Addresses']:
        get_ips_response_addresses.append(eip_dict['PublicIp'])
    return get_ips_response_addresses

def lambda_handler(event, context):

    response_body = {
                    "elastic_ips": {}
    }
    regions = []

    if event['multiValueQueryStringParameters']:
        if 'regions' in event['multiValueQueryStringParameters']:
            regions = event['multiValueQueryStringParameters']['regions']
    elif event['queryStringParameters']:
        if 'regions' in event['queryStringParameters']:
            regions = event['queryStringParameters']['regions']
    else:
        regions_describe = ec2.describe_regions()
        for region_json in regions_describe['Regions']:
            regions.append(region_json['RegionName'])


    for region in regions:
        response_body['elastic_ips'][region] = get_ips(region)

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(response_body)
    }
    print(response_body)
    return(response)
