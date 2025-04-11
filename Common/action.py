# 复杂操作封装

from playwright.sync_api import Page

def click_fill(page: Page, selector: str, text: str):
    """点击元素后输入内容"""
    page.click(selector)
    page.fill(selector, text)

def drag_and_drop(page: Page, source: str, target: str):
    """拖拽元素操作"""
    page.drag_and_drop(source, target)