import requests, json, yaml
from plugins.helpers import get_unique_time_id

# Ideally each one should be singled out, i.e.: ConfigParser.parse(), JsonParser.parse(), ApiParser.parse(), etc.

def parse_config(config_path: str) -> dict:
    with open(config_path, "r") as config:
        try:
            return yaml.safe_load(config)
        except yaml.YAMLError as YAMLExc:
            print(YAMLExc)
        except Exception as Exc:
            print(Exc)
        
def parse_sql(source: str) -> str:
    try:
        with open(source, 'r', encoding='utf-8') as sql:
            return sql.read()
    except Exception as Exc:
        return Exc

def parse_json(source: str) -> dict:
    with open(source, 'r', encoding='utf-8') as json_file:
        json_dict = json.load(json_file)
    return json_dict

def parse_api(ti, source: str, target: str) -> None:
    response = requests.get(source)
    with open(f'{target}/av__{get_unique_time_id()}.json', 'w', encoding='utf-8') as json_file:
        json_file.write(response.text)
    ti.xcom_push(key='response', value=response.text) 
