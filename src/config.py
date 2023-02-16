from src.utils.sql_client import SqlClient


conn_internal = SqlClient("postgres")
conn_external = SqlClient("localhost")
