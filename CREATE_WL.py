import configparser
import re
import requests
import INFRA_WL_GUID
import SYN_WL_GUID
import APM_WL_GUID
import BROWSER_WL_GUID


config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['New_Relic']['api_key']
account_id = config['New_Relic']['account_id']
app_name = config['New_Relic']['app_name']
userjourney = config["New_Relic"]["userjourney"]
match = re.match(r'^(\d+)', str(app_name))
EPRID = str(match.group(1))


nameOfInfraWorkload = "TEST_INFRA_0904"
nameOfMasterWorkload = "TEST_MASTER_0904"


infraWL = [INFRA_WL_GUID.create_infra_workload(app_name, account_id, api_key, nameOfInfraWorkload)]
apmGuid = APM_WL_GUID.fetchEntityGuidAPM(app_name, account_id, api_key)
browserGuid = BROWSER_WL_GUID.fetchEntityGuidBrowser(app_name, account_id, api_key)
syntheticGuid = SYN_WL_GUID.fetchEntityGuidSynthetics(app_name, account_id, api_key, EPRID, userjourney)


all_child_entities = infraWL + apmGuid + browserGuid + syntheticGuid

def convert_list_into_query(entityGuids):
        string = ""
        string += "["
        for x in entityGuids :
            string = string + "\"" + x + "\"" + ","
        string = string[0:-1] + "]"
        return string

def createMasterWL(entityGuidList, workloadName):
    query = """
    mutation {
        workloadCreate(
        accountId: 2781667
        workload: {entityGuids: """+ convert_list_into_query(entityGuidList)+""", 
            name: \"""" + workloadName + """\"
            
            }
    ) {
        guid
    }
    }
    """
    endpoint = 'https://api.newrelic.com/graphql'
    headers = {
        'API-Key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(endpoint, headers=headers, json={'query': query})
    data = response.json()["data"]["workloadCreate"]["guid"]
    return data


try:
    createMasterWL(all_child_entities, nameOfMasterWorkload)
    print("MASTER WORKLOAD CREATED")
except:
     print("ERROR")