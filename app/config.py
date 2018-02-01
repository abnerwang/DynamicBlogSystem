import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'some hard guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    def init_app(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wxp12345@localhost/dynamic_blog_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wxp12345@localhost/dynamic_blog_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wxp12345@localhost/dynamic_blog'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
