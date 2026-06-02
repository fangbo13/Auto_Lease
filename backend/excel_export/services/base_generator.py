from abc import ABC, abstractmethod


class BaseExcelGenerator(ABC):
    """Excel 生成器抽象基类。"""

    @abstractmethod
    def generate(self, lease_input, calculation_result) -> bytes:
        """
        生成 Excel 文件并返回字节流。

        Args:
            lease_input: LeaseInput 实例
            calculation_result: CalculationResult 实例

        Returns:
            bytes: Excel 文件字节流
        """
        pass
