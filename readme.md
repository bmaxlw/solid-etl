___________________________________________________________________________________________
STRUCTURE:

solid-etl
-> dags
    -> load_postgres.py // DAG to load data from jokes api to psql + csv
    -> ...
-> logs
    -> ...
-> plugins
    -> parsers.py // functions used to parse data sources
    -> compilers.py // functions used to compile source data into targets
    -> helpers.py // functions used as utils
    -> ...
-> data
    -> json // folder to store JSONs, very poor imitation of S3/GCS
    -> csv // folder to store CSVs, very poor imitation of S3/GCS
    -> ...
-> sql
    -> load_postgres // folder to store .sql queries
        -> create_staging_table.sql
        -> create_jokes_table.sql
        -> ...
-> config
    -> load_postgres.yaml // config for load_postgres DAG
    -> ...

___________________________________________________________________________________________
RUN:
git clone <repo>
mkdir -p ./logs
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
docker compose down

___________________________________________________________________________________________
NOTES/TODO:

(1) /var/lib/pgsql/9.4/data/pg_hba.conf to open connections to psql:
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5

(2) host 4 Airflow conn = psql docker container IPV4 (mutable!) (docker inspect)

(3) webserver -> export PYTHONPATH to the root folder
