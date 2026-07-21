"""
PyMySQL shim — makes Django use pure-Python MySQL driver transparently.

This is required on shared hosting (e.g. o2switch) where compiling
the C-based mysqlclient extension may not be available.
PyMySQL implements the same DB-API 2.0 interface as MySQLdb.
"""
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass
