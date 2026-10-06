import os

import allure
from playwright.sync_api import Page
from test_ui.elements.demo_search_element import DemoSearchElements


class DemoSearchPage:
    """本地演示搜索页面对象。

    使用仓库内静态页（assets/demo_search.html）而非真实第三方站点：
    第三方页面改版频繁且可能触发风控，CI 依赖它会长期处于不稳定状态。
    """

    def __init__(self, page: Page):
        self.page = page
        self.elements = DemoSearchElements()

    def open_demo_page(self):
        demo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "assets", "demo_search.html",
        )
        self.page.goto("file://" + demo_path)

    def search(self, keyword: str):
        self.page.fill(self.elements.search_input, keyword)
        self.page.click(self.elements.search_btn)
        # 等待结果区块渲染
        self.page.wait_for_selector(self.elements.first_result, timeout=5000)

    def get_first_result(self) -> str:
        return self.page.text_content(self.elements.first_result) or ""

    def take_screenshot(self, name: str):
        """添加截图到Allure报告"""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name, allure.attachment_type.PNG)
