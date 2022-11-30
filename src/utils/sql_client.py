from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Query
from src.utils.exceptions import ErroBancoDados

Base = declarative_base()


class SqlClient:
    def __init__(self, nome_banco) -> None:
        self._engine = create_engine(f"sqlite:///{nome_banco}", echo=False)
        _session_maker = sessionmaker(bind=self._engine)
        self._session = _session_maker()

    def update(self):
        self._session.flush()
        self._session.commit()

    def lista_maximo(self, modelo):
        resultado = self._session.query(modelo).all()
        if len(resultado) > 0:
            return resultado[-1]
        return resultado

    def inicializa_tabela(self, modelo):
        Base.metadata.create_all(self._engine)
        resultado = self._session.query(modelo).all()
        for instance in resultado:
            self._session.delete(instance)
            self._session.flush()
            self._session.commit()

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
