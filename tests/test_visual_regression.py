import pytest
from playwright.sync_api import sync_playwright
import os
from PIL import Image, ImageChops

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


def images_are_similar(img1_path, img2_path, threshold=10):
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')
    diff = ImageChops.difference(img1, img2)
    # Calculate the bounding box of non-zero regions in the difference image
    bbox = diff.getbbox()
    if not bbox:
        return True
    # Calculate the diff histogram to quantify difference
    hist = diff.histogram()
    # Sum of differences
    diff_sum = sum(hist)
    return diff_sum < threshold


def visual_regression_test(page, name, url):
    page.goto(url)
    screenshot_path = os.path.join(CURRENT_DIR, f'{name}.png')
    baseline_path = os.path.join(BASELINE_DIR, f'{name}.png')

    page.screenshot(path=screenshot_path, full_page=True)

    if not os.path.exists(baseline_path):
        page.screenshot(path=baseline_path, full_page=True)
        pytest.skip(f"Baseline image for {name} did not exist, created new baseline.")

    assert os.path.exists(screenshot_path), "Screenshot was not created."
    assert os.path.exists(baseline_path), "Baseline screenshot is missing."

    assert images_are_similar(screenshot_path, baseline_path), f"Visual regression detected for {name}."


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


# Additional tests for other important UI states can be added similarly
