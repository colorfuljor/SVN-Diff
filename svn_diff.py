#!/usr/bin/env python
# -*- coding: utf-8 -*-

# time: 2020/6/21
# author: colorful

import sys
import os
import re

def jump(f, n):
    for i in range(0, n):
        f.readline()

class OneFile:
    def __init__(self, lines, file_name):
        self.lines = lines

        self.file_name = file_name
        self.add_list = {}
        self.del_list = {}
        self.upd_list = {}

        # 自动解析
        self._parse()

    def _parse(self):
        del_num = 0
        for line in self.lines:
            if line.startswith('@@'):
                snum, dnum = self._parse_headline(line)
                del_num = 0

            else:
                if line.startswith('-'):
                    # 保存删除的行
                    self.del_list[snum] = line.strip('\n')
                    del_num = del_num + 1
                    #print 'D [%s: %s]:\n  %s' % (self.file_name, snum, line) 

                else:
                    # 计算行号
                    snum = snum - del_num
                    del_num = 0

                    # 保存新增或修改的行
                    if line.startswith('+'): 
                        if self.del_list.has_key(snum):
                            updates = [self.del_list[snum], line.strip('\n')]
                            self.upd_list[snum] = updates
                            del self.del_list[snum]
                            #print 'U [%s: %s]:\n  %s' % (self.file_name, snum, line)
                        else:
                            self.add_list[snum] = line.strip('\n')
                            #print 'A [%s: %s]:\n  %s' % (self.file_name, snum, line)

                snum = snum + 1    

    def _parse_headline(self, line):
        start_num = 0
        diff_num = 0 # 新文件多了就是正数，少了就是负数

        nums = re.findall(r"\d+\.?\d*", line)

        start_num = int(nums[2])
        diff_num = int(nums[3]) - int(nums[1])

        return start_num, diff_num

    def check_change(self, pattern):
        ret = False
        for line_num, lines in self.upd_list.iteritems():
            if not self._compare_line(lines[0], lines[1], pattern):
                ret = True
                print '[%s: %s]: Updated %s\n %s\n %s' % (self.file_name, line_num, pattern, lines[0], lines[1])

        return ret

    def check_del(self, pattern):
        ret = False
        for line_num, line in self.del_list.iteritems():
            if len(re.findall(pattern, line)) > 0:
                ret = True
                print '[%s: %s]: Deleted %s\n %s' % (self.file_name, line_num, pattern, line)

        return ret

    def _compare_line(self, old_line, line, pattern):
        old = re.findall(pattern, old_line)
        new = re.findall(pattern, line)
        if (len(old) != len(new)):
            return False

        ret = True
        for i in range(0, len(old)):
            print old[i], new[i]
            if old[i] != new[i]:
                ret = False 

        return ret

    def check_change_tagid(self):
        ret = False
        for line_num, lines in self.upd_list.iteritems():
            if not self._compare_line_tagid(lines[0], lines[1]):
                ret = True
                print '[%s: %s]: Updated Tagid\n %s\n %s' % (self.file_name, line_num, lines[0], lines[1])

        return ret

    def check_delete_tagid(self):
        ret = False
        for line_num, line in self.del_list.iteritems():
            if len(re.findall(r'tagid=\"\d*\"', line)) > 0:
                ret = True
                print '[%s: %s]: Deleted Tagid\n %s' % (self.file_name, line_num, line)

        return ret

    def _compare_line_tagid(self, old_line, line):
        if not 'tagid' in old_line:
            return True

        old_tagid = re.findall(r'tagid=\"\d*\"', old_line)[0]
        if len(re.findall(r'tagid=\"\d*\"', line)) <= 0:
            return False
        new_tagid = re.findall(r'tagid=\"\d*\"', line)[0]
        print old_tagid, new_tagid

        # 提取其中的数字，并比较
        old_tagid = re.findall(r'\d+\.?\d*', old_tagid)[0]
        new_tagid = re.findall(r'\d+\.?\d*', new_tagid)[0]

        return int(old_tagid) == int(new_tagid)
        

class Diff:
    def __init__(self, file_path):
        self.file_path = file_path

        self.files = {}
        
        # 自动解析
        self._parse()

    def _parse(self):
        with open(self.file_path,'r') as f:
            line = f.readline()
            while line:
                if line.startswith('Index: '):
                    line = line.strip('Index: ').strip('\n')
                    print '--------- [' + line + '] Changed. ---------'

                    # 获取文件名
                    name = line.strip('Index: ').strip('\n')
                    if self.files.has_key(name):
                        print '[ERROR] Duplicate file name.'
                        sys.exit(2)

                    # 跳过几行
                    jump(f, 3)

                    # 获取单文件改变行
                    change_lines = []
                    line = f.readline()
                    while line and not line.startswith('Index: '):
                        change_lines.append(line)
                        line = f.readline()

                    # 进一步解析，并保存
                    self.files[name] = OneFile(change_lines, name)

    def check_change(self, pattern):
        ret = False
        for onefile in self.files.values():
            if onefile.check_change(pattern):
                ret = True

        return ret

    def check_delete(self, pattern):
        ret = False
        for onefile in self.files.values():
            if onefile.check_del(pattern):
                ret = True

        return ret

    def check_change_tagid(self):
        ret = False
        for onefile in self.files.values():
            if onefile.check_change_tagid():
                ret = True

        return ret

    def check_delete_tagid(self):
        ret = False
        for onefile in self.files.values():
            if onefile.check_delete_tagid():
                ret = True

        return ret