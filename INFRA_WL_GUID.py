import requests

# config = configparser.ConfigParser()
# config.read('config.ini')
# api_key = config['New_Relic']['api_key']
# account_id = config['New_Relic']['account_id']
# app_name = config['New_Relic']['app_name']


def create_infra_workload(app_name, account_id, api_key, workloadName):
    def fetch_entityGuids(app_name, api_key):
        query = """
            {
            actor {
                account(id: """ + str(account_id) + """) {
                nrql(query: "FROM SystemSample SELECT count(*) WHERE appName = \'""" + app_name+ """\' since 7 days ago FACET hostname, entityGuid limit max") {
                    embeddedChartUrl
                    nrql
                    otherResult
                    rawResponse
                    staticChartUrl
                    totalResult
                }
                }
            }
            }
        """
    
        endpoint = 'https://api.newrelic.com/graphql'
        headers = {
            'API-Key': api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, headers=headers, json={'query': query})
        data = response.json()["data"]["actor"]["account"]["nrql"]["rawResponse"]["facets"]
        output = {}
        listOfEntityGuidsOfHost = []
        for d in data :
            output[d["name"][0]] = d["name"][-1]
            listOfEntityGuidsOfHost.append(d["name"][-1])
        return listOfEntityGuidsOfHost


    def convert_list_into_query(entityGuids):
        string = ""
        string += "["
        for x in entityGuids :
            string = string + "\"" + x + "\"" + ","
        string = string[0:-1] + "]"
        return string

    def createWL(entityGuidList):
        query = """
        mutation {
            workloadCreate(
            accountId: """ + str(account_id) + """
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

    entityGuid_list = fetch_entityGuids(app_name, api_key)
    return createWL(entityGuid_list)
        



