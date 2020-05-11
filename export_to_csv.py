"""
导出为csv
"""

from DBcm import UseDatabase
import os
import pandas as pd
from DBconfig import dbconfig
# 导出csv
# dbconfig = {'host':'127.0.0.1', 'user': 'axah', 'password': '', 'database': 'axah'}

def db2csv(dbconfig):
	with UseDatabase(dbconfig) as cursor:
		_SQL = """select * from log"""
		cursor.execute(_SQL)
		res = cursor.fetchall()
		print(type(res))
		print(res)

		CSV_columnName =['id','time','code_only_num','code_include_comments_num','scripts_num']
		test = pd.DataFrame(columns = CSV_columnName, data = res)
		print(test)
		test.to_csv('/Users/axah/Desktop/tools/log.csv', encoding = 'gbk')

db2csv(dbconfig)

