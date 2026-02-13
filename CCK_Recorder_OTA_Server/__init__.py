try:
    import pymysql

    pymysql.install_as_MySQLdb()
except Exception:
    # Linux/production may use mysqlclient directly.
    pass
