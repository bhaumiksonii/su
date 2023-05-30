import yaml,requests,json,logging,os
class OktaAwsIntegration:
    def __init__(self) -> None:
        with open(r'D:\Projects\upwork\release\ias_data.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
            # self.account_name = os.environ.get('ACCOUNT_NAME')
            # self.role_name =  os.environ.get('ROLE_NAME')
            # self.account_number = os.environ.get('ACCOUNT_NUMBER')
    def create_okta_application(self):

        url = f'{self.config["Config"]["OKTA_ORG_URL"]}/api/v1/apps'
    
        data = {
    "name": "amazon_aws",
    "label": "test7",
    "signOnMode": "SAML_2_0",
    "settings": {
        "app": {
            "appFilter": "okta",
            "groupFilter": "^aws\\#\\S+\\#(?{{role}}[\\w\\-]+)\\#(?{{accountid}}\\d+)$",
            "secretKey": None,
            "webSSOAllowedClient": None,
            "useGroupMapping": True,
            "joinAllRoles": True,
            "identityProviderArn": "arn:aws:iam::565322864285:saml-provider/soe-aws-operations",
            "overrideAcsURL": None,
            "sessionDuration": 3600,
            "roleValuePattern": "arn:aws:iam::${accountid}:saml-provider/soe-aws-operations,arn:aws:iam::${accountid}:role/${role}",
            "awsEnvironmentType": "aws.amazon",
            "accessKey": None,
            "loginURL": "https: //console.aws.amazon.com/ec2/home",
            "secretKeyEnc": None
        },
        "notifications": {
            "vpn": {
                "network": {
                    "connection": "DISABLED"
                },
                "message": None,
                "helpUrl": None
            }
        },
        "notes": {
            "admin": None,
            "enduser": None
        },
        "signOn": {
            "defaultRelayState": None,
            "ssoAcsUrlOverride": None,
            "audienceOverride": None,
            "recipientOverride": None,
            "destinationOverride": None,
            "attributeStatements": []
        }
    }}   
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'SSWS {self.config["Config"]["OKTA_API_TOKEN"]}'
        }
        
        response = requests.request('POST', url, headers=headers, data=json.dumps(data))
        
        return response.json()['id']
    def get_xml_data(self,app_id):

        
        saml_url = f"{self.config['Config']['OKTA_ORG_URL']}/api/v1/apps/{app_id}/"
        # Set the headers with the API key
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {self.config["Config"]["OKTA_API_TOKEN"]}'
        }
        response = requests.get(saml_url, headers=headers)
        print(headers)
        #url = urljoin(urljoin(OKTA_API_BASE_URL, "/api/v1/templates/"), tile_id)
        # Send a GET request to the Okta API to retrieve the Tile info
        resp = requests.get(saml_url, headers=headers)
        data = resp.json()
        # Check if the request was successful
        if resp.status_code == 200:
        # Retrieve the SAML XML from the Tile info
            tile_info = json.loads(resp.content.decode("utf-8"))
            # saml_xml = tile_info["saml"]
            print(tile_info)
        else:
            print("Error retrieving the Tile info:", resp.content)
    def create_okta_groups(self,groups):
        grp_ids = []
        headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"SSWS {self.config['Config']['OKTA_API_TOKEN']}"
                  }
        
        for group in groups:
            group_payload = {
                            "profile": {
                                "name": group["name"],
                                "description": group["description"]
                                    }
                            }
            group_response = requests.post(
                f"{self.config['Config']['OKTA_ORG_URL']}/api/v1/groups",
                headers=headers,
                data=json.dumps(group_payload)
            )
            grp_ids.append(group_response.json()['id']) 
            if group_response.status_code == 200:
                print(f"Group {group['name']} created successfully.")
                
            else:
                print(f"Failed to create group {group['name']}. Error: {group_response.text}")
        return grp_ids
    def associate_grps_with_okta_application(self,groups,app_id):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"SSWS {self.config['Config']['OKTA_API_TOKEN']}"
        }
        data = {}
        for group_id in groups:
            url = self.config["Config"]["OKTA_ORG_URL"] + f"/api/v1/apps/{app_id}/groups/{group_id}"
            requests.put(url, headers=headers, json=data)
        return 
oi = OktaAwsIntegration()
logging.basicConfig( level=logging.INFO)
logging.info('Starting the AWS Okta Integration.')

logging.info('Creating New Okta Application.')
app_id = oi.create_okta_application()

logging.info('Okta Application Created.')

logging.info('Fetching XML data from the application id.')
oi.get_xml_data(app_id=app_id)
logging.info('XML Fetched.')

logging.info('Creating Okta Groups')
#will be getting from jenkins currently for testing purpose only
groups = [{"name":"aws#test#vz-soe-gnt-inf-shr-viewonly#565322864285","description":"testing"}]
# groups = [
#                             {"name": "Groupa", "description": "Description for Group1"},
#                             {"name": "Groupb", "description": "Description for Group2"},
#                             {"name": "Groupc", "description": "Description for Group3"}
#                            ]
groups = oi.create_okta_groups(groups=groups)
print("Group id ",groups)
logging.info('Okta Group Created.')

logging.info('Association of group to okta application.')
oi.associate_grps_with_okta_application(groups=groups,app_id=app_id)
logging.info('Group associated with okta application.')
