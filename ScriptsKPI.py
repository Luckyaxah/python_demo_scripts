"""
计算代码文件的行数
"""


import os
import time
from DBcm import UseDatabase
from DBconfig import dbconfig, rootdir

# rootdir = '/Users/axah/Desktop/tools'
# dbconfig = {'host':'127.0.0.1', 'user': 'axah', 'password': '.', 'database': 'axahDB'}

def log_code_rowcount(dbconfig :dict, CountResult : tuple) -> None:
	with UseDatabase(dbconfig) as cursor:
		_SQL = """insert into log (code_only_num, code_include_comments_num, scripts_num) 
		values (%s, %s, %s)"""
		cursor.execute(_SQL, CountResult)


def countlines(file_path):
		count_code_only = 0
		count_code_include_comments = 0
		for line in open(file_path, encoding='UTF-8'):
			if not len(line.strip()):
				continue
			if not line.strip().startswith('#'):
				count_code_only = count_code_only + 1
			count_code_include_comments = count_code_include_comments +1
			# print(type(line))
		# 	print(line, end = '')
		# print()
		# print(count_code_include_comments)
		# print(count_code_only)
		return count_code_only, count_code_include_comments


def get_code_totalnum(rootdir):

	
	count_code_only_sum = 0
	count_code_include_comments_sum = 0
	scripts_num = 0
	for parent, dirnames, filenames in os.walk(rootdir):
		# for dirname in dirnames:
			# print('parent is' +parent)
			# print('dirname is'+ dirname)
		for filename in filenames:
			if not filename.endswith('.py'):
				continue
			# print('parent is:'+parent)
			# print('filename is:'+filename)
			scripts_num += 1
			print(os.path.join(parent,filename))
			results = countlines(os.path.join(parent,filename))
			count_code_only_sum = results[0]+count_code_only_sum
			count_code_include_comments_sum = results[1]+count_code_include_comments_sum
			print(results)



	# print(count_code_only_sum)
	# print(count_code_include_comments_sum)
	return count_code_only_sum, count_code_include_comments_sum, scripts_num


CountResult = get_code_totalnum(rootdir)
print("代码总行数：",CountResult[:2])
print("代码文件数：",CountResult[2])
print(type(CountResult))
log_code_rowcount(dbconfig, CountResult)

