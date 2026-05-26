"""Capture report bottom half."""
import time, os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8501"
SHOT_DIR = "c:/Users/rajes/Documents/Python Projects/mindview_streamlit/screenshots"

def wait_ready(page):
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(1.0)

def click_btn(page, label):
    page.get_by_role("button", name=label).scroll_into_view_if_needed()
    page.get_by_role("button", name=label).click()
    wait_ready(page)

def sel_gender(page):
    page.locator('[data-testid="stSelectbox"]').first.click()
    wait_ready(page)
    page.get_by_role("option", name="Male", exact=True).click()
    wait_ready(page)

def main():
    os.makedirs(SHOT_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(BASE, wait_until="networkidle"); wait_ready(page)
        click_btn(page, "Start New Assessment")
        page.get_by_label("Patient Name *").fill("Test Patient")
        page.get_by_label("Age *").fill("35")
        page.get_by_label("Interviewer Name *").fill("Dr. Test")
        sel_gender(page)
        click_btn(page, "Continue")
        page.get_by_label("Present Problems *").fill("Persistent low mood and anxiety.")
        click_btn(page, "Continue")
        q = 0
        while True:
            wait_ready(page)
            h3 = page.locator("h3")
            if h3.count() > 0 and "Clinical" in h3.first.inner_text():
                break
            radios = page.locator('[data-testid="stRadio"] label')
            if radios.count() >= 2:
                radios.nth(1).click(); wait_ready(page)
            q += 1
            if page.get_by_role("button", name="Complete Assessment").count() > 0:
                page.get_by_role("button", name="Complete Assessment").click()
                wait_ready(page); break
            elif page.get_by_role("button", name="Next").count() > 0:
                page.get_by_role("button", name="Next").click()
        page.get_by_label("Clinical Judgement / Summary *").fill("Mild depressive symptoms.")
        click_btn(page, "Generate Report")
        wait_ready(page); time.sleep(3)

        # Take full page screenshot
        page.screenshot(path=SHOT_DIR + "/full_report.png", full_page=True)

        # Scroll to bottom 25% of page and screenshot
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight * 0.5)")
        time.sleep(0.5)
        page.screenshot(path=SHOT_DIR + "/report_mid.png")

        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(0.5)
        page.screenshot(path=SHOT_DIR + "/report_end.png")

        browser.close()
        print("done, q=%d" % q)

main()
