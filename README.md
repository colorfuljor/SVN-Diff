# SVN-DIFF 文件解析工具

## 简介

svn-diff 是一个对svn diff文件解析的模块，用于解析SVN diff返回的结果。

## 使用说明

### 模块接入

* svn-diff 是一个对svn diff文件解析的模块，所以需要先将svn diff返回的结果输出到一个文件中（建议使用.diff作为后缀名，方便使用TortoiseSVN打开查看）。然后再使用svn_diff去解析该文件：

```python
import svn_diff

diff = svn_diff.Diff(diff_file) # diff_file为diff文件路径
```

* Diff包含一个字典files，key为file_name，value为OneFile类。
* OneFile类表示一个文件的更改情况，包含三个字典add_list、del_list和upd_list。key都为line_num，value为相应的行（upd_list则保存前后行）。

### 暂时提供接口

#### Diff类

* ```check_change(patten)```：这个接口用于检查一个diff文件中是否有相应的改变，pattern为一个正则表达式。
* 未完待续~

### OneFile 类

* ```check_change(pattern)```：这个接口用于检查修改了的文件中是否有相应的改变，pattern为一个正则表达式。
* ```check_del(pattern)```：这个接口用于检测修改文件张是否删除了包含某种串的行，pattern为一个正则表达式。
* 未完待续~

## 设计说明
### Diff 类
```python
files:{}
	file_name -> OneFile
```

### OneFile 类

```python
file_name: string
add_list:{}
    line_num -> line
del_list:{}
    line_num -> line
upd_list:{}
    line_num -> [old_line, new_line]
```

