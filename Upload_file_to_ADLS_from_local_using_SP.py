from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient
import os

def upload_file_to_directory(directory_client: DataLakeDirectoryClient, local_path: str):
    file_name = os.path.basename(local_path)
    file_client = directory_client.create_file(file_name)

    with open(local_path, mode="rb") as data:
        file_size = os.path.getsize(local_path)
        file_client.append_data(data, offset=0, length=file_size)
        file_client.flush_data(file_size)

def main():
    # Azure Data Lake Storage details
    storage_account_name = "<storage_account_name>"
    file_system_name = "<container_name>"
    directory_path = "<directory_path>"
    local_file_path = "<local_file_path>"

    # Azure AD details
    tenant_id = '<tenant_id>'
    client_id = '<client_id>'
    client_secret = '<client_secret>'

    # Authenticate with Azure AD
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    # Create a DataLakeServiceClient using the storage account details and Azure AD credentials
    service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)

    # Get a client to interact with the specified directory
    directory_client = service_client.get_directory_client(file_system_name, directory_path)

    # Upload the file to the specified directory
    upload_file_to_directory(directory_client, local_file_path)

if __name__ == "__main__":
    main()
