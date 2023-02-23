from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Query
from src.utils.exceptions import ErroBancoDados
from sqlalchemy.schema import MetaData
from config import DATABASE_NAME

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base

metadata = MetaData(schema="api")
Base = declarative_base(metadata=metadata)


def get_session():
    engine = create_engine(
        f"postgresql+pg8000://postgres:postgresql@{DATABASE_NAME}/postgres",
        echo=False,
    )
    _session_maker = sessionmaker(bind=engine)
    return _session_maker()


session = get_session()


def list_maximum(modelo):
    resultado = session.query(modelo).all()
    if len(resultado) > 0:
        return resultado[-1]
    return resultado


def update():
    session.flush()
    session.commit()


def get(model, id_):
    result = session.query(model).filter(model.id == id_).first()
    if not result:
        raise ErroBancoDados(f"Registro {id_} do tipo {model.__name__} nao encontrado")
    return result


def get_all(modelo):
    return session.query(modelo).all()


def create(instancia):
    session.add(instancia)
    session.commit()


def run_query(query: Query):
    return query.with_session(session).all()


class SqlClient:
    def __init__(self, nome_banco=None) -> None:
        self._engine = create_engine(
            f"postgresql+pg8000://postgres:postgresql@{DATABASE_NAME}/postgres",
            echo=False,
        )
        _session_maker = sessionmaker(bind=self._engine)
        self._session = _session_maker()

    def create_schema(self):
        statements = [
            "create schema api;",
            "create role web_anon nologin;",
        ]
        for statement in statements:
            try:
                with self._session as s:
                    s.execute(statement)
                    s.commit()
            # catch any exception
            except:
                continue

    def grant_permissions(self):
        statements = [
            "grant usage on schema api to web_anon;",
            "grant select on api.alunos to web_anon;",
            "grant insert on api.alunos to web_anon;",
            "grant delete on api.alunos to web_anon;",
            "grant update on api.alunos to web_anon;",
            "grant select on api.cursos to web_anon;",
            "grant insert on api.cursos to web_anon;",
            "grant delete on api.cursos to web_anon;",
            "GRANT ALL ON TABLE api.alunos TO postgres;",
            "GRANT ALL ON TABLE api.alunos TO web_anon;",
            "GRANT ALL ON TABLE api.cursos TO postgres;",
            "GRANT ALL ON TABLE api.cursos TO web_anon;",
            "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA api TO web_anon;",
            "create role authenticator noinherit login password 'mysecretpassword';",
            "grant web_anon to authenticator;",
        ]
        for statement in statements:
            try:
                with self._session as s:
                    s.execute(statement)
                    s.commit()
            # catch any exception
            except:
                continue

    def update(self):
        with self._session as s:
            s.flush()
            s.commit()

    def lista_maximo(self, modelo):
        resultado = self._session.query(modelo).all()
        if len(resultado) > 0:
            return resultado[-1]
        return resultado

    def init_table(self, modelo):
        self._session.close_all()
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def run_query(self, query: Query):
        return query.with_session(self._session).all()

    def confirma(self):
        self._session.commit()

    def get_all(self, modelo):
        return self._session.query(modelo).all()

    def get(self, modelo, id_):
        resultado = self._session.query(modelo).filter(modelo.id == id_).first()
        if not resultado:
            raise ErroBancoDados(
                f"Registro {id_} do tipo {modelo.__name__} nao encontrado"
            )
        return resultado

    def create(self, instancia):
        self._session.add(instancia)
        self._session.commit()
