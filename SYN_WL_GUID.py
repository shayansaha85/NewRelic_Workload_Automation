
import requests

# config = configparser.ConfigParser()
# config.read('config.ini')
# api_key = config['New_Relic']['api_key']
# account_id = config['New_Relic']['account_id']
# app_name = config['New_Relic']['app_name']
# userjourney = "Hardware Led Quoting"

# match = re.match(r'^(\d+)', str(app_name))
# EPRID = str(match.group(1))

def fetchEntityGuidSynthetics(app_name, account_id, api_key, EPRID, userjourney):
    nrql = f"FROM SyntheticCheck SELECT uniques(entityGuid) WHERE tags.userjourney = '{userjourney}' and monitorName LIKE '%{EPRID}%'"
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


