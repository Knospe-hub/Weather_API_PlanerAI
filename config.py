import os

"""
config file für die flask app
beinhalten die config für die datenbank
erweiterbar um flask server und allgemeine app configs in verschiedenen dev und deployment umgebungen
verhindert das hardcoden von configs in der app und macht sie austauschbar
"""
class Config:
    SECRETE_KEY = 'super secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///stuff.db'
    ADMIN = 'ADMIN'

    # Root_path_nt = os.environ['PATH'].split(os.pathsep)[0].split("venv")[0]
    # # Root_path = os.environ['PATH'].split(os.pathsep)[0].split("venv")[0]
    # Root_path = os.path.dirname(os.path.abspath(__file__))
    # print(f"cwd: {os.getcwd()}")
    # THREAD_LOG_PATH = Root_path_nt + '/app/logs/processLog.ini'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///dev_stuff.db'
    pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///test_stuff.db'
    pass


class UnitConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///unit_stuff.db'
    pass


config = {
    'development': DevelopmentConfig,
    'testing_app': TestingConfig,
    'unit': UnitConfig
}
