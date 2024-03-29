from configparser import ConfigParser
import os


config = ConfigParser()
config.read(os.path.join('conf', 'configig.ini'))


# logs相關參數
# 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
LOG_DISABLE = config.getboolean('LOG', 'LOG_DISABLE', fallback=False)
# logs路徑 預設 logs
LOG_PATH = config.get('LOG', 'LOG_PATH', fallback='logs')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = config.get('LOG', 'LOG_LEVEL', fallback='WARNING')
# 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 不關閉
LOG_FILE_DISABLE = config.getboolean('LOG', 'LOG_FILE_DISABLE', fallback=False)
# 指定log大小(輸入數字) 單位byte, 與 LOG_DAYS 只能輸入一項 若都輸入 LOG_SIZE優先
LOG_SIZE = config.getint('LOG', 'LOG_SIZE', fallback=0)
# 指定保留log天數(輸入數字) 預設7
LOG_DAYS = config.getint('LOG', 'LOG_DAYS', fallback=7)

if not LOG_FILE_DISABLE:
    # 建立log資料夾
    if not os.path.exists(LOG_PATH) and not LOG_DISABLE:
        os.makedirs(LOG_PATH)
