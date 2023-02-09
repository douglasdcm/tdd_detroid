from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Query
from src.utils.exceptions import ErroBancoDados
from sqlalchemy.schema import MetaData

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base
# https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base

metadata = MetaData(schema="api")
Base = declarative_base(metadata=metadata)


class SqlClient:
    def __init__(self, nome_banco) -> None:
        self._engine = create_engine(
            "postgresql+pg8000://postgres:postgresql@localhost/postgres",
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
            "grant select on all tables in schema api to web_anon;",
            "grant insert on all tables in schema api to web_anon;",
            "grant delete on all tables in schema api to web_anon;",
            "grant update on all tables in schema api to web_anon;",
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
        self.drop_views()
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.create_views()

    def drop_views(self):
        statement = "DROP VIEW IF EXISTS api.view_course_and_discipline;"
        try:
            with self._session as s:
                s.execute(statement)
                s.commit()
        except:
            raise ErroBancoDados("Could not delete the views.")

    def create_views(self):
        statement = """
        CREATE VIEW api.view_course_and_discipline AS
        SELECT *
        FROM api.materias
        GROUP BY curso_id, id;
        """
        try:
            with self._session as s:
                s.execute(statement)
                s.commit()
        except:
            raise ErroBancoDados("Could not create the views.")

    def roda_query(self, query: Query):
        return query.with_session(self._session).all()

    def confirma(self):
        self._session.commit()

    def lista_tudo(self, modelo):
        return self._session.query(modelo).all()

    def lista(self, modelo, id_):
        resultado = self._session.query(modelo).filter(modelo.id == id_).first()
        if not resultado:
            raise ErroBancoDados(
                f"Registro {id_} do tipo {modelo.__name__} nao encontrado"
            )
        return resultado

    def cria(self, instancia):
        self._session.add(instancia)
        self._session.commit()
