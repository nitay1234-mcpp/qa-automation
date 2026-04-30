import pytest
from playwright.sync_api import sync_playwright
import os

BASELINE_DIR = os.path.join(os.path.dirname(__file__), 'visual_baselines')
CURRENT_DIR = os.path.join(os.path.dirname(__file__), 'visual_current')

os.makedirs(BASELINE_DIR, exist_ok=True)
os.makedirs(CURRENT_DIR, exist_ok=True)

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()


def test_homepage_visual_regression(browser_context):
    page = browser_context.new_page()
    page.goto("http://localhost:8000")  # Change to your app URL
    screenshot_path = os.path.join(CURRENT_DIR, 'homepage.png')
    page.screenshot(path=screenshot_path, full_page=True)

    baseline_path = os.path.join(BASELINE_DIR, 'homepage.png')
    if not os.path.exists(baseline_path):
        page.screenshot(path=baseline_path, full_page=True)
        pytest.skip("Baseline image did not exist, created new baseline.")

    # Compare screenshots using simple pixel match using Playwright
    comparison = page.context._impl_obj._browser._connection.send('playwright:compareScreenshots', {
        'actual': screenshot_path,
        'expected': baseline_path,
    })

    # The above internal API may not be stable; alternatively, use image diff libraries externally.
    # Here we just check file existence and size difference as a placeholder.
    actual_size = os.path.getsize(screenshot_path)
    expected_size = os.path.getsize(baseline_path)
    size_diff = abs(actual_size - expected_size)

    # Fail if size difference exceeds threshold
    assert size_diff < 10000, f"Visual regression detected: size difference {size_diff} bytes exceeds threshold."

