# Python-CommonTool

Python 常用工具模組集合，包含 Log 封裝（logger）與 CLI 進度條（progress_bar），可作為其他 Python 專案的共用工具模組直接引入使用。

---

## 目錄

- [專案概覽](#專案概覽)
- [模組說明](#模組說明)
- [執行流程](#執行流程)
- [使用方法](#使用方法)
- [設定檔說明](#設定檔說明)
- [建議注意事項](#建議注意事項)

---

## 專案概覽

```
Python-CommonTool/
├── src/
│   ├── logger.py           # Log 封裝模組（Log、BasicLogClass）
│   └── progress_bar.py     # CLI 文字進度條
└── conf/
    └── config.ini.default  # 設定檔範本
```

本模組設計為被其他專案引入使用，不含獨立的執行入口（`main.py`）。

---

## 模組說明

### src/logger.py

基於 Python 標準 `logging` 模組的封裝，提供以下功能：

| 方法 | 說明 |
|---|---|
| `set_msg_handler()` | 輸出 log 至終端機（StreamHandler） |
| `set_file_handler(size, file_amount)` | 輸出至檔案並依大小輪換，預設 1MB / 1 個備份 |
| `set_date_handler(amount, when)` | 輸出至檔案並依時間輪換（S/M/H/D），預設每天保留 3 份 |
| `set_level(level)` | 設定 log 等級：DEBUG / INFO / WARNING / ERROR / CRITICAL |
| `set_log_path(log_path)` | 設定 log 存放目錄，預設 `logs/` |
| `set_log_file_name(name)` | 設定 log 檔名稱，預設使用 logger 名稱 |
| `set_log_formatter(formatter)` | 自訂 log 輸出格式 |
| `disable_log()` | 停用全部 log 輸出 |

**Log 等級方法：**

```python
logger.debug(message, exc_info=False)
logger.info(message, exc_info=False)
logger.warning(message, exc_info=False)
logger.error(message, exc_info=False)
logger.critical(message, exc_info=False)
```

**BasicLogClass：** 可作為基底類別繼承，省略手動初始化 logger 的步驟。

### src/progress_bar.py

純文字 CLI 進度條，適用於批次處理任務的終端機進度顯示，無需額外相依套件。

---

## 執行流程

```
引用模組
  └─ from src.logger import Log

初始化 logger
  └─ logger = Log('APP_NAME')

設定 log 等級
  └─ logger.set_level('INFO')

設定輸出方式（可同時設定多種）
  ├─ logger.set_msg_handler()          → 控制台輸出
  ├─ logger.set_file_handler()         → 檔案輸出（大小輪換）
  └─ logger.set_date_handler()         → 檔案輸出（天數輪換）

使用 logger 記錄訊息
  └─ logger.info('訊息')
```

---

## 使用方法

### 基本使用（控制台輸出）

```python
from src.logger import Log

logger = Log('MY_APP')
logger.set_level('INFO')
logger.set_msg_handler()    # 輸出至控制台

logger.debug('除錯訊息')
logger.info('一般訊息')
logger.warning('警告訊息')
logger.error('錯誤訊息', exc_info=True)
logger.critical('嚴重錯誤訊息')
```

### 同時輸出至控制台與檔案（大小輪換）

```python
from src.logger import Log

logger = Log('MY_APP')
logger.set_level('DEBUG')
logger.set_log_path('logs')
logger.set_log_file_name('my_app')

logger.set_msg_handler()                    # 控制台輸出
logger.set_file_handler(                    # 檔案輸出（大小輪換）
    size=5 * 1024 * 1024,                   # 5MB
    file_amount=3                           # 保留 3 個備份
)

logger.debug('除錯訊息')
```

### 依天數輪換 log 檔

```python
from src.logger import Log

logger = Log('MY_APP')
logger.set_level('INFO')
logger.set_date_handler(amount=7, when='D') # 保留 7 天，每天輪換
logger.set_msg_handler()

logger.info('每日輪換 log')
```

### 作為基底類別使用（BasicLogClass）

```python
from src.logger import BasicLogClass

class MyClass(BasicLogClass):
    def __init__(self):
        super().__init__('MyClass', log_level='DEBUG')

    def run(self):
        self.logger.info('執行中')
```

### 引入進度條模組

```python
from src.progress_bar import ProgressBar

bar = ProgressBar(total=100)
for i in range(100):
    bar.update(i + 1)
```

---

## 設定檔說明

### conf/config.ini（從 config.ini.default 複製）

```ini
[LOG]
; 關閉 log 功能（true / True / 1），預設不關閉
; LOG_DISABLE=

; log 檔存放路徑，預設 logs
; LOG_PATH=

; 關閉記錄 log 檔案（true / True / 1），預設不關閉
; LOG_FILE_DISABLE=

; log 等級：DEBUG / INFO / WARNING / ERROR / CRITICAL，預設 WARNING
; LOG_LEVEL=

; 指定 log 檔案大小（單位 byte），與 LOG_DAYS 擇一；若同時設定，LOG_SIZE 優先
; LOG_SIZE=

; 指定保留 log 天數，預設 7
; LOG_DAYS=7
```

---

## 建議注意事項

- `Log` 類別預設 log 等級為 `WARNING`，若要看到 `DEBUG` 或 `INFO` 訊息，需明確呼叫 `set_level()`。
- `set_file_handler()` 與 `set_date_handler()` 可擇一使用；若同時呼叫，兩個 handler 都會被加入，log 會同時寫入兩種輪換規則的檔案。
- `has_handler()` 會檢查是否已存在相同類型的 handler，避免重複加入導致 log 訊息重複輸出。
- log 檔案目錄不存在時會自動建立（`os.makedirs`），無需手動建立 `logs/` 資料夾。
- `exc_info=True` 參數可在 log 訊息中附加完整的 traceback，建議在 `error()` 或 `critical()` 呼叫時使用。
- `LOG_SIZE` 與 `LOG_DAYS` 為互斥設定，同時填寫時以 `LOG_SIZE` 為準。
- 建議在正式環境將 `LOG_LEVEL` 設為 `INFO` 或 `WARNING`，避免 `DEBUG` 等級產生大量日誌。
