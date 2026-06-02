# Auto Lease

租赁使用权资产自动计算与审计底稿生成系统。

基于 IFRS 16 / ASC 842 准则，支持上传租赁合同（PDF/图片）进行 AI 自动识别，或手动填写租赁参数，自动计算使用权资产、租赁负债、折旧与利息费用，并导出中国式审计风格的 Excel 底稿。

## 技术栈

- **前端**: React 18 + TypeScript + Tailwind CSS + Vite + Recharts
- **后端**: Django 4 + Django REST Framework + PostgreSQL/SQLite
- **AI 解析**: GPT-4 Vision / Qwen-VL / Tesseract OCR（可插拔）
- **部署**: Docker Compose

## 快速启动

### Docker Compose（推荐）

```bash
# 1. 克隆项目并进入目录
cd Auto_Lease

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入必要的 API Key

# 3. 启动全部服务
docker-compose up --build

# 4. 访问
# 前端: http://localhost
# 后端 API: http://localhost/api/
# Django Admin: http://localhost/api/admin/
```

### 本地开发

**后端:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**前端:**
```bash
cd frontend
npm install
npm run dev
```

## AI 解析器配置

在 `.env` 中设置 `AI_PARSER_BACKEND`：

- `tesseract`（默认）: 本地 OCR，无需 API Key
- `gpt4vision`: OpenAI GPT-4 Vision，需配置 `OPENAI_API_KEY`
- `qwen`: 阿里云 Qwen-VL，需配置 `QWEN_API_KEY`

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/contracts/` | POST | 上传合同 |
| `/api/contracts/{id}/parse/` | POST | 触发 AI 解析 |
| `/api/lease-inputs/` | POST/GET | 创建/列表租赁输入 |
| `/api/lease-inputs/{id}/calculate/` | POST | 触发计算 |
| `/api/export/working-paper/` | GET | 下载审计底稿 Excel |

## 项目结构

```
Auto_Lease/
├── backend/          # Django 后端
│   ├── auto_lease/   # 项目配置
│   ├── contracts/    # 合同上传
│   ├── lease_input/  # 租赁参数
│   ├── ai_parser/    # AI 解析器（可插拔）
│   ├── calculations/ # IFRS 16 计算引擎
│   ├── excel_export/ # 审计底稿 Excel 生成
│   └── audit_trail/  # 审计日志
├── frontend/         # React 前端
├── nginx/            # 反向代理
└── docker-compose.yml
```

## 审计底稿 Excel 格式

生成的 Excel 包含 5 个工作表：
1. **封面**: 项目信息、编制人/复核人签章区
2. **输入参数**: 所有租赁输入字段，用于审计追溯
3. **计算汇总**: 使用权资产、租赁负债、总付款额、总利息等
4. **摊销明细表**: 逐期利息、本金、折旧、负债余额、ROU 净值
5. **会计分录建议**: 每期折旧、利息、付款的建议分录

样式采用中国式审计底稿风格：带边框、标题行深蓝底色、表头浅蓝底色、固定列宽。
