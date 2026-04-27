# 知晓 · 智能家居智能客服 🤖

> 基于 LangChain ReAct Agent + RAG + Streamlit 的多品类智能家居智能客服系统

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.15-green.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-orange.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 项目简介

**知晓** 是一个面向智能家居用户的智能客服系统，当前覆盖 **扫地/扫拖机器人**、**智能冰箱**、**智能空调** 三大品类。

系统以 Streamlit 构建轻量级前端网页，后端基于 LangChain 搭建 **ReAct（Reasoning + Acting）Agent**，整合以下核心能力：

- 🧠 **RAG 增强检索**：将各品类手册片段、常见问题、维护指南等文档向量化存储，AI 回答时优先检索知识库
- 🗺️ **高德 MCP 服务**：调用高德地图 API 实时获取用户定位与天气信息
- 📊 **总结汇报模式**：中间件通过识别特定意图，动态切换系统提示词，自动生成使用情况报告
- 🔧 **多轮工具调用**：Agent 可自主规划并多轮调用所配备的工具，直至满足用户需求
- ⚡ **流式响应**：最终结果在网页端以逐字流式方式呈现，提升交互体验
- 📝 **完善的日志与历史**：配备结构化日志（文件 + 控制台）与对话历史记录

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **LLM** | 阿里云通义千问 `qwen3-max`（通过 `ChatTongyi`）|
| **Embedding** | 阿里云 DashScope `text-embedding-v4` |
| **向量数据库** | Chroma（本地持久化）|
| **Agent 框架** | LangChain ReAct Agent + LangGraph |
| **前端** | Streamlit Web 界面，支持对话历史 |
| **外部服务** | 高德地图 REST API（天气、定位）|
| **动态提示词** | 中间件根据上下文信号量自动切换 System Prompt |
| **去重机制** | MD5 哈希追踪已处理文档，避免重复入库 |
| **日志** | 按天分文件，同时输出到控制台与文件 |
| **测试** | pytest 自动化测试，覆盖率 77%+ |

---

## 🏗 系统架构

```
┌──────────────────────────────────────────────┐
│          Streamlit 前端 (app.py)              │
│  - 对话历史  - 流式显示  - 会话状态管理        │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│        ReAct Agent (agent/react_agent.py)     │
│  ┌─────────────────────────────────────────┐ │
│  │  中间件层 (middleware.py)                │ │
│  │  ├─ monitor_tool   工具调用监控与日志    │ │
│  │  ├─ log_before_model  模型调用前日志     │ │
│  │  └─ report_prompt_switch 动态提示词切换  │ │
│  └─────────────────────────────────────────┘ │
│  工具集：rag_summarize / get_weather /        │
│         get_user_location / get_user_id /     │
│         get_current_month / fetch_external_data│
│         fill_context_for_report               │
└──┬──────────────┬───────────────┬────────────┘
   │              │               │
   ▼              ▼               ▼
┌──────────┐ ┌─────────────┐ ┌────────────────┐
│ RAG 服务 │ │  高德 API   │ │  外部 CSV 数据 │
│(rag/)    │ │ 天气 / 定位 │ │ data/external/ │
└────┬─────┘ └─────────────┘ └────────────────┘
     │
┌────▼─────────────────────────┐
│  Chroma 向量数据库 (chroma_db/)│
│  Embedding: text-embedding-v4 │
│  知识库文档 (data/)           │
├──────────────────────────────┤
│  ┌─────────────────────────┐ │
│  │ 扫地机器人100问.pdf     │ │
│  │ 扫地机器人100问2.txt    │ │
│  │ 扫拖一体机器人100问.txt │ │
│  │ 故障排除.txt            │ │
│  │ 维护保养.txt            │ │
│  │ 选购指南.txt            │ │
│  │ 智能冰箱与空调知识.txt  │ │
│  └─────────────────────────┘ │
└──────────────────────────────┘
```

---

## 📂 目录结构

