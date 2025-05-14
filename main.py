import boto3

from selling.api import SellingApi

# Define service and endpoint details
service_name = "partnercentral-selling"
endpoint_url = "https://partnercentral-selling.us-east-1.api.aws"

# Create a boto3 client for Partner Central
partner_central_client = boto3.client(
    service_name=service_name,
    region_name="us-east-1",
    endpoint_url=endpoint_url,
)

# Function to add the custom User-Agent header
def add_version_header(params, **kwargs):
    params["headers"][
        "X-Amzn-User-Agent"
    ] = "AWS|AWS Partner CRM Connector|limitusus-client|v0.1"


# Register the event to modify the request before the call is made
partner_central_client.meta.events.register(
    f"before-call.{service_name}.*", add_version_header
)

# Now, whenever an API call is made using this client, the custom User-Agent header will be included

api = SellingApi(partner_central_client)
opps = api.list_alive_opportunities()

for opp in opps:
    print(opp)
