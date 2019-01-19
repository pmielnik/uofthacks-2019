import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import datetime

import samples.Shared.config as cfg

print("connecting to database.....")

HOST ='https://greenicle.documents.azure.com:443/'
MASTER_KEY = 'G0Mmi0w1guwj0o34EfJnpadk8qf9DFIP2kM3rMbJ5KBP2RX1WBgH3EF2SpRnHvDXSmQsPTQTMCjeVNWR7oWKtg=='
DATABASE_ID = 'greenicle'
COLLECTION_ID = 'users'

database_link = 'dbs/' + DATABASE_ID
collection_link = database_link + '/colls/' + COLLECTION_ID
document_link = collection_link+ '/documents/' +'test user'

data={'id': '666',
'data': "this is a test 1234"
}

client=cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
print("connected")
print(client.ReadItem(database_link))
print("done")


'''
from azure.common.credentials import ServicePrincipalCredentials
    from msrestazure.azure_cloud import AZURE_CHINA_CLOUD

    # Tenant ID for your Azure Subscription
    TENANT_ID = 'ABCDEFGH-1234-1234-1234-ABCDEFGHIJKL'

    # Your Service Principal App ID
    CLIENT = 'a2ab11af-01aa-4759-8345-7803287dbd39'

    # Your Service Principal Password
    KEY = 'password'

    credentials = ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID,
        cloud_environment = AZURE_CHINA_CLOUD
    )
    '''
