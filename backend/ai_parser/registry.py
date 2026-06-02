from django.conf import settings
from .base import AbstractAIParser


class ParserRegistry:
    _parsers = {}

    @classmethod
    def register(cls, name: str, parser_class):
        if not issubclass(parser_class, AbstractAIParser):
            raise ValueError(f'解析器 {name} 必须继承 AbstractAIParser')
        cls._parsers[name] = parser_class

    @classmethod
    def get_parser(cls, name: str = None) -> AbstractAIParser:
        if name is None:
            name = getattr(settings, 'AI_PARSER_BACKEND', 'tesseract')
        if name not in cls._parsers:
            raise ValueError(f'未注册的解析器: {name}。可用解析器: {list(cls._parsers.keys())}')
        return cls._parsers[name]()

    @classmethod
    def list_parsers(cls):
        return list(cls._parsers.keys())


def get_active_parser(name: str = None) -> AbstractAIParser:
    return ParserRegistry.get_parser(name)


# 延迟导入并注册，避免循环依赖
def _register_default_parsers():
    from .gpt4vision import GPT4VisionParser
    from .qwen import QwenParser
    from .tesseract import TesseractParser

    ParserRegistry.register('gpt4vision', GPT4VisionParser)
    ParserRegistry.register('qwen', QwenParser)
    ParserRegistry.register('tesseract', TesseractParser)


_register_default_parsers()
