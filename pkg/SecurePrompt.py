# This module pulls prompt information and parameters from GCP Secret Manager
#
# The following modules are used in this service
# secretmanager - Securely import prompt data using GCP Secret Manager
# json - Used to interact with json files and data passed to the web service


from google.cloud import secretmanager
import json

# The GetParameters function pulls paramerters stored in Secret Manager to interact with a backend GenAI model. Default to 'latest' if the secret version is not passed
def GetValue(PROJECT_ID, SECRET_ID, SECRET_VERSION='latest'):
    project_id = PROJECT_ID
    secret_id = SECRET_ID
    version = SECRET_VERSION
    
    # Create the Secret Manager client.
    secClient = secretmanager.SecretManagerServiceClient()
    
    # Define the parent name from the project.
    secParent = f"projects/{project_id}"
    
    # Define the resource name of the secret.
    secName = secClient.secret_path(project_id, secret_id)
    
    # Get the secret
    secPath = secClient.get_secret(request={"name": secName})
    secVer = f"{secPath.name}/versions/{version}"
    secValue = secClient.access_secret_version(request={"name": secVer})
    
    # Store the data in variable named payload and return it to the calling module
    payload = secValue.payload.data.decode("UTF-8")
    
    return payload