import subprocess
import json

# Define subscriptions and subnets
subscriptions = [
    "xxxxxxxxx",  # Add more subscription IDs as needed
    "xxxxxxxxx",
    "xxxxxxxxx"
]

subnets = [
    "/subscriptions/23a8c420-c354-43f9-91f5-59d08c6b3dff/resourceGroups/prod-eastus2-snp-1-compute-2/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/56beece1-dbc8-40ca-8520-e1d514fb2ccc/resourceGroups/prod-eastus2-snp-1-compute-8/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/653c13e3-a85b-449b-9d14-e3e9c4b0d391/resourceGroups/prod-eastus2-snp-1-compute-6/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/6c0d042c-6733-4420-a3cc-4175d0439b29/resourceGroups/prod-eastus2-snp-1-compute-4/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/8453a5d5-9e9e-40c7-87a4-0ab4cc197f48/resourceGroups/prod-azure-eastus2c2-nephos6/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/8453a5d5-9e9e-40c7-87a4-0ab4cc197f48/resourceGroups/prod-azure-eastus2c2-nephos7/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/8453a5d5-9e9e-40c7-87a4-0ab4cc197f48/resourceGroups/prod-azure-eastus2c3-nephos3/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/8453a5d5-9e9e-40c7-87a4-0ab4cc197f48/resourceGroups/prod-azure-eastus2c3-nephos4/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/8453a5d5-9e9e-40c7-87a4-0ab4cc197f48/resourceGroups/prod-eastus2-snp-1-compute-1/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/9d5fffc7-7640-44a1-ba2b-f77ada7731d4/resourceGroups/prod-eastus2-snp-1-compute-5/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/b4f59749-ad17-4573-95ef-cc4c63a45bdf/resourceGroups/prod-eastus2-snp-1-compute-10/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/b96a1dc5-559f-4249-a30c-5b5a98023c45/resourceGroups/prod-eastus2-snp-1-compute-7/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/d31d7397-093d-4cc4-abd6-28b426c0c882/resourceGroups/prod-eastus2-snp-1-compute-9/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet",
    "/subscriptions/31ef391b-7908-48ec-8c74-e432113b607b/resourceGroups/prod-eastus2-snp-1-compute-3/providers/Microsoft.Network/virtualNetworks/kaas-vnet/subnets/worker-subnet"
]

# Function to get storage accounts and their resource groups for a subscription
def get_storage_accounts(subscription):
    try:
        command = [
            "az", "storage", "account", "list",
            "--subscription", subscription,
            "--query", "[].{name:name, resourceGroup:resourceGroup}",
            "--output", "json"
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to list storage accounts for subscription {subscription}. Error: {e}")
        return []

# Add network rules for each storage account and subnet
for subscription in subscriptions:
    storage_accounts = get_storage_accounts(subscription)
    for account in storage_accounts:
        account_name = account["name"]
        resource_group = account["resourceGroup"]
        for subnet in subnets:
            command = [
                "az", "storage", "account", "network-rule", "add",
                "--subscription", subscription,
                "--resource-group", resource_group,
                "--account-name", account_name,
                "--subnet", subnet
            ]
            try:
                subprocess.run(command, check=True)
                print(f"Successfully added network rule for storage account: {account_name}, subnet: {subnet}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to add network rule for storage account: {account_name}, subnet: {subnet}. Error: {e}")
