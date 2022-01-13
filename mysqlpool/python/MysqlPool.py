# -*- coding:utf-8 -*-
import pymysql, os
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

class BaseMysqlPool(object):
    def __init__(self, host, port, user, password, dbname):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = dbname
        self.conn = None
        self.cursor = None


class MysqlPool(BaseMysqlPool):
    """
    MYSQL数据库对象，负责产生数据库连接
    此类中的连接采用连接池实现
        获取连接对象: conn = MysqlPool.getConn()
        释放连接对象: conn.close()
    """
    def __init__(self, conf = None):
        self.conf = conf
        super(MysqlPool, self).__init__(**self.conf)
        self.__pool = PooledDB(creator = pymysql,
                              mincached = 1,    # 最少的空闲连接数，如果空闲连接数小于这个数，Pool 自动创建新连接;
                              maxcached = 20,   # 最大的空闲连接数，如果空闲连接数大于这个数，Pool 则关闭空闲连接;
                              host = self.db_host,
                              port = self.db_port,
                              user = self.user,
                              passwd = self.password,
                              db = self.db,
                              use_unicode = False,
                              blocking = True,
                              charset = "utf8",
                              cursorclass = DictCursor,
                              autocommit = True)

    def getConn(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        return self.__pool.connection()

    def getAll(self, sql, param = None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql: 查询 SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        conn = self.getConn()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchall()
        else:
            result = False
        cursor.close()
        conn.close()
        return result

    def getOne(self, sql, param = None):
        """
        @summary: 执行查询，并取出第一条
        @param sql: 查询 SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        conn = self.getConn()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = False
        cursor.close()
        conn.close()
        return result

    def getMany(self, sql, num, param = None):
        """
        @summary: 执行查询，并取出 num 条结果
        @param sql: 查询 SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num: 取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        conn = self.getConn()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchmany(num)
        else:
            result = False
        cursor.close()
        conn.close()
        return result

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql: 要插入 SQL 格式
        @param values: 要插入的记录数据 tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        conn = self.getConn()
        cursor = conn.cursor()
        try:
            count = cursor.executemany(sql, values)
        except Exception as e:
            print("sql exec failed! %s : %s" % (sql, e))
        cursor.close()
        conn.commit()
        conn.close()
        return count

    def __query(self, sql, param = None):
        conn = self.getConn()
        cursor = conn.cursor()
        try:
            if param is None:
                count = cursor.execute(sql)
            else:
                count = cursor.execute(sql, param)
        except Exception as e:
            print("sql exec failed! %s : %s" % (sql, e))
        cursor.close()
        conn.commit()
        conn.close()
        return count

    def update(self, sql, param = None):
        """
        @summary: 更新数据表记录
        @param sql: SQL 格式及条件，使用 (%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def insert(self, sql, param = None):
        """
        @summary: 更新数据表记录
        @param sql: SQL 格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param = None):
        """
        @summary: 删除数据表记录
        @param sql: SQL 格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

'''
USE:

import MysqlPool as mysqlPool

db_config = {}
db_config['host'] = localhost
db_config['port'] = 3306
db_config['user'] = test
db_config['password'] = test
db_config['dbname'] = test

mysql = mysqlPool.MysqlPool(db_config)

'''