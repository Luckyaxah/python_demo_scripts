"""
获取手机参数
"""


# -*- coding: UTF-8 -*-
import os
from DBconfig import dbconfig
from DBcm import UseDatabase
# os.system 只能看到命令的返回结果，得不到命令的值
# PhoneProp = os.system("adb shell getprop")

# os.popen

# def PhoneManager(dbconfig:dict, DevicePropDict:dict ) -> None:
# 	with UseDatabase(dbconfig) as cursor:
# 		_SQL = """ insert into PhoneManager() 
# 		"""

PropList = [
		'ro.product.name',
		'ro.product.brand', # 设备厂商
		'ro.build.version.release', # 设备Android系统版本号
		'ro.product.model', # sd卡状态
		'ro.build.characteristics',
		'ro.build.version.sdk',
		'ro.product.manufacturer',
		'ro.product.board',
		'ro.build.version.incremental', # 对于小米手机会记录MIUI的版本号
		'ro.serialno', # 设备ID 序列号 这个作为主键
		'DeviceResolution',# 分辨率

		]

DevicePropDict = {prop : os.popen("adb shell getprop {}".format(prop)).readlines()[0][:-1] for prop in (PropList) if prop.startswith('ro.')} 
DevicePropDict['DeviceResolution'] = os.popen("adb shell wm size").readlines()[0].split()[2]

DeviceProp = [DevicePropDict[key] for key in PropList]

print(DeviceProp)
print(DevicePropDict)

