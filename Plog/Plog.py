# 多日志文件的简单实现
import pathlib
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler
import time

class Plog(object):
    """docstring for Plog
    级别       何时使用
    DEBUG     详细信息，典型地调试问题时会感兴趣。
    INFO      证明事情按预期工作。
    WARNING   表明发生了一些意外，或者不久的将来会发生问题（如‘磁盘满了’）。软件还是在正常工作。
    ERROR     由于更严重的问题，软件已不能执行一些功能了。
    CRITICAL  严重错误，表明软件已不能继续运行了。

    """
    formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(levelname)08s] [%(lineno)03s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    formatter2 = logging.Formatter('%(message)s')

    def __init__(self, log_file, level=logging.DEBUG, stream=True, msgOnly=True, overlap=True):
        """
        stream=True, 表示终端也会打印日志
        msgOnly=True  表示只有日志，没有时间信息和日志等级
        overlap  false表示如果存在同名日志文件则会删除原日志，ture表示会在之前的日志后直接追加
        """

        pdir = pathlib.Path(log_file).parent
        if not pdir.exists():
            pathlib.Path.mkdir(pdir,parents=True) # 父文件夹不存在则自动创建。
        self.log_file = log_file
        if not overlap and pathlib.Path(self.log_file).exists():
            pathlib.Path(self.log_file).unlink()
        self.level = level
        self.stream = stream
        self.log_name = str(uuid.uuid1())    # 区分不同日志。

        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.level)

        # 日志文件
        handler = TimedRotatingFileHandler(self.log_file, when='D', encoding="utf-8")
        if msgOnly:
            handler.setFormatter(Plog.formatter2)
        else:
            handler.setFormatter(Plog.formatter)
        self.logger.addHandler(handler)

        # 终端流
        if self.stream:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(Plog.formatter2)
            self.logger.addHandler(streamHandler)


        if overlap:
            self.logger.debug(f"==========***** {time.strftime('%Y-%m-%d %H:%M:%S')} start to log *****==========")

    def __getattr__(self,item):
        return getattr(self.logger,item)

    def log(self, *args):
        """
        临时解决方案。
        因为logger.debug() 有多个参数的时候会报错，不知道如何处理。暂时重写一下debug。
        不知道装饰器能不能解决这个问题，以后遇到新方法再解决。
        """
        msg = " ".join(args)
        self.logger.debug(msg)
