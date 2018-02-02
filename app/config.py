import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.yeah.net'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    AHU_BLOG_SUBJECT_PREFIX = '[安徽大学博客系统]'
    AHU_BLOG_MAIL_SENDER = 'Blog Admin <ahu_blog@yeah.net>'

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
