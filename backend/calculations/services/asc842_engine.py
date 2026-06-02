from decimal import Decimal
from calculations.services.ifrs16_engine import IFRS16Engine


class ASC842Engine(IFRS16Engine):
    """ASC 842 计算引擎（目前与 IFRS 16 逻辑基本一致，可扩展短期租赁豁免等差异）。"""

    def calculate(self):
        # 目前复用 IFRS 16 逻辑，后续可添加 ASC 842 特有处理
        return super().calculate()
