import os
import pymysql as dbapi
from pymysql.constants import CLIENT


class InitDBMSCredsException(Exception):
    pass


class NumberPlusOneExists(Exception):
    pass


class NumberExists(Exception):
    pass


class DBHandler:
    sql_init_query = '''
        CREATE TABLE IF NOT EXISTS numbs (
           indx INT AUTO_INCREMENT PRIMARY KEY,
            num INT UNIQUE
        ) ENGINE=INNODB;
        TRUNCATE TABLE numbs;
    '''

    def __init__(self):
        self.__dbms_ip = os.environ.get('DBMS_IP')
        self.__dbms_port = os.environ.get('DBMS_PORT')
        self.__dbms_user = os.environ.get('DBMS_USER')
        self.__dbms_pass = os.environ.get('DBMS_PASS')

        if self.__dbms_ip is None or self.__dbms_port is None or self.__dbms_user is None or self.__dbms_pass is None:
            raise InitDBMSCredsException('Initialization of DBMS was failed')

        try:
            self.__dbms_port = int(self.__dbms_port)
            self.execute(
                DBHandler.sql_init_query, commit=True
            )
        except Exception as e:
            raise InitDBMSCredsException('Incorrect creds to DBMS', e)

    def get_conn_and_cur(self):
        connection = dbapi.connect(
            host=self.__dbms_ip,
            port=self.__dbms_port,
            user=self.__dbms_user,
            password=self.__dbms_pass,
            db='mysql',
            client_flag=CLIENT.MULTI_STATEMENTS
        )
        cur = connection.cursor()
        return connection, cur

    def execute(self, query, args=(), commit=False):
        conn, cur = self.get_conn_and_cur()
        result = None
        try:
            cur.execute(query, args)
            result = cur.fetchall()
            if commit:
                conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

        return result

    def exist_in_db(self, numb):
        return bool(self.execute('SELECT num FROM numbs WHERE num=%s', [numb]))

    def insert_numb(self, numb):
        query = 'INSERT INTO numbs (num) VALUES (%s)'
        self.execute(query, [numb], True)
