## 项目简介
这是一个基于 Playwright + Pytest + Allure + Midscene + Request 的自动化测试框架，支持 UI 自动化测试和 API 自动化测试。框架采用 Page Object 模式设计，具有良好的可维护性和扩展性。

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
│
├── Config/                # 配置层
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

## 常见问题
1. 如何处理测试环境配置？
   - 在 `.env` 文件中配置相应的环境变量

2. 如何添加新的测试用例？
   - 在 test_ui 或 test_api 目录下创建新的测试文件
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