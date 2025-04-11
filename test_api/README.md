pip install -r requirements.txt

# 运行所有测试
pytest test_api

# 运行特定测试文件
pytest test_api/test_cases/test_sample.py

# 生成HTML报告
pytest test_api --html=report.html

# 生成Allure报告
pytest test_api --alluredir=./allure-results
allure serve ./allure-results