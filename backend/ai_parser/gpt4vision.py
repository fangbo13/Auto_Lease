import base64
import json
import os
from typing import Dict, Any
from django.conf import settings
from .base import AbstractAIParser
from .prompts import LEASE_EXTRACTION_PROMPT


class GPT4VisionParser(AbstractAIParser):
    def get_name(self) -> str:
        return 'gpt4vision'

    def supports(self, mime_type: str) -> bool:
        return mime_type in [
            'application/pdf',
            'image/png',
            'image/jpeg',
            'image/jpg',
        ]

    def parse(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        try:
            import openai
        except ImportError:
            raise ImportError('请安装 openai 包: pip install openai')

        api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if not api_key:
            raise ValueError('未配置 OPENAI_API_KEY')

        client = openai.OpenAI(api_key=api_key)

        # PDF 需要转换为图片（简化处理：提示用户当前仅直接支持图片）
        if mime_type == 'application/pdf':
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(file_path, first_page=1, last_page=1)
                if images:
                    import tempfile
                    temp_path = os.path.join(tempfile.gettempdir(), 'gpt4v_page1.png')
                    images[0].save(temp_path, 'PNG')
                    file_path = temp_path
                    mime_type = 'image/png'
            except Exception as e:
                raise ValueError(f'PDF 转图片失败: {e}')

        with open(file_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        data_url = f"data:{mime_type};base64,{image_data}"

        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': '你是一个专业的租赁合同解析助手，精通中国会计准则 IFRS 16 租赁准则。'
                },
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': LEASE_EXTRACTION_PROMPT},
                        {'type': 'image_url', 'image_url': {'url': data_url, 'detail': 'high'}},
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.1,
        )

        content = response.choices[0].message.content
        # 清理可能的 markdown 代码块
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
            raise ValueError('GPT-4 Vision 返回结果缺少必要字段')
        return result
