___________________________________________________________________________________________
STRUCTURE:

![Screenshot from 2023-11-08 00-47-13](https://github.com/bmaxlw/solid-etl/assets/83329102/4b44b5ac-d7b7-4703-89b7-38501df92958)
___________________________________________________________________________________________
RUN:
1. git clone <repo>
2. mkdir -p ./logs
3. echo -e "AIRFLOW_UID=$(id -u)" > .env
4. docker compose up airflow-init
5. docker compose up
6. docker compose down

___________________________________________________________________________________________
NOTES/TODO:

(1) /var/lib/pgsql/9.4/data/pg_hba.conf to open connections to psql:
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5

(2) host 4 Airflow conn = psql docker container IPV4 (mutable!) (docker inspect)

(3) webserver -> export PYTHONPATH to the root folder