```
zhisaotong-Agent/
├── app.py                        # Streamlit 前端入口
├── agent/
│   ├── react_agent.py            # ReAct Agent 核心逻辑
│   └── tools/
│       ├── agent_tools.py        # 工具函数定义
│       └── middleware.py         # Agent 中间件
├── rag/
│   ├── rag_service.py            # RAG 检索摘要服务
│   └── vector_store.py           # Chroma 向量库管理
├── model/
│   └── factory.py                # 模型工厂（LLM + Embedding）
├── utils/
│   ├── config_handler.py         # YAML 配置加载器
│   ├── logger_handler.py         # 日志工具
│   ├── prompt_loader.py          # 提示词加载器
│   ├── file_handler.py           # 文档加载（PDF/TXT）
│   └── path_tool.py              # 路径工具
├── config/
│   ├── agent.yml                 # Agent 配置（高德 API Key 等）
│   ├── rag.yml                   # 模型名称配置
│   ├── chroma.yml                # 向量库配置
│   └── prompts.yml               # 提示词文件路径
├── prompts/
│   ├── main_prompt.txt           # 主 ReAct 提示词
│   ├── rag_summarize.txt         # RAG 摘要提示词
│   └── report_prompt.txt         # 报告生成提示词
├── data/                         # 知识库文档
│   ├── 扫地机器人100问.pdf
│   ├── 扫拖一体机器人100问.txt
│   ├── 故障排除.txt
│   ├── 维护保养.txt
│   ├── 选购指南.txt
│   ├── 智能家居冰箱与空调知识.txt
│   └── external/
│       └── records.csv           # 用户使用记录
├── chroma_db/                    # Chroma 持久化目录（自动生成）
├── logs/                         # 日志文件目录（按天自动生成）
├── tests/                        # pytest 自动化测试
│   ├── conftest.py
│   ├── test_config_handler.py
│   ├── test_prompt_loader.py
│   ├── test_file_handler.py
│   └── test_logger_handler.py
├── pytest.ini                    # pytest 配置文件
├── md5.text                      # 文档 MD5 去重记录
└── 启动.bat                      # Windows 一键启动脚本
```

---

## 📦 环境依赖

### Python 版本

建议使用 **Python 3.10+**（代码中使用了 `tuple[str, str]` 等 3.10+ 类型注解语法）。

### 主要依赖包

| 包名 | 用途 |
|------|------|
| `streamlit` | 前端 Web 框架 |
| `langchain` | Agent / Chain / Tool 框架 |
| `langchain-core` | LangChain 核心抽象 |
| `langchain-community` | 通义千问、DashScope Embedding 等集成 |
| `langgraph` | 基于图的 Agent 执行引擎 |
| `langchain-chroma` | LangChain 与 Chroma 向量库集成 |
| `chromadb` | Chroma 向量数据库 |
| `dashscope` | 阿里云 DashScope SDK |
| `pypdf` | PDF 文档加载 |
| `pyyaml` | YAML 配置文件解析 |
| `pytest` | 自动化测试框架 |

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## ⚙️ 配置说明

### 1. 阿里云 DashScope API Key

本项目使用阿里云通义千问（`ChatTongyi`）和 DashScope Embedding，需要配置 **DashScope** 的 API Key：

**推荐：环境变量**

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="你的DashScope密钥"

# Linux / macOS
export DASHSCOPE_API_KEY="你的DashScope密钥"
```

> 可在 [阿里云百炼平台](https://bailian.console.aliyun.com/) 获取 API Key。

### 2. 高德地图 API Key

编辑 `config/agent.yml`，将 `gaodekey` 替换为你的高德地图 Web 服务 API Key：

```yaml
gaodekey: 你的高德key!        # ← 替换这里
```

> 可在 [高德开放平台](https://console.amap.com/) 申请 Web 服务类型的 API Key。

---

## 🚀 快速开始

### 方式一：一键启动（Windows）

双击 `启动.bat`，等待服务启动后浏览器自动打开。

### 方式二：命令行启动

```bash
# 1. 设置 API Key
$env:DASHSCOPE_API_KEY="你的DashScope密钥"

