"""全局 pytest fixture。

浏览器参数通过环境变量注入，便于在本地（有头）与 CI（无头）两种环境复用同一套用例。
"""
import os

import pytest
from playwright.sync_api import sync_playwright

# 有头/无头由 HEADLESS 环境变量决定，默认无头，避免 CI 环境因缺显示服务而启动失败
HEADLESS = os.getenv("HEADLESS", "1").lower() in ("1", "true", "yes")
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
BASE_URL = os.getenv("BASE_URL", "https://www.baidu.com")


@pytest.fixture(scope="session")
def browser_type():
    with sync_playwright() as p:
        yield p.chromium


@pytest.fixture(scope="function")
def browser(browser_type):
    browser = browser_type.launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO,
        args=["--disable-dev-shm-usage"],
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """独立浏览器上下文，隔离 cookie/storage，用例间互不污染。"""
    context = browser.new_context(base_url=BASE_URL, viewport={"width": 1440, "height": 900})
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """把每个阶段的执行结果挂到 item 上，供失败取证 fixture 判断。"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_{}".format(rep.when), rep)
    setattr(item, "rep_call_failed", rep.failed)


@pytest.fixture(scope="function", autouse=True)
def attach_on_failure(request):
    """用例失败时自动截图并打印页面 URL，作为最小取证。

    注意：不直接声明 page 参数——autouse fixture 的参数会立即触发浏览器启动，
    导致纯逻辑单测也被迫依赖 Playwright。这里改为失败后按需懒加载，
    且仅对真正使用 page 的 UI 用例生效。
    """
    yield
    if not getattr(request.node, "rep_call_failed", False):
        return
    if "page" not in request.fixturenames:
        return
    try:
        page = request.getfixturevalue("page")
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        report_dir = os.path.join(root, "Reports", "screenshots")
        os.makedirs(report_dir, exist_ok=True)
        shot = page.screenshot(full_page=True)
        name = request.node.name.replace("/", "_")[:80]
        with open(os.path.join(report_dir, "{}.png".format(name)), "wb") as f:
            f.write(shot)
        print("\n[attach] 失败截图: Reports/screenshots/{}.png".format(name))
        print("[attach] 失败页面 URL: {}".format(page.url))
    except Exception as exc:  # 取证失败不得掩盖原始失败
        print("[attach] 截图取证失败: {}".format(exc))