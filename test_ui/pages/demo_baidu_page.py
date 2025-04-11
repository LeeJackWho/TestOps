from playwright.sync_api import Page
import allure
from test_ui.elements.demo_baidu_element import BaiduElements

class BaiduPage:
    def __init__(self, page: Page):
        self.page = page
        self.elements = BaiduElements()

    def navigate_to_baidu(self):
        self.page.goto("https://www.baidu.com")

    def search(self, keyword: str):
        self.page.fill(self.elements.search_input, keyword)
        self.page.click(self.elements.search_btn)
        # 添加等待搜索结果加载
        self.page.wait_for_load_state('networkidle')

    def get_first_result(self) -> str:
        # 添加等待和重试机制
        self.page.wait_for_selector(self.elements.first_result, timeout=5000)
        return self.page.text_content(self.elements.first_result) or ""
    
     # 添加截图方法
    def take_screenshot(self, name: str):
        """添加截图到Allure报告"""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name, allure.attachment_type.PNG)