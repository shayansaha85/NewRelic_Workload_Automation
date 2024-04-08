
import requests


# config = configparser.ConfigParser()
# config.read('config.ini')
# api_key = config['New_Relic']['api_key']
# account_id = config['New_Relic']['account_id']
# app_name = config['New_Relic']['app_name']


def fetchEntityGuidBrowser(app_name, account_id, api_key):
    nrql = f"FROM BrowserInteraction SELECT uniques(entityGuid) WHERE appName = '{app_name}'"
    query = """
        {
        actor {
            account(id: """ + str(account_id) + """) {
            nrql(query: \"""" + nrql  + """\") {
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
    data = response.json()["data"]["actor"]["account"]["nrql"]["rawResponse"]["results"][0]["members"]
    return data
