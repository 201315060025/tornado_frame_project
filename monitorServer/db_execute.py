# encoding: utf-8
"""
数据库操作
"""
import pymysql
from logger import log
from config import Config
from tools import cur_time



class DbExecute(object):
    def __init__(self ):
        self._ip = Config.ip
        self._name = Config.name
        self._pwd = Config.pwd
        self._database = Config.database
        self._table = Config.table
        self.cursor = None
        self.db = None
        self._init_obj()

    def _init_obj(self):
        """生命一个执行者"""
        if self.cursor is None:
            db = pymysql.connect(user=self._name, passwd=self._pwd, db=self._database, host=self._ip)
            cur = db.cursor()
            self.cursor = cur
            self.db = db

    def generate_table(self):
        """生成表"""

        pass

    def insert(self, *args)->bool:
        sql = """insert into {}(TIME,mem_free,mem_total,mem_percent,mem_used,cpu,disk1,disk2,disk3,disk4,disk5) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(
            self._table)
        try:
            val = (cur_time(),) + args[0]
            self.cursor.execute(sql, val)
            self.db.commit()
            return True
        except Exception as e:
            log.warning(f"insert data fail and source data = {sql}, {str(e)}")
            self.cursor.close()
            self.db.close()
            return False



if __name__ == '__main__':
    from job.systemJob import SystemJob
    data = SystemJob().do()
    db_exe = DbExecute()
    res = db_exe.insert(data)
    print(res)