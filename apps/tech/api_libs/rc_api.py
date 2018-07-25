#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 15:50
# @Author  : Ferras

import pyodbc
import psycopg2


class ModifyRcReportOwner(object):
    """
    Used for RC/GVP
    """
    def __init__(self, report_key, account, version):
        """
        init
        :param report_key: int
        :param account: email
        :param version: rc or gvp
        """
        self.report_key = report_key
        self.account = account
        self.version = version
        self.conn_info = 'Driver={SQL Server};Database=MyDatabase;Server=127.0.0.1;'
        self.report_sql = """
        UPDATE Report
        SET Owner={account}
        WHERE ReportKey={report_key}
        """

    def conn_db(self):
        """
        Connect to database
        :return: cursor
        """
        if self.version.upper() == 'TEST1':
            conn = pyodbc.connect(self.conn_info)
            return conn
        elif self.version.upper() == 'TEST2':
            db_name = 'gvp_rc'
            host = '127.0.0.1'
            port = 5432
            user = 'user'
            password = 'password'
            conn = psycopg2.connect(
                database=db_name, user=user, password=password, host=host,
                port=port
            )
            return conn

    def get_account_key(self):
        """
        Get account key
        :return: data
        """
        conn = self.conn_db()
        cur = conn.cursor()
        account_sql = str()
        if self.version.upper() == 'TEST1':
            account_sql = """
            SELECT AccountKey, AccountName, Email
            FROM dbo.Account
            WHERE Email='{account}'
            """
        elif self.version.upper() == 'TEST2':
            account_sql = """
            SELECT "AccountKey", "AccountName", "Email"
            FROM "Account"
            WHERE "Email"='{account}'
            """

        cur.execute(account_sql.format(account=self.account))
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_report_info(self):
        """
        Get report information
        :return: data
        """
        conn = self.conn_db()
        cur = conn.cursor()
        report_info_sql = str()
        if self.version.upper() == 'TEST!':
            report_info_sql = """
            SELECT r.ReportKey, r.Caption, r.MailTitle, r.Owner, a.AccountName, a.Email
            FROM dbo.Report r
            JOIN dbo.Account a ON r.Owner=a.AccountKey
            WHERE ReportKey={report_key}
            """
        elif self.version.upper() == 'TEST2':
            report_info_sql = """
            SELECT r."ReportKey", r."Caption", r."MailTitle", r."Owner", a."AccountName", a."Email"
            FROM "Report" r
            JOIN "Account" a ON r."Owner"=a."AccountKey"
            WHERE "ReportKey"={report_key}
            """

        sql = report_info_sql.format(report_key=self.report_key)
        print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_report_key(self, report_name):
        """
        Get report key
        :param report_name: string
        :return: data
        """
        conn = self.conn_db()
        cur = conn.cursor()
        report_sql = str()
        if self.version.upper() == 'TEST!':
            report_sql = """
            SELECT r.ReportKey, r.Caption, r.MailTitle, r.Owner, a.AccountName, a.Email
            FROM dbo.Report r
            JOIN dbo.Account a ON r.Owner=a.AccountKey
            WHERE r.Caption = '{report_name}'
            """
        elif self.version.upper() == 'TEST@':
            report_sql = """
            SELECT r."ReportKey", r."Caption", r."MailTitle", r."Owner", a."AccountName", a."Email"
            FROM "Report" r
            JOIN "Account" a ON r."Owner"=a."AccountKey"
            WHERE r."Caption" = '{report_name}'
            """

        cur.execute(report_sql.format(report_name=report_name))
        rows = cur.fetchall()
        return rows

    def modify_report_owner(self):
        """
        Update owner and return
        :return: data
        """
        account = self.get_account_key()[0][0]
        update_report_sql = str()
        if self.version.upper() == 'TEST1':
            update_report_sql = """
            UPDATE Report
            SET Owner={account}
            WHERE ReportKey={report_key}
            """
        elif self.version.upper() == 'TEST2':
            update_report_sql = """
            UPDATE "Report"
            SET "Owner"={account}
            WHERE "ReportKey"={report_key}
            """
        update_report_sql = update_report_sql.format(account=account, report_key=self.report_key)
        conn = self.conn_db()
        cur = conn.cursor()
        cur.execute(update_report_sql)
        conn.commit()

        results = self.get_report_info()
        print(results)
        return results


