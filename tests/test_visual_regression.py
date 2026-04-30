import pytest
from playwright.sync_api import sync_playwright
import os
from PIL import Image, ImageChops, ImageFilter

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


def images_are_similar(img1_path, img2_path, threshold=5000):
    img1 = Image.open(img1_path).convert('RGB').filter(ImageFilter.GaussianBlur(1))
    img2 = Image.open(img2_path).convert('RGB').filter(ImageFilter.GaussianBlur(1))
    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()
    if not bbox:
        return True
    hist = diff.histogram()
    diff_sum = sum(hist)
    return diff_sum < threshold


def visual_regression_test(page, name, url, extra_actions=None, threshold=5000):
    page.goto(url)
    if extra_actions:
        extra_actions(page)
    screenshot_path = os.path.join(CURRENT_DIR, f'{name}.png')
    baseline_path = os.path.join(BASELINE_DIR, f'{name}.png')

    page.screenshot(path=screenshot_path, full_page=True)

    if not os.path.exists(baseline_path):
        page.screenshot(path=baseline_path, full_page=True)
        pytest.skip(f"Baseline image for {name} did not exist, created new baseline.")

    assert os.path.exists(screenshot_path), "Screenshot was not created."
    assert os.path.exists(baseline_path), "Baseline screenshot is missing."

    assert images_are_similar(screenshot_path, baseline_path, threshold=threshold), f"Visual regression detected for {name}."


# Helper function to enable dark mode

def enable_dark_mode(page):
    page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")

# Helper function for mobile viewport

def set_mobile_viewport(page):
    page.set_viewport_size({"width": 375, "height": 812})  # Typical iPhone X dimensions


# Test multiple key UI states

def test_homepage_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'homepage', "http://localhost:8000")


def test_error_page_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'error_page', "http://localhost:8000/nonexistent")


def test_login_page_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'login_page', "http://localhost:8000/login")


def test_dashboard_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'dashboard', "http://localhost:8000/dashboard")


def test_user_profile_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'user_profile', "http://localhost:8000/profile")


def test_settings_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'settings', "http://localhost:8000/settings")


def test_checkout_flow_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'checkout_flow', "http://localhost:8000/checkout")


# New tests for dark mode

def test_homepage_dark_mode_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'homepage_dark_mode', "http://localhost:8000", extra_actions=enable_dark_mode)


def test_dashboard_dark_mode_visual_regression(browser_context):
    page = browser_context.new_page()
    visual_regression_test(page, 'dashboard_dark_mode', "http://localhost:8000/dashboard", extra_actions=enable_dark_mode)


# New test for mobile viewport

def test_homepage_mobile_viewport_visual_regression(browser_context):
    page = browser_context.new_page()
    def actions(page):
        set_mobile_viewport(page)
    visual_regression_test(page, 'homepage_mobile', "http://localhost:8000", extra_actions=actions)


# New test for interactive components

def test_modal_dialog_visual_regression(browser_context):
    page = browser_context.new_page()
    def actions(page):
        page.goto("http://localhost:8000")
        page.click('#openModalButton')  # Assuming there is a button to open modal
    visual_regression_test(page, 'modal_dialog', "http://localhost:8000", extra_actions=actions)


# Additional tests for other important UI states can be added similarly
