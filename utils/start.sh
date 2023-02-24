BASE_DIR="/webapp"
# start the database
python ${BASE_DIR}/cli.py init-bd
# start the server
python ${BASE_DIR}/app.py
