from rest_framework.exceptions import APIException


class LeaseCalculationError(APIException):
    status_code = 400
    default_detail = '租赁计算发生错误。'
    default_code = 'lease_calculation_error'


class ParseError(APIException):
    status_code = 400
    default_detail = '合同解析发生错误。'
    default_code = 'parse_error'


class ExportError(APIException):
    status_code = 400
    default_detail = '导出发生错误。'
    default_code = 'export_error'
