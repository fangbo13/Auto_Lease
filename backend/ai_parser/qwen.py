import base64
import json
import os
from typing import Dict, Any
from django.conf import settings
from .base import AbstractAIParser
from .prompts import LEASE_EXTRACTION_PROMPT


class QwenParser(AbstractAIParser):
    """Qwen-VL 解析器（预留实现，基于 DashScope / 阿里云百炼）。"""

    def get_name(self) -> str:
        return 'qwen'

    def supports(self, mime_type: str) -> bool:
        return mime_type in [
            'application/pdf',
            'image/png',
            'image/jpeg',
            'image/jpg',
        ]

    def parse(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        api_key = getattr(settings, 'QWEN_API_KEY', '')
        if not api_key:
            raise ValueError('未配置 QWEN_API_KEY')

        # PDF 转图片
        if mime_type == 'application/pdf':
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(file_path, first_page=1, last_page=1)
                if images:
                    import tempfile
                    temp_path = os.path.join(tempfile.gettempdir(), 'qwen_page1.png')
                    images[0].save(temp_path, 'PNG')
                    file_path = temp_path
                    mime_type = 'image/png'
            except Exception as e:
                raise ValueError(f'PDF 转图片失败: {e}')

        with open(file_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # DashScope API 调用示例（需根据实际 API 调整）
        import requests
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'qwen-vl-plus',
            'input': {
                'messages': [
                    {
                        'role': 'system',
                        'content': [{'text': '你是一个专业的租赁合同解析助手，精通中国会计准则 IFRS 16 租赁准则。'}]
                    },
                    {
                        'role': 'user',
                        'content': [
                            {'image': f'data:{mime_type};base64,{image_data}'},
                            {'text': LEASE_EXTRACTION_PROMPT},
                        ]
                    }
                ]
            },
            'parameters': {
                'result_format': 'message',
                'temperature': 0.1,
            }
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        content = data['output']['choices'][0]['message']['content']
        if isinstance(content, list):
            content = content[0].get('text', '')

        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()

        result = json.loads(content)
        if not self.validate_output(result):
            raise ValueError('Qwen 返回结果缺少必要字段')
        return result
