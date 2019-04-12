import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    EXPLAIN_TEMPLATE_LOADING = True
    CACHE_TYPE = "null"
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/lc1012019'
    SQLALCHEMY_ECHO = True
    THREADS_PER_PAGE = 2
    CSRF_ENABLED     = True
    CSRF_SESSION_KEY = b'!\xe6\xa6\xa3_?\x9e+2`>\xfa\x04\x10\x08w'
    SECRET_KEY = b'1\x19\xca0\\\xe7\x84X\xb3\x03d/tR\x14\x88'