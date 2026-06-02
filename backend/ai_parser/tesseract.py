import os
import re
import json
from typing import Dict, Any
from .base import AbstractAIParser


class TesseractParser(AbstractAIParser):
    """Tesseract OCR 兜底解析器，无需外部 API 密钥。"""

    def get_name(self) -> str:
        return 'tesseract'

    def supports(self, mime_type: str) -> bool:
        return mime_type in [
            'application/pdf',
            'image/png',
            'image/jpeg',
            'image/jpg',
        ]

    def parse(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            raise ImportError('请安装 pytesseract 和 Pillow: pip install pytesseract Pillow')

        # PDF 转图片
        if mime_type == 'application/pdf':
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(file_path, first_page=1, last_page=1)
                if images:
                    import tempfile
                    temp_path = os.path.join(tempfile.gettempdir(), 'tess_page1.png')
                    images[0].save(temp_path, 'PNG')
                    file_path = temp_path
            except Exception as e:
                raise ValueError(f'PDF 转图片失败: {e}')

        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')

        result = self._extract_from_text(text)
        result['parsed_text'] = text
        return result

    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        result = {
            'lease_name': None,
            'lease_commencement_date': None,
            'lease_term_months': None,
            'payment_frequency': 'monthly',
            'payment_amount': None,
            'payment_timing': 'end',
            'discount_rate': None,
            'tax_rate': None,
            'initial_direct_costs': 0,
            'lease_incentives': 0,
            'residual_value_guarantee': 0,
            'purchase_option': False,
            'purchase_option_price': None,
            'standard': 'IFRS16',
            'confidence_score': 0.3,
            'field_confidence': {},
        }

        # 提取日期
        date_patterns = [
            r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{4})/(\d{2})/(\d{2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                result['lease_commencement_date'] = f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
                result['field_confidence']['lease_commencement_date'] = 0.4
                break

        # 提取期限（月/年）
        term_patterns = [
            r'(\d+)\s*个月',
            r'期限\s*(\d+)\s*月',
            r'租期\s*(\d+)\s*月',
            r'(\d+)\s*年',
            r'期限\s*(\d+)\s*年',
        ]
        for pattern in term_patterns:
            match = re.search(pattern, text)
            if match:
                value = int(match.group(1))
                if '年' in pattern:
                    value *= 12
                result['lease_term_months'] = value
                result['field_confidence']['lease_term_months'] = 0.4
                break

        # 提取金额
        amount_patterns = [
            r'租金[\s\w]*?(\d[\d,\.]+)\s*元',
            r'每期[\s\w]*?(\d[\d,\.]+)\s*元',
            r'月租[\s\w]*?(\d[\d,\.]+)',
            r'(\d[\d,\.]+)\s*元\s*/\s*月',
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    result['payment_amount'] = float(amount_str)
                    result['field_confidence']['payment_amount'] = 0.3
                except ValueError:
                    pass
                break

        # 提取税率
        tax_patterns = [
            r'增值税率\s*(\d+\.?\d*)\s*%',
            r'税率\s*(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)%\s*增值税',
        ]
        for pattern in tax_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    result['tax_rate'] = float(match.group(1)) / 100
                    result['field_confidence']['tax_rate'] = 0.3
                except ValueError:
                    pass
                break

        # 提取利率/折现率
        rate_patterns = [
            r'利率\s*(\d+\.?\d*)\s*%',
            r'折现率\s*(\d+\.?\d*)\s*%',
            r'年利率\s*(\d+\.?\d*)\s*%',
        ]
        for pattern in rate_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    result['discount_rate'] = float(match.group(1)) / 100
                    result['field_confidence']['discount_rate'] = 0.2
                except ValueError:
                    pass
                break

        return result
