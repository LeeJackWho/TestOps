import allure
import pytest
from Common.read_file import load_yaml
from test_ui.pages.demo_search_page import DemoSearchPage

# 通过Allure装饰器增强报告可读性
@allure.epic("演示搜索测试")
# 冒烟测试标记
@pytest.mark.smoke
class TestSearch:
    """本地 fixture 页面驱动的搜索冒烟用例（CI 稳定，不依赖外部站点）"""

    # 使用@pytest.mark.parametrize实现数据驱动
    @pytest.mark.parametrize("case", load_yaml("search_data.yaml"))
    def test_search_flow(self, page, case):
        demo_page = DemoSearchPage(page)
        # 执行搜索并验证结果
        demo_page.open_demo_page()
        demo_page.search(case["keyword"])
        assert case["expected"] in demo_page.get_first_result()

        # 添加Allure报告附件
        demo_page.take_screenshot("搜索结果页")
