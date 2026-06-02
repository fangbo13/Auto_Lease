import io
from decimal import Decimal
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from .base_generator import BaseExcelGenerator
from excel_export.templates.chinese_styles import (
    apply_style, set_column_widths,
    TITLE_STYLE, HEADER_STYLE, DATA_STYLE, DATA_STYLE_LEFT, LABEL_STYLE,
    CURRENCY_FORMAT, PERCENTAGE_FORMAT, DATE_FORMAT, THIN_BORDER, TITLE_FILL,
)


class ChineseAuditWorkingPaperGenerator(BaseExcelGenerator):
    """中国式审计底稿生成器。"""

    def generate(self, lease_input, calculation_result) -> bytes:
        wb = Workbook()

        self._create_cover_sheet(wb, lease_input)
        self._create_input_sheet(wb, lease_input)
        self._create_summary_sheet(wb, lease_input, calculation_result)
        self._create_schedule_sheet(wb, calculation_result)
        self._create_journal_sheet(wb, calculation_result)

        # 删除默认 Sheet
        if 'Sheet' in wb.sheetnames:
            del wb['Sheet']

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output.read()

    def _create_cover_sheet(self, wb, lease_input):
        ws = wb.create_sheet('封面')
        set_column_widths(ws, {'A': 20, 'B': 40, 'C': 20, 'D': 40})

        # 标题
        ws.merge_cells('A1:D1')
        cell = ws['A1']
        cell.value = '租赁使用权资产审计工作底稿'
        apply_style(cell, TITLE_STYLE)
        ws.row_dimensions[1].height = 40

        # 基本信息
        cover_data = [
            ('项目名称', lease_input.lease_name, '编制日期', datetime.now().strftime('%Y-%m-%d')),
            ('租赁开始日', str(lease_input.lease_commencement_date), '租赁期限(月)', str(lease_input.lease_term_months)),
            ('适用准则', lease_input.standard, '付款周期', self._get_frequency_label(lease_input.payment_frequency)),
            ('', '', '', ''),
            ('编制人', '', '复核人', ''),
            ('编制日期', '', '复核日期', ''),
        ]

        for idx, (label1, value1, label2, value2) in enumerate(cover_data, start=3):
            ws[f'A{idx}'] = label1
            apply_style(ws[f'A{idx}'], LABEL_STYLE)
            ws[f'B{idx}'] = value1
            apply_style(ws[f'B{idx}'], DATA_STYLE_LEFT)
            ws[f'C{idx}'] = label2
            apply_style(ws[f'C{idx}'], LABEL_STYLE)
            ws[f'D{idx}'] = value2
            apply_style(ws[f'D{idx}'], DATA_STYLE_LEFT)
            ws.row_dimensions[idx].height = 28

        # 签章区提示
        ws.merge_cells('A9:D9')
        ws['A9'] = '本底稿依据《企业会计准则第21号——租赁》（IFRS 16 / ASC 842）编制'
        apply_style(ws['A9'], DATA_STYLE_LEFT)

    def _create_input_sheet(self, wb, lease_input):
        ws = wb.create_sheet('输入参数')
        set_column_widths(ws, {'A': 25, 'B': 30, 'C': 25, 'D': 30})

        ws.merge_cells('A1:D1')
        ws['A1'] = '输入参数表'
        apply_style(ws['A1'], TITLE_STYLE)
        ws.row_dimensions[1].height = 35

        inputs = [
            ('租赁名称', lease_input.lease_name, '适用准则', lease_input.standard),
            ('租赁开始日', str(lease_input.lease_commencement_date), '租赁期限(月)', str(lease_input.lease_term_months)),
            ('付款周期', self._get_frequency_label(lease_input.payment_frequency), '付款时点', self._get_timing_label(lease_input.payment_timing)),
            ('每期租金(不含税)', float(lease_input.payment_amount), '税率', f"{float(lease_input.tax_rate) * 100:.2f}%"),
            ('折现率(年)', f"{float(lease_input.discount_rate) * 100:.4f}%", '折现率类型', self._get_rate_type_label(lease_input.discount_rate_type)),
            ('初始直接费用', float(lease_input.initial_direct_costs), '租赁激励', float(lease_input.lease_incentives)),
            ('复原成本/担保余值', float(lease_input.residual_value_guarantee), '购买选择权', '是' if lease_input.purchase_option else '否'),
        ]
        if lease_input.purchase_option:
            inputs.append(('购买选择权价格', float(lease_input.purchase_option_price or 0), '', ''))

        for idx, (label1, value1, label2, value2) in enumerate(inputs, start=3):
            ws[f'A{idx}'] = label1
            apply_style(ws[f'A{idx}'], HEADER_STYLE)
            ws[f'B{idx}'] = value1
            apply_style(ws[f'B{idx}'], DATA_STYLE_LEFT)
            ws[f'C{idx}'] = label2
            apply_style(ws[f'C{idx}'], HEADER_STYLE)
            ws[f'D{idx}'] = value2
            apply_style(ws[f'D{idx}'], DATA_STYLE_LEFT)

    def _create_summary_sheet(self, wb, lease_input, calculation_result):
        ws = wb.create_sheet('计算汇总')
        set_column_widths(ws, {'A': 30, 'B': 25, 'C': 30, 'D': 25})

        ws.merge_cells('A1:D1')
        ws['A1'] = '计算汇总表'
        apply_style(ws['A1'], TITLE_STYLE)
        ws.row_dimensions[1].height = 35

        summary = [
            ('使用权资产', float(calculation_result.right_of_use_asset), '租赁负债', float(calculation_result.lease_liability)),
            ('总付款额', float(calculation_result.total_payments), '总利息费用', float(calculation_result.total_interest)),
            ('总折旧费用', float(calculation_result.total_depreciation), '实际月利率', f"{float(calculation_result.effective_monthly_rate) * 100:.6f}%"),
            ('首月利息', float(calculation_result.first_month_interest), '首月折旧', float(calculation_result.first_month_depreciation)),
        ]

        for idx, (label1, value1, label2, value2) in enumerate(summary, start=3):
            ws[f'A{idx}'] = label1
            apply_style(ws[f'A{idx}'], HEADER_STYLE)
            ws[f'B{idx}'] = value1
            ws[f'B{idx}'].number_format = CURRENCY_FORMAT
            apply_style(ws[f'B{idx}'], DATA_STYLE)
            ws[f'C{idx}'] = label2
            apply_style(ws[f'C{idx}'], HEADER_STYLE)
            ws[f'D{idx}'] = value2
            if isinstance(value2, (int, float, Decimal)):
                ws[f'D{idx}'].number_format = CURRENCY_FORMAT
            apply_style(ws[f'D{idx}'], DATA_STYLE)

        # 计算公式说明
        ws.merge_cells('A8:D8')
        ws['A8'] = '计算说明'
        apply_style(ws['A8'], TITLE_STYLE)

        formulas = [
            '租赁负债 = 每期付款额 × 年金现值系数（按折现率、期数、期初/期末）',
            '使用权资产 = 租赁负债 + 初始直接费用 - 租赁激励 + 复原成本 + 购买选择权价格',
            '利息费用 = 期初负债 × 实际利率',
            '本金偿还 = 每期付款额 - 利息费用',
            '折旧费用 = 使用权资产 / 租赁期限（直线法）',
        ]
        for idx, text in enumerate(formulas, start=9):
            ws.merge_cells(f'A{idx}:D{idx}')
            ws[f'A{idx}'] = text
            apply_style(ws[f'A{idx}'], DATA_STYLE_LEFT)

    def _create_schedule_sheet(self, wb, calculation_result):
        ws = wb.create_sheet('摊销明细表')
        headers = ['期次', '期初日期', '期末日期', '期初负债', '付款额', '利息费用',
                   '本金偿还', '期末负债', '期初ROU', '折旧费用', '期末ROU']
        col_widths = {'A': 8, 'B': 14, 'C': 14, 'D': 18, 'E': 18, 'F': 18,
                      'G': 18, 'H': 18, 'I': 18, 'J': 18, 'K': 18}
        set_column_widths(ws, col_widths)

        ws.merge_cells('A1:K1')
        ws['A1'] = '摊销明细表'
        apply_style(ws['A1'], TITLE_STYLE)
        ws.row_dimensions[1].height = 35

        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=3, column=col_idx, value=header)
            apply_style(cell, HEADER_STYLE)

        schedule = calculation_result.schedule.all()
        for row_idx, item in enumerate(schedule, start=4):
            values = [
                item.period_number,
                item.period_start_date,
                item.period_end_date,
                float(item.opening_liability),
                float(item.payment_amount),
                float(item.interest_expense),
                float(item.principal_reduction),
                float(item.closing_liability),
                float(item.rou_asset_opening),
                float(item.depreciation_expense),
                float(item.rou_asset_closing),
            ]
            for col_idx, value in enumerate(values, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                apply_style(cell, DATA_STYLE)
                if col_idx >= 4:
                    cell.number_format = CURRENCY_FORMAT
                elif col_idx in [2, 3]:
                    cell.number_format = DATE_FORMAT

    def _create_journal_sheet(self, wb, calculation_result):
        ws = wb.create_sheet('会计分录建议')
        set_column_widths(ws, {'A': 12, 'B': 25, 'C': 25, 'D': 20, 'E': 50})

        ws.merge_cells('A1:E1')
        ws['A1'] = '会计分录建议'
        apply_style(ws['A1'], TITLE_STYLE)
        ws.row_dimensions[1].height = 35

        headers = ['期次', '借方科目', '贷方科目', '金额', '摘要']
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=3, column=col_idx, value=header)
            apply_style(cell, HEADER_STYLE)

        schedule = calculation_result.schedule.all()
        row_idx = 4
        for item in schedule:
            # 折旧分录
            ws.cell(row=row_idx, column=1, value=item.period_number)
            ws.cell(row=row_idx, column=2, value='管理费用/制造费用-折旧费')
            ws.cell(row=row_idx, column=3, value='使用权资产累计折旧')
            ws.cell(row=row_idx, column=4, value=float(item.depreciation_expense))
            ws.cell(row=row_idx, column=5, value=f'第{item.period_number}期使用权资产折旧')
            for col in range(1, 6):
                apply_style(ws.cell(row=row_idx, column=col), DATA_STYLE_LEFT if col in [2, 3, 5] else DATA_STYLE)
            ws.cell(row=row_idx, column=4).number_format = CURRENCY_FORMAT
            row_idx += 1

            # 利息分录
            ws.cell(row=row_idx, column=1, value=item.period_number)
            ws.cell(row=row_idx, column=2, value='财务费用-利息支出')
            ws.cell(row=row_idx, column=3, value='租赁负债')
            ws.cell(row=row_idx, column=4, value=float(item.interest_expense))
            ws.cell(row=row_idx, column=5, value=f'第{item.period_number}期租赁负债利息')
            for col in range(1, 6):
                apply_style(ws.cell(row=row_idx, column=col), DATA_STYLE_LEFT if col in [2, 3, 5] else DATA_STYLE)
            ws.cell(row=row_idx, column=4).number_format = CURRENCY_FORMAT
            row_idx += 1

            # 付款分录
            ws.cell(row=row_idx, column=1, value=item.period_number)
            ws.cell(row=row_idx, column=2, value='租赁负债')
            ws.cell(row=row_idx, column=3, value='银行存款')
            ws.cell(row=row_idx, column=4, value=float(item.payment_amount))
            ws.cell(row=row_idx, column=5, value=f'第{item.period_number}期支付租金')
            for col in range(1, 6):
                apply_style(ws.cell(row=row_idx, column=col), DATA_STYLE_LEFT if col in [2, 3, 5] else DATA_STYLE)
            ws.cell(row=row_idx, column=4).number_format = CURRENCY_FORMAT
            row_idx += 1

    @staticmethod
    def _get_frequency_label(value):
        mapping = {'monthly': '月付', 'quarterly': '季付', 'annual': '年付'}
        return mapping.get(value, value)

    @staticmethod
    def _get_timing_label(value):
        mapping = {'beginning': '期初', 'end': '期末'}
        return mapping.get(value, value)

    @staticmethod
    def _get_rate_type_label(value):
        mapping = {'incremental_borrowing': '增量借款利率', 'implicit_rate': '租赁内含利率'}
        return mapping.get(value, value)
