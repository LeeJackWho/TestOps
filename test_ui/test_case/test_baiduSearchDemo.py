import allure
import pytest
from Common.read_file import load_yaml
from test_ui.pages.demo_baidu_page import BaiduPage

# 通过Allure装饰器增强报告可读性
@allure.epic("百度搜索测试")
# 冒烟测试标记
@pytest.mark.smoke
class TestSearch:
    # 使用@pytest.mark.parametrize实现数据驱动
    @pytest.mark.parametrize("case", load_yaml("search_data.yaml"))
    def test_search_flow(self, page, case):
        baidu_page = BaiduPage(page)
        # 执行搜索并验证结果
        baidu_page.navigate_to_baidu()
        baidu_page.search(case["keyword"])
        assert case["expected"] in baidu_page.get_first_result()
        
        # 添加Allure报告附件
        baidu_page.take_screenshot("搜索结果页")