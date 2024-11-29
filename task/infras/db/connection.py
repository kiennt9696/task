from flask import Flask
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self) -> None:
        self.__engine: None
        self.session = None

    def init_app(self, app: Flask):
        self.__engine = self.__create_database_engine(app.config.get("DB_URI"))
        self.__enter__()

    def __create_database_engine(self, db_uri) -> Engine:
        engine = create_engine(db_uri)
        return engine

    def get_engine(self) -> Engine:
        return self.__engine

    def __enter__(self):
        Session = sessionmaker(bind=self.__engine)
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
