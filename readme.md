# 一个简单的Python日志封装类。

优点：极简、多日志、按天生成日志、日志覆盖与否可选，日志格式多样化


 ## 如何安装
 
 [这里有关于setup.py编写的详细说明](https://blog.konghy.cn/2018/04/29/setup-dot-py/)

 ```bash
 python setup.py install
 ```

 ## 如何使用
 
 ```python
from Plog import Plog

log1 = Plog("log1.txt")
log1.log('hello','world') #多个参数请用这个

log2 = Plog("log2.txt",stream=True, msgOnly=False, overlap=False) #overlap为False的时候，每次运行时有同名日志文件存在就会删除
log2.debug('hello','world') # 如果有多个参数这个会报错，
log2.debug('hello') # 单个参数的时候和log2.log('hello')是一样的。
log2.info('world') # 

 ```
