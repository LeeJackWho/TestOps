# TestOps

![CI](https://github.com/LeeJackWho/TestOps/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

AI-assisted automation testing framework based on Playwright + Pytest + Allure + Midscene, supporting UI / API / MQTT testing. Page Object pattern, data-driven, Docker-ready.

## 项目简介
这是一个基于 Playwright + Pytest + Allure + Midscene + Request 的自动化测试框架，支持 UI 自动化测试、API 自动化测试和 **MQTT 消息中间件测试**。框架采用 Page Object 模式设计，具有良好的可维护性和扩展性。

## 子系统总览

| 子系统 | 目录 | 说明 |
|---|---|---|
| UI 自动化测试 | `test_ui/` | Playwright + Midscene AI 辅助，Page Object 模式 |
| API 自动化测试 | `test_api/` | requests 封装 + YAML 数据驱动 |
| MQTT 测试 | `test_mqtt/` | paho-mqtt 封装，覆盖发布/订阅回路、QoS、遗留消息、通配符订阅 |
| 框架自测 | `tests/` | 配置模块与数据加载器的单元自测，CI 门禁 |
| Docker 化 | `Dockerfile` / `docker-compose.yml` | 一键拉起 Mosquitto broker 并执行自测 + MQTT 测试 |
| CI | `.github/workflows/ci.yml` | GitHub Actions：框架自测 + MQTT 集成测试双 job |

## 环境要求
- Python 3.7+
- Node.js 14+
- npm 6+
- Playwright
- Allure (可选)

## 框架目录
```
TestOps/
├── Common/                 # 公共方法层
│   ├── base_page.py       # 页面基类
│   └── ...               # 其他公共方法
│├── Config/                # 配置层
│   ├── config.ini        # 配置文件
│   └── ...              # 其他配置
│
├── Log/                  # 日志文件（自动生成）
│   └── ...              # 运行日志
│
├── Reports/              # 测试报告（自动生成）
│   ├── allure-results/   # Allure 原始结果
│   └── html/            # HTML 报告
│
├── TestDatas/            # 测试数据
│   ├── api_data/        # API测试数据
│   └── ui_data/         # UI测试数据
│
├── Utils/                # 工具类
│   ├── logger.py        # 日志工具
│   ├── file_reader.py   # 文件读取工具
│   └── ...             # 其他工具类
│
├── test_api/            # API测试用例
│   ├── __init__.py
│   └── ...             # API测试脚本
│
├── test_mqtt/           # MQTT测试用例
│   ├── mqtt/           # paho-mqtt 客户端封装
│   ├── conftest.py     # broker 夹具（MQTT_BROKER/MQTT_PORT 环境变量）
│   └── ...             # 发布/订阅/QoS/遗留消息/通配符用例
│
├── tests/               # 框架自测（CI 门禁）
├── mosquitto/           # Mosquitto broker 配置
├── .github/workflows/   # GitHub Actions CI
├── Dockerfile           # 测试执行镜像
├── docker-compose.yml   # 一键运行（broker + tests）
│
├── test_ui/             # UI测试用例
│   ├── __init__.py
│   ├── pages/          # 页面对象
│   └── ...            # UI测试脚本
│
├── test-results/        # 测试结果
├── midscene_run/        # Midscene运行相关
│   ├── report/         # Midscene报告
│   └── dump-logger/    # 日志文件
│
├── node_modules/        # Node.js依赖包
│
├── assets/             # 静态资源文件
│
├── .env               # 环境变量配置
├── .gitignore         # Git忽略文件配置
├── .npmrc             # NPM配置
├── conftest.py        # Pytest配置文件
├── README.md          # 项目说明文档
├── requirements.txt    # Python依赖配置
├── setup.py           # 项目安装配置
├── package.json       # 项目依赖配置
├── package-lock.json  # 依赖版本锁定文件
├── playwright.config.ts # Playwright配置
├── run.py             # 测试执行入口
└── tsconfig.json      # TypeScript配置
```

## 快速开始

### 1. 克隆项目
```bash
git clone repository
```

### 2. 安装依赖
```
pip install -r requirements.txt
playwright install chromium
```
### 有安装Allure的情况下运行测试并查看报告
```
python run.py
```
### 没安装Allure的情况下运行测试并查看报告
```
pytest --html=report.html
```

### 3. 配置环境变量

create `.env` file

```shell
# export OPENAI_BASE_URL="https://gemini.deno.dev"
# export OPENAI_API_KEY="YOUR_KEY"
# export MIDSCENE_MODEL_NAME="gemini-2.0-flash-exp"
export MIDSCENE_DEBUG_AI_PROFILE=1

export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export OPENAI_API_KEY="sk-or-v1-YOUR_KEY"
export MIDSCENE_MODEL_NAME="qwen/qwen2.5-vl-32b-instruct:free"
```

Refer to this document if your want to use other models like Qwen: https://midscenejs.com/choose-a-model

新增依赖：npm install @midscene/web --save-dev

### 4. 运行测试

run test_ui test

```bash
npm install

npx playwright install

# run test_ui test
npm run test_ui

# prefer using cache
npm run test_ui:cache

# run test_ui with playwright ui, remember to click the little "Play" button on the upper-left corner
npm run test_ui:ui

# run test_ui with playwright ui + cache
npm run test_ui:ui:cache
```

After the above command executes successfully, the console will output: `Midscene - report file updated: ./current_cwd/midscene_run/report/some_id.html.` You can open this file in a browser to view the report.

# 运行测试用例
```
npx playwright test ./test_ui/todo-mvc-zh.spec.ts
npx playwright test --headed ./test_ui/todo-mvc-zh.spec.ts
```


# 查看测试报告
当上面的命令执行成功后，会在控制台输出：
```
Midscene - report file updated: ./current_cwd/midscene_run/report/some_id.html
```
通过浏览器打开该文件即可看到报告。

## 框架特点
- 支持 UI 自动化测试和 API 自动化测试
- 使用 Page Object 模式，提高代码复用性和可维护性
- 集成 Allure 报告，提供详细的测试报告
- 支持多环境配置
- 集成 Midscene 进行 AI 辅助测试
- 提供完整的日志记录功能

## 使用指南

### UI 测试用例编写
```python
# 示例：test_ui/test_login.py
def test_login(page):
    # 测试步骤
    pass
```

### API 测试用例编写
```python
# 示例：test_api/test_user_api.py
def test_user_api():
    # 测试步骤
    pass
```

## MQTT 测试

### 本地运行（需先启动 broker）

```bash
# 方式一：Docker 一键运行（自动拉起 Mosquitto + 执行测试）
docker compose up --build tests

# 方式二：本机已安装 mosquitto
mosquitto -c mosquitto/config/mosquitto.conf -d
pytest test_mqtt -v -o "addopts="
```

### 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `MQTT_BROKER` | `localhost` | broker 地址 |
| `MQTT_PORT` | `1883` | broker 端口 |

测试数据（topic/payload/QoS）见 `TestDatas/mqtt_data.yaml`，新增场景只需加 YAML 用例。

## UI 测试

### 本地运行

```bash
# 首次运行需安装浏览器内核
playwright install chromium

# 有头模式（本地调试，可看到浏览器操作）
HEADLESS=0 pytest test_ui/test_case -v -o "addopts="

# 无头模式（默认，CI 与脚本场景）
HEADLESS=1 pytest test_ui/test_case -v -o "addopts="
```

### 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `HEADLESS` | `1` | `1` 无头 / `0` 有头，本地调试设为 `0` |
| `BASE_URL` | `https://www.baidu.com` | 浏览器上下文根地址 |
| `SLOW_MO` | `0` | 每步操作延迟毫秒数，调试可设 `200` |

### 演示用例说明

UI 冒烟用例基于仓库内静态页 `assets/demo_search.html`（数据驱动：`TestDatas/search_data.yaml`），
不依赖真实第三方站点——外部页面改版频繁且可能触发风控，会导致 CI 长期不稳定。
如需针对真实站点编写用例，建议仅本地调试运行，不要直接挂进 CI 门禁。

### 失败取证

`conftest.py` 注册了 `attach_on_failure` 全局 fixture：用例失败时自动全页截图至
`Reports/screenshots/<用例名>.png`，并打印失败时的页面 URL。CI 已将该目录作为
artifact 上传（保留 7 天），便于直接定位 UI 失败原因。

## 常见问题
1. 如何处理测试环境配置？
   - 在 `.env` 文件中配置相应的环境变量

2. 如何添加新的测试用例？
   - 在 test_ui 或 test_api 目录下创建新的测试文件

3. CI 上 UI 用例报浏览器启动失败？
   - conftest 默认无头运行，且 launch 已带 `--disable-dev-shm-usage`；
     若本地调试需有头，显式设置 `HEADLESS=0`
   - 遵循项目的命名规范和测试规范

## 贡献指南
1. Fork 本仓库
2. 创建您的特性分支 (git checkout -b feature/AmazingFeature)
3. 提交您的更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 打开一个 Pull Request

## 参考文档
https://midscenejs.com/integrate-with-playwright.html
https://midscenejs.com/api.html

## 许可证
MIT License

## 联系方式
如有问题，请提交 Issue 或联系项目维护者。