# 2. 启动服务
streamlit run app.py
```

### 方式三：Docker 启动（待实现）

```bash
docker-compose up -d
```

---

## 💬 使用方式

启动后，在浏览器打开 `http://localhost:8501`，即可开始与智能客服对话：

### 产品咨询

可直接提问扫地机器人、冰箱、空调等品类的使用、维护、故障排除等问题：

```
用户：扫地机器人的滤网多久需要更换一次？
用户：智能冰箱冷藏室结霜严重可能是什么原因？
用户：空调滤网大概多久洗一次比较合适？
用户：风冷冰箱和直冷冰箱怎么选？
```

### 天气与定位查询

Agent 可调用高德 API 获取实时信息：

```
用户：我现在所在城市今天的天气怎么样？
```

### 使用报告生成

Agent 会自动检测报告生成意图，生成 Markdown 格式的使用情况报告：

```
用户：帮我生成我的使用报告
用户：给我一份智能家居的使用分析和保养建议
```

---

## 🧪 自动化测试

项目使用 pytest 进行自动化测试：

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=utils --cov-report=term-missing

# 运行单个测试文件
pytest tests/test_config_handler.py
```

当前测试覆盖率：**77%+**（持续改进中）

---

## 🛠 工具列表

Agent 配备了以下 7 个工具：

| 工具名 | 描述 |
|--------|------|
| `rag_summarize` | 从向量知识库检索多品类智能家居参考资料 |
| `get_weather` | 获取指定城市的实时天气（高德 API）|
| `get_user_location` | 通过 IP 获取用户所在城市（高德 API）|
| `get_user_id` | 获取当前用户 ID |
| `get_current_month` | 获取当前月份 |
| `fetch_external_data` | 从外部系统获取指定用户指定月份的使用记录 |
| `fill_context_for_report` | 触发报告模式，切换为报告生成提示词 |

---

## 📊 日志说明

日志文件存放在 `logs/` 目录下，按天自动创建：

```
logs/
└── agent_20260427.log    # 格式：agent_YYYYMMDD.log
```

| 级别 | 说明 |
|------|------|
| `INFO` | 正常运行信息（控制台输出）|
| `DEBUG` | 调试信息（文件输出）|
| `ERROR` | 错误信息 |

---

## 🔄 中间件机制

Agent 的三个中间件负责监控、日志和动态提示词切换：

```
monitor_tool         工具调用监控
  ├─ 记录每次工具调用的名称和参数
  ├─ 记录工具调用成功/失败状态
  └─ 检测 fill_context_for_report 调用，将 context["report"] 置为 True

log_before_model     模型调用前日志
  └─ 记录当前消息数量及最新消息内容

report_prompt_switch 动态提示词切换
  ├─ context["report"] == True  → 使用报告生成提示词
  └─ context["report"] == False → 使用主 ReAct 提示词
```

---

## 🔮 后续优化方向

- [ ] 将向量数据库从 Chroma 替换为 Redis（更适合生产部署）
- [ ] 地点、天气等功能完整迁移至高德 MCP 协议
- [ ] 增加用户身份认证与多用户会话隔离
- [ ] 支持更多文档格式（Word、Excel 等）
- [ ] 提高测试覆盖率至 90%+
- [ ] FastAPI 替代 Streamlit（前后端分离）
- [ ] Docker 容器化部署

---

## 📜 License

MIT License

---

## 🙏 致谢

- [LangChain](https://www.langchain.com/) - Agent 框架
- [Streamlit](https://streamlit.io/) - 前端框架
- [阿里云百炼](https://bailian.console.aliyun.com/) - 大模型服务
- [高德开放平台](https://console.amap.com/) - 地图 API

---

_⭐ 如果这个项目对你有帮助，欢迎 Star！_
