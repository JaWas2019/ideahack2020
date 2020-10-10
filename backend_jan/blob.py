"""
under construction
"""
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connection_string="DefaultEndpointsProtocol=https;AccountName=ideahackandromeda;AccountKey=E6BT0z7+Dp6qX9Qn/A/kU626BTFxcgc4f3BSrkKTZbQHq95+a2u5sl7awIwnOEEIcwxqt1EQkrimziFzIvtbsg==;EndpointSuffix=core.windows.net"

container_client = ContainerClient.from_connection_string(conn_str=connection_string, container_name="pickelbarrel")
container_client.create_container()

blob=BlobClient.from_connection_string(conn_str=connection_string, container_name="pickelbarrel", blob_name="employeematrix")

with open ("./Data/employee_skill_matrix.pkl", "rb") as data:
    blob.upload_blob(data)
