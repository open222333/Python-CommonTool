import sys


class Bar():

    detail_ljust_len = 80  # 進度條 填空長度

    def __init__(self, symbol: str = '=', bar_size: int = 50, **kwargs) -> None:
        """進度條

        title 預設 Progress, 使用 set_title 設定 title

        Args:
            symbol (str, optional): 進度條符號. Defaults to '='.
            bar_size (int, optional): 進度條大小(滿值有多少符號). Defaults to 50.
        """
        '''進度表屬性'''
        self.title = kwargs.get('title', 'Progress')
        self.symbol = symbol
        self.bar_size = bar_size
        # 迴圈內 使用
        self.done_num = kwargs.get('done', 0)

    def set_title(self, title: str):
        """設置標題

        Args:
            title (str): 標題. Defaults to 'Progress'.
        """
        self.title = title

    def print_progress_bar(self, done: int, total: int, decimal: int, detail: str = ''):
        """繪製 進度表

        Args:
            done (int): 已完成數
            total (int): 總任務數
            decimal (int): 百分比顯示到後面幾位
            detail (str): 細節內容
        """
        # 計算百分比（total <= 0 視為已完成，避免除以 0）
        precent = float(round(100 * done / total, decimal)) if total > 0 else 100.0
        done_symbol = int(precent / 100 * self.bar_size)
        left = self.symbol * done_symbol
        right = ' ' * (self.bar_size - done_symbol)
        # 顯示進度條
        bar = f"\r{self.title}:[{left}{right}] {format(precent, f'.{decimal}f')}% {done}/{total} {detail.ljust(self.detail_ljust_len)}"
        return bar

    def done(self):
        print()


class ProgressBar(Bar):

    def __init__(self, symbol: str = '=', bar_size: int = 50, **kwargs) -> None:
        super().__init__(symbol, bar_size, **kwargs)

    def __call__(self, total: int, done: int = 1, decimal: int = 1, in_loop: bool = False, detail: str = None):
        """呼叫進度表

        Args:
            total (int): 總數
            done (int, optional): 已完成. Defaults to 1.
            decimal (int, optional): 顯示小數位. Defaults to 1.
            in_loop (bool, optional): 建立的實體是否在迴圈內使用. Defaults to False.
        """
        if in_loop:
            self.done_num += done
            if self.done_num >= total:
                self.done_num = total
            if detail:
                bar = self.print_progress_bar(self.done_num, total, decimal, detail)
            else:
                bar = self.print_progress_bar(self.done_num, total, decimal)
            sys.stdout.write(bar)
            sys.stdout.flush()
            if self.done_num == total:
                self.done()
        else:
            count = 0
            while True:
                count += done
                if count >= total:
                    count = total
                bar = self.print_progress_bar(count, total, decimal)
                sys.stdout.write(bar)
                sys.stdout.flush()
                if count == total:
                    break
            self.done()


class MultiProgressBar(Bar):
    """同時顯示多條進度條（每條一行，原地更新）。

    範例：
        bars = MultiProgressBar()
        a = bars.add_progress('下載', total=100)
        b = bars.add_progress('解壓', total=50)
        bars.update(a)          # 進度 +1
        bars.update(b, done=5)  # 進度 +5
        bars.done()
    """

    def __init__(self, symbol: str = '=', bar_size: int = 50) -> None:
        super().__init__(symbol, bar_size)
        self.progress = []
        self._printed = False

    def add_progress(self, title: str, total: int, decimal: int = 1) -> int:
        """新增一條進度條，回傳其索引（供 update 使用）。"""
        self.progress.append({"title": title, "total": total, "decimal": decimal, "done": 0, "detail": ''})
        return len(self.progress) - 1

    def update(self, index: int, done: int = 1, detail: str = ''):
        """將第 index 條進度條增加 done，並重新繪製全部進度條。"""
        p = self.progress[index]
        p['done'] = min(p['done'] + done, p['total'])
        if detail:
            p['detail'] = detail
        self.render()

    def render(self):
        if self._printed:
            # 游標上移回到第一條進度條
            sys.stdout.write(f"\x1b[{len(self.progress)}F")
        for p in self.progress:
            self.title = p['title']
            line = self.print_progress_bar(p['done'], p['total'], p['decimal'], p['detail'])
            sys.stdout.write(line.lstrip('\r') + '\n')
        sys.stdout.flush()
        self._printed = True

    def done(self):
        pass


# 舊名稱相容（拼字錯誤），請改用 MultiProgressBar
MutliProgressBar = MultiProgressBar
