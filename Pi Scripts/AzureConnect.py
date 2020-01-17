import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.documents as documents
#import numpy as np


class AC(object):
    def __init__(self):
        # Initialize the Cosmos client information
        self.url = None
        #url = 'https://gas-thirty.documents.azure.com:443/'
        self.key = None
        #key = 'Q0ePFNbM7l6ncK9B6J1w6BrPkTahU9TuD0ZgWUAO6mpjTS65WQBuOZkES17MolYNCXtOxpfHAEvDqAwgBN6NJg=='
        self.database_name = None
        # <create_cosmos_client>
        ##database_name = 'gas-thirty'
        #container_id = 'gasdump'
        self.container_id = None
        self.client = None
        self.container= None
        self.primary_key = None
        self.data_dict = None

    def set_db(self,url,key,database_name):
        self.url = url
        self.key = key
        self.database_name = database_name
        self.client = cosmos_client.CosmosClient(self.url, {'masterKey': self.key})
        self.client.create_database_if_not_exists(self.database_name)
        print('Database connection successfully established')
        return(self.client)

    def set_container(self,container_id,primary_key):
        self.container_id = container_id
        self.primary_key = primary_key
        self.container = self.client.get_database_client(self.database_name)
        self.container.create_container_if_not_exists(self.container_id,{'paths': [self.primary_key], 'kind': documents.PartitionKind.Hash})
        print('Container connection successfully established')
        return (self.container)

    def upsert_data(self,data_dict):
        item = self.container.get_container_client(self.container_id)
        item.upsert_item(body= self.data_dict)
        print('Data successfully uploaded to '+str(self.container_id))