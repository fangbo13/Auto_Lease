from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractAIParser(ABC):
    """AI 解析器抽象基类，所有具体解析器必须实现此接口。"""

    @abstractmethod
    def parse(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        """
        解析合同文件，提取租赁关键信息。

        Args:
            file_path: 文件本地路径
            mime_type: 文件 MIME 类型

        Returns:
            dict: 标准化解析结果，包含以下字段（如无法识别则为 None）：
                - lease_name: 租赁名称
                - lease_commencement_date: 租赁开始日期 (YYYY-MM-DD)
                - lease_term_months: 租赁期限（月）
                - payment_frequency: 付款周期 (monthly/quarterly/annual)
                - payment_amount: 每期租金（不含税）
                - payment_timing: 付款时点 (beginning/end)
                - discount_rate: 折现率（年利率，如 0.05）
                - tax_rate: 税率（如 0.13）
                - initial_direct_costs: 初始直接费用
                - lease_incentives: 租赁激励
                - residual_value_guarantee: 预计复原成本/担保余值
                - purchase_option: 是否有购买选择权 (True/False)
                - purchase_option_price: 购买选择权价格
                - standard: 适用准则 (IFRS16/ASC842)
                - confidence_score: 整体置信度 (0-1)
                - field_confidence: 各字段置信度 dict
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """返回解析器名称。"""
        pass

    @abstractmethod
    def supports(self, mime_type: str) -> bool:
        """检查是否支持该 MIME 类型。"""
        pass

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """验证解析器输出结构。"""
        required_fields = ['lease_commencement_date', 'lease_term_months', 'payment_amount']
        return all(field in output for field in required_fields)
