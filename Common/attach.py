# 结果处理（截图+Allure报告）

import allure
from playwright.sync_api import Page

def add_screenshot(page: Page, name: str = "步骤截图"):
    """添加截图到Allure报告"""
    screenshot = page.screenshot()
    allure.attach(screenshot, name, allure.attachment_type.PNG)

def add_text_log(content: str):
    """添加文本日志到报告"""
    allure.attach(content, "执行日志", allure.attachment_type.TEXT)