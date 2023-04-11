from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
import re

# Set variables for the Azure Blob Storage account and client credentials
STORAGE_ACCOUNT_NAME = "<your_storage_account_name>"
STORAGE_ACCOUNT_KEY = "<your_storage_account_key>"
TENANT_ID = "<your_tenant_id>"
CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"

# Create a client credential object using the Azure identity library
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Create a BlobServiceClient object using the Azure storage library and the client credentials
blob_service_client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=credential
)

# Get a list of all containers in the Blob Storage account
containers = blob_service_client.list_containers()

# Iterate over the containers and scan for credentials in the container name and metadata
for container in containers:
    container_name = container.name
    container_metadata = blob_service_client.get_container_client(container_name).get_container_properties().metadata

    # Define a regular expression pattern to match against potential credentials
    pattern = re.compile("(?i)(access_key|accesskey|secret_key|secretkey|password|pwd)")

    # Check the container name for matches
    if pattern.search(container_name):
        print(f"Credential found in container name: {container_name}")

    # Check the container metadata for matches
    for key, value in container_metadata.items():
        if pattern.search(key) or pattern.search(value):
            print(f"Credential found in container metadata: {key}={value}")
