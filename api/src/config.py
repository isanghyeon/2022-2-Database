import os
import pymysql.cursors

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'DB-Project'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qwer1234!@localhost:20001/db_shop?charset=utf8"
    # SQLALCHEMY_BINDS = {
    #     "CVELIST": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVELIST.db")}',
    #     "TASK_MANAGER": f'sqlite:///{os.path.join(BASE_PATH, "databases/TASK_MANAGER.db")}'
    # }
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        pass


class Developments_config(Config):
    """
        Flask Config for Development
    """
    DEBUG = True
    TESTING = True
    ERROR_404_HELP = True


class Production_config(Config):
    """
        Flask Config for Production
    """
    DEBUG = False
    TESTING = False
    ERROR_404_HELP = False
