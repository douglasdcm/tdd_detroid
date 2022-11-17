from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Query

Base = declarative_base()


class ErroBancoDados(Exception):
    pass


class SqlClient:
    def __init__(self, nome_banco) -> None:
        _engine = create_engine(f"sqlite:///{nome_banco}", echo=False)
        Base.metadata.create_all(_engine)
        _session_maker = sessionmaker(bind=_engine)
        self._session = _session_maker()

    def lista_maximo(self, modelo):
        resultado = self._session.query(modelo).all()
        if len(resultado) > 0:
            return resultado[-1]
        return resultado

    def deleta_tabela(self, modelo):
        resultado = self._session.query(modelo).all()
        for instance in resultado:
            self._session.delete(instance)
            self._session.flush()
            self._session.commit()

    def conta(self, query_livre: Query):
        return query_livre.with_session(self._session).count()

    def roda_query(self, query_livre: Query):
        return query_livre.with_session(self._session).all()

    def lista_tudo(self, modelo):
        return self._session.query(modelo).all()

    def lista(self, modelo, id_):
        return self._session.query(modelo).filter(modelo.id == id_).first()

    def cria(self, instancia):
        self._session.add(instancia)
        self._session.commit()
