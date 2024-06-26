# from . import LOG_PATH, LOG_LEVEL, LOG_DISABLE, LOG_FILE_DISABLE, LOG_SIZE, LOG_DAYS
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from traceback import print_exc
from datetime import datetime
import logging
import socket
import os


'''
; ******log設定******
; 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
; LOG_DISABLE=1

; logs路徑 預設 logs
; LOG_PATH=

; 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 不關閉
; LOG_FILE_DISABLE=1

; 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
; LOG_LEVEL=

; 指定log大小(輸入數字) 單位byte, 與 LOG_DAYS 只能輸入一項 若都輸入 LOG_SIZE優先
; LOG_SIZE=

; 指定保留log天數(輸入數字) 預設7
; LOG_DAYS=
'''


class Log():

    def __init__(self, log_name: str = None) -> None:
        """
        Args:
            log_name (str, optional): logger名稱. Defaults to 主機名稱.
        """
        if log_name:
            self.log_name = log_name
        else:
            self.log_name = socket.gethostname()

        self.log_path = 'logs'
        self.logfile_name = None

        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(logging.WARNING)

        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_log_path(self, log_path: str):
        """設置log檔存放位置

        Args:
            log_path (str): 路徑 預設為 logs
        """
        self.log_path = log_path

    def set_log_file_name(self, name: str):
        """設置log檔名稱 預設為 主機名稱.log

        Args:
            name (str): 名稱
        """
        self.logfile_name = name

    def set_date_handler(self, amount: int = 3, when: str = 'D') -> TimedRotatingFileHandler:
        """設置每日log檔

        Args:
            `amount` (int, optional): 保留檔案數量. Defaults to 3.\n
            `when` (str, optional): S - Seconds, M - Minutes, H - Hours, D - Days., Defaults to 'D'.

        Returns:
            TimedRotatingFileHandler: _description_
        """
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        def my_namer(default_name: str):
            """替換 TimedRotatingFileHandler namer

            [TimedRotatingFileHandler Changing File Name?](https://stackoverflow.com/questions/338450/timedrotatingfilehandler-changing-file-name)\n

            Args:
                default_name (str): _description_

            Returns:
                _type_: _description_
            """
            base_filename, ext, date = default_name.split(".")
            return f"{base_filename}.{date}.{ext}"

        # 當前
        if when == 'S':
            date_format = '%Y-%m-%d_%H-%M-%S'
        elif when == 'M':
            date_format = '%Y-%m-%d_%H-%M'
        elif when == 'H':
            date_format = '%Y-%m-%d_%H'
        elif when == 'D' or when == 'MIDNIGHT':
            date_format = '%Y-%m-%d'

        if not self.logfile_name:
            self.logfile_name = self.log_name

        self.now_time = datetime.now().__format__(date_format)
        self.log_file = os.path.join(self.log_path, f'{self.logfile_name}')
        handler = TimedRotatingFileHandler(
            self.log_file, when=when, backupCount=amount)
        handler.namer = my_namer
        handler.setFormatter(self.formatter)
        if self.has_handler(handler) == False:
            self.logger.addHandler(handler)

    def set_file_handler(self, size: int = 1 * 1024 * 1024, file_amount: int = 1) -> RotatingFileHandler:
        """設置log檔案大小限制

        Args:
            log_file (_type_): log檔名
            size (int, optional): 檔案大小. Defaults to 1*1024*1024 (1M).
            file_amount (int, optional): 檔案數量. Defaults to 1.

        Returns:
            RotatingFileHandler: _description_
        """
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        if not self.logfile_name:
            self.logfile_name = self.log_name

        self.log_file = os.path.join(self.log_path, f'{self.logfile_name}')
        handler = RotatingFileHandler(
            self.log_file, maxBytes=size, backupCount=file_amount)
        handler.setFormatter(self.formatter)
        if self.has_handler(handler) == False:
            self.logger.addHandler(handler)

    def set_msg_handler(self) -> logging.StreamHandler:
        """設置log steam

        Returns:
            logging.StreamHandler: _description_
        """
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        if self.has_handler(handler) == False:
            self.logger.addHandler(handler)

    def set_log_formatter(self, formatter: str):
        """設置log格式 formatter

        %(asctime)s - %(name)s - %(levelname)s - %(message)s

        Args:
            formatter (str): log格式.
        """
        self.formatter = logging.Formatter(formatter)

    def set_level(self, level: str = 'WARNING'):
        """設置log等級

        Args:
            level (str): 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
        """
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)

    def has_handler(self, handler):
        """是否 已存在handler

        Args:
            handler (_type_): _description_

        Returns:
            _type_: _description_
        """
        for h in self.logger.handlers:
            if isinstance(h, type(handler)):
                return True
        return False

    def disable_log(self):
        """關閉log
        """
        logging.disable()

    def debug(self, message: str, exc_info: bool = False):
        self.logger.debug(message, exc_info=exc_info)

    def info(self, message: str, exc_info: bool = False):
        self.logger.info(message, exc_info=exc_info)

    def warning(self, message: str, exc_info: bool = False):
        self.logger.warning(message, exc_info=exc_info)

    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        self.logger.critical(message, exc_info=exc_info)


class BasicLogClass():

    def __init__(self, log_name: str = 'BasicLog', **kwargs) -> None:
        log_level = kwargs.get('log_level')
        self.logger = Log(log_name)
        if log_level != None:
            self.logger.set_level(log_level.upper())
