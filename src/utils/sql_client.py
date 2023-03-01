from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Query
from src.utils.exceptions import ErrorDatabase
from sqlalchemy.schema import MetaData
from os import getenv
from dotenv import load_dotenv
import logging

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base

load_dotenv()

database_name = getenv("DATABASE_NAME", "postgres")
metadata = MetaData(schema="api")
Base = declarative_base(metadata=metadata)
engine = create_engine(
    f"postgresql+pg8000://postgres:postgresql@{database_name}/postgres",
    echo=False,
)


def get_session():

    _session_maker = sessionmaker(bind=engine)
    return _session_maker()


session = get_session()


def get_maximum(modelo):
    resultado = session.query(modelo).all()
    if len(resultado) > 0:
        return resultado[-1]
    return resultado


def update():
    try:
        session.flush()
        session.commit()
    except Exception as e:
        logging.error(str(e))
        raise e


def get(model, id_):
    result = session.query(model).filter(model.id == id_).first()
    if not result:
        raise ErrorDatabase(f"Registro {id_} do tipo {model.__name__} nao encontrado")
    return result


def get_all(modelo):
    return session.query(modelo).all()


def create(instancia):
    try:
        session.add(instancia)
        session.commit()
    except Exception as e:
        logging.error(str(e))
        raise e


def run_query(query: Query):
    return query.with_session(session).all()


def create_schema():
    statements = [
        "create schema api;",
        "create role web_anon nologin;",
    ]
    for statement in statements:
        try:
            with session as s:
                s.execute(statement)
                s.commit()
        # catch any exception
        except (BaseException) as e:
            logging.error(str(e))
            continue


def grant_permissions():
    statements = [
        "grant usage on schema api to web_anon;",
        "grant select on api.alunos to web_anon;",
        "grant insert on api.alunos to web_anon;",
        "grant delete on api.alunos to web_anon;",
        "grant update on api.alunos to web_anon;",
        "grant select on api.courses to web_anon;",
        "grant insert on api.courses to web_anon;",
        "grant delete on api.courses to web_anon;",
        "GRANT ALL ON TABLE api.alunos TO postgres;",
        "GRANT ALL ON TABLE api.alunos TO web_anon;",
        "GRANT ALL ON TABLE api.courses TO postgres;",
        "GRANT ALL ON TABLE api.courses TO web_anon;",
        "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA api TO web_anon;",
        "create role authenticator noinherit login password 'mysecretpassword';",
        "grant web_anon to authenticator;",
    ]
    for statement in statements:
        try:
            with session as s:
                s.execute(statement)
                s.commit()
        # catch any exception
        except (BaseException) as e:
            logging.error(str(e))
            continue


def init_table():
    session.close_all()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
