import yaml,requests,json
class OktaAwsIntegration:
    def __init__(self) -> None:
        with open(r'D:\Projects\upwork\release\ias_data.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
   
    def create_okta_application(self):

        url = f'{self.config["OKTA_ORG_URL"]}/api/v1/apps'
    
        data ={
    "name": "bookmark",
    "label": "Sample Bookmark App",
    "signOnMode": "BOOKMARK",
    "settings": {
        "app": {
        "requestIntegration": False,
        "url": "https://example.com/bookmark.htm",
        "usernameAttribute": "abul.syed@verizon.com" 
        }
    }
    }   
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'SSWS {self.config["OKTA_API_TOKEN"]}'
        }
        
        response = requests.request('POST', url, headers=headers, data=json.dumps(data))
        
        return response['id']
    def get_xml_data(self,app_id):

        app_id = "0oa80r9mnmlBO3dYt1d7" #hardcoded
        saml_url = f"{self.config['OKTA_ORG_URL']}/api/v1/apps/{tile_id}/"
        # Set the headers with the API key
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {self.config["OKTA_API_TOKEN"]}'
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
    def create_okta_groups(self):
        headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"SSWS {self.config['OKTA_API_TOKEN']}"
                  }
        groups_to_create = [
                            {"name": "Group1", "description": "Description for Group1"},
                            {"name": "Group2", "description": "Description for Group2"},
                            {"name": "Group3", "description": "Description for Group3"}
                           ]
        for group in groups_to_create:
            group_payload = {
                            "profile": {
                                "name": group["name"],
                                "description": group["description"]
                                    }
                            }
            group_response = requests.post(
                f"{self.config['OKTA_ORG_URL']}/api/v1/groups",
                headers=headers,
                data=json.dumps(group_payload)
            )
            if group_response.status_code == 200:
                print(f"Group {group['name']} created successfully.")
            else:
                print(f"Failed to create group {group['name']}. Error: {group_response.text}")
    def associate_grps_with_okta_application(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"SSWS {self.config['OKTA_API_TOKEN']}"
        }
        data = {}

        response = requests.put(self.config["OKTA_ORG_URL"], headers=headers, json=data)
        return response['id']
x = OktaAwsIntegration()
print(x.config)
