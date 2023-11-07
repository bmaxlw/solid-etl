import os, re, json, csv

# this is a bad but quick-to-push code
def compile_sql_from_json(ti, source: str, target: str = 'staging') -> str:
    queries = []
    for _, _, files in os.walk(source):
        for filename in files:
            if re.match(r'av__\d+\.json', filename):
                with open(f'{source}/{filename}', 'r', encoding='utf-8') as json_file:
                    json_dict: dict = json.load(json_file)
                    joke_type  = json_dict.get('type').replace("'", "''")
                    joke_setup = json_dict.get('setup').replace("'", "''")
                    joke_punch = json_dict.get('punchline').replace("'", "''")
                    # sql below has to be templated 
                    query = f"""INSERT INTO {target} (joke_type, joke_setup, joke_punch) VALUES \
                        ('{joke_type}', '{joke_setup}', '{joke_punch}')"""
                    queries.append(query.strip())
        string_of_queries = "; ".join(queries)
        ti.xcom_push(key='queries', value=f'{string_of_queries};') 

def compile_csv_from_api(ti, target: str, key: str = 'response', task_ids: str = 'get_api'):
    json_dict  = json.loads(ti.xcom_pull(key=key, task_ids=task_ids))
    # violation of DRY
    joke_id    = json_dict.get('id')
    joke_type  = json_dict.get('type').replace("'", "''")
    joke_setup = json_dict.get('setup').replace("'", "''")
    joke_punch = json_dict.get('punchline').replace("'", "''")
    with open(f'{target}/av__csv.csv', 'a', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow((joke_id,joke_type,joke_setup,joke_punch))

# def compile_<...>_from_api(ti, ...) -> ...:
    # ...       
