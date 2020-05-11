"""
将桌面的视频及图片保存到固定目录
"""


import os
import time
from DBcm import UseDatabase
from DBconfig import dbconfig, rootdir


def sort_PicAndVideo(rootdir, newdir):
    for parent, dirnames, filenames in os.walk(rootdir):
        # print(parent)
        # print(filenames)
        if not parent is rootdir:
            continue
        for filename in filenames:
            if filename.endswith('.jpeg') or filename.endswith('.png')  \
                    or filename.endswith('.jpg') or filename.endswith('.mp4') \
                    or filename.endswith('.JPEG') or filename.endswith('.PNG') \
                    or filename.endswith('.JPG') or filename.endswith('.MP4') \
                    or filename.endswith('.MOV'):

                olddirpath = os.path.join(rootdir, filename)
                newdirpath = os.path.join(newdir, filename)
                # print(newdirpath)
                movefile(olddirpath, newdirpath)
            # for dirname in dirnames:
                # print('parent is', parent)
                # print('dirname', dirname)

            # print(parent)


def movefile(olddirpath, newdirpath):
    char = [' ', '(', ')']
    for i in char:
        olddirpath = olddirpath.replace(i, '\\'+i)
        newdirpath = newdirpath.replace(i, '\\'+i)

    # print(olddirpath)
    # print(newdirpath)
    os.system('mv {} {}'.format(olddirpath, newdirpath))


if __name__ == '__main__':
    Rootdir = ['/Users/axah/Desktop/', '/Users/axah/Downloads/']
    # Rootdir = ['/Users/leqi/Desktop/']
    for rootdir in Rootdir:
        fname = "截图" + str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon) \
            + "-" + str(time.localtime().tm_mday)

        ToDir = os.path.join('/Users/axah/work-relevant/', "测试截图", fname)
        if not os.path.isdir(ToDir):
            os.mkdir(ToDir)

        # print(rootdir)
        # print(ToDir)
        sort_PicAndVideo(rootdir, ToDir)
