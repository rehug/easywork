# -*-coding:utf-8-*-
import time
import pyodbc
import psycopg2
import datetime
import re
import pymysql
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

from easywork.settings import DATABASES


class Impala(object):
    def __init__(self, connection_string="DSN=openbi"):
        self.connection_string = connection_string

    def connect(self):
        return pyodbc.connect(self.connection_string, autocommit=True)

    def read(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("set request_pool = \'hadoop-wd\';")
        cursor.execute("set mem_limit = 4GB;")
        cursor.execute(sql)
        data = cursor.fetchall()
        fileds = [x[0] for x in cursor.description]
        return data, fileds

    def insert(self, table_name, fileds, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            template = '''
            INSERT INTO {table_name}({fileds}) values({placeholder})
            '''
            # value_format = '(%s)'% ','.join(['"%s"' % x for x in value])
            sql = template.format(table_name=table_name,
                                  fileds=",".join(fileds),
                                  placeholder=",".join(["?"] * len(fileds)))
            s = time.time()
            try:
                cursor.executemany(sql, data)
                print("Insert take time:", time.time() - s)
            except Exception as e:
                conn.rollback()

    def insert_many_by_one_sql(self, table_name, fileds, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            template = '''
            INSERT INTO {table_name}({fileds}) values{values}
            '''
            sql = template.format(table_name=table_name,
                                  fileds=",".join(fileds),
                                  placeholder=",".join(["?"] * len(fileds)),
                                  values=insert_values_construct(data))
            s = time.time()
            try:
                cursor.execute(sql)
                print("Insert take time:", time.time() - s)
            except Exception as e:
                conn.rollback()

    def insert_by_pandas(self, table_name, fileds, data):
        """暂不可用"""
        conn = self.connect()
        engine = sqlalchemy.create_engine('impala://', creator=conn)
        df = pd.DataFrame(data, columns=fileds)
        s = time.time()
        df.to_sql(name=table_name, con=engine, if_exists='append')
        print("Insert by pandas take time:", time.time() - s)
        conn.close()

    def clear(self, table_name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SHOW CREATE TABLE {table_name}".format(
            table_name=table_name))
        create_tabel_sql = cursor.fetchall()[0][0]
        create_tabel_sql = re.sub("LOCATION.+", "", create_tabel_sql)
        cursor.execute("DROP TABLE {table_name}".format(table_name=table_name))
        cursor.execute(create_tabel_sql)
        conn.close()

    def modify(self, sql):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

    def filter(self, table_name, condition: str):
        """
        根据条件创建第三表
        删除原表
        修改新表名
        """
        temp_table_name = "tech_ba.easy_work_temp"
        create_table_sql = '''
            CREATE TABLE {temp_table_name} as
            SELECT * FROM {table_name} WHERE {condition}
            '''.format(temp_table_name=temp_table_name,
                       table_name=table_name,
                       condition=condition)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS {temp_table_name}".format(
            temp_table_name=temp_table_name))
        conn.commit()
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.execute("DROP TABLE IF EXISTS {table_name}".format(
            table_name=table_name))
        conn.commit()
        cursor.execute("ALTER TABLE {temp_table_name} RENAME TO {table_name}".format(
            temp_table_name=temp_table_name, table_name=table_name))
        conn.commit()
        conn.close()


def insert_values_construct(data):
    def value_convert(x):
        if isinstance(x, (int, float)):
            return str(x)
        else:
            return "'%s'" % str(x)
    values = ["(%s)" % ",".join([value_convert(x) for x in row])
              for row in data]
    values_str = ",".join(values)
    return values_str


class Postgres(object):
    def __init__(self, **kwargs):
        self.setting = kwargs

    def connect(self):
        return psycopg2.connect(**self.setting)

    def read(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        fileds = [x[0] for x in cursor.description]
        return data, fileds

    def create_table(self, table_name, fileds, data):
        pass

    def insert(self, table_name, fileds, data):
        conn = self.connect()
        cursor = conn.cursor()
        template = '''
        INSERT INTO {table_name}({fileds}) values({placeholder})
        '''
        sql = template.format(table_name=table_name,
                              fileds=",".join(fileds),
                              placeholder=",".join(["%s"] * len(fileds)))
        cursor.executemany(sql, data)
        conn.commit()
        conn.close()

    def delete_rows(self, table_name, condition):
        '''删除行'''
        conn = self.connect()
        cursor = conn.cursor()
        template = '''
        DELETE FROM {table_name}
        WHERE {condition}
        '''
        sql = template.format(table_name=table_name,
                              condition=condition
                              )
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def delete_one_day(self, table_name, day: int):
        """因为轮询任务经常需要按天更新，所以定制了一个删除一天数据的SQL"""
        dt = datetime.datetime.strptime(str(day), "%Y%m%d")
        db_day = datetime.datetime.strftime(dt, "%Y-%m-%d")
        condition = "day = '{}'".format(db_day)
        self.delete_rows(table_name=table_name, condition=condition)

    def delete_day(self, table_name, day: int, day_column_name="day"):
        """目标是通用的删除某一天的函数，因为测试时间不够，所以暂时不修改之前的代码"""
        dt = datetime.datetime.strptime(str(day), "%Y%m%d")
        db_day = datetime.datetime.strftime(dt, "%Y-%m-%d")
        condition = "{day_column_name} = '{db_day}'".format(
            day_column_name=day_column_name, db_day=db_day)
        self.delete_rows(table_name=table_name, condition=condition)


class MySqlConn(object):
    """
    Method of mysql.
    """
    def __init__(self):
        self.host = DATABASES['default']['HOST']
        self.port = DATABASES['default']['PORT']
        self.user = DATABASES['default']['USER']
        self.password = DATABASES['default']['PASSWORD']
        self.database = DATABASES['default']['NAME']

    def get_engine(self):
        """
        Connect to mysql and return engine.
        :return: engine
        """
        engine_info = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            self.user, self.password, self.host, self.port, self.database
        )
        print(engine_info)
        _engine = create_engine(engine_info, echo=True)
        return _engine

    def to_db(self, frame, table, flag='append'):
        engine = self.get_engine()
        frame.to_sql(table, con=engine, if_exists=flag, index=False)


