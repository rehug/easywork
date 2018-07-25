#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 15:08
# @Author  : Ferras

import psycopg2

from apps.easy_jobs.common.dbsetting import gvp_projects


class ReadGvpPSql(object):
    """
    Show postgresql tables or return data from a table.
    """
    def __init__(self, table_name=''):
        """
        init
        :param table_name: table name
        """
        self.table_name = table_name

    def psql_conn(self):
        """
        connect to psql
        :return: cursor
        """
        dbname = gvp_projects.get('dbname')
        host = gvp_projects.get('host')
        port = gvp_projects.get('port')
        user = gvp_projects.get('user')
        password = gvp_projects.get('password')
        conn = psycopg2.connect(
                database=dbname, user=user, password=password, host=host,
                port=port)
        cur = conn.cursor()
        return cur

    def show_tables(self):
        """
        show psql tables
        :return:
        """
        cur = self.psql_conn()
        cur.execute('SELECT tablename FROM pg_tables;')
        rows = cur.fetchall()
        return rows

    def read_psql(self, _limit=10):
        """
        Return data from a table, default last 10 lines.
        :param _limit:
        :return:
        """
        cur = self.psql_conn()
        sql = '''
        select day, count(*)
        from %s
        group by day
        order by day desc
        limit %s;
        ''' % (self.table_name, _limit)
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
