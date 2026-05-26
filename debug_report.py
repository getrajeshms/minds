"""Debug script: navigate directly to the report and capture the full page."""
import time
import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8501"
SHOT_DIR = "c:/Users/rajes/Documents/Python Projects/mindview_streamlit/screenshots"


def wait_ready(page):
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(1.2)


def click_btn(page, label):
    btn = page.get_by_role("button", name=label)
    btn.scroll_into_view_if_needed()
    btn.click()
    wait_ready(page)


def main():
    os.makedirs(SHOT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Navigate through all steps quickly
        page.goto(BASE, wait_until="networkidle")
        wait_ready(page)
        click_btn(page, "Start New Assessment")

        page.get_by_label("Patient Name *").fill("Test Patient")
        page.get_by_label("Age *").fill("35")
        page.get_by_label("Interviewer Name *").fill("Dr. Test")
        gender_box = page.locator('[data-testid="stSelectbox"]').first
        gender_box.click()
        wait_ready(page)
        page.get_by_role("option", name="Male", exact=True).click()
        wait_ready(page)
        click_btn(page, "Continue")

        page.get_by_label("Present Problems *").fill("Patient reports persistent low mood.")
        click_btn(page, "Continue")

        # Answer all questions
        while True:
            wait_ready(page)
            heading_els = page.locator("h3")
            if heading_els.count() > 0 and "Clinical" in heading_els.first.inner_text():
                break
            radios = page.locator('[data-testid="stRadio"] label')
            if radios.count() >= 2:
                radios.nth(1).click()
                wait_ready(page)
            complete_btn = page.get_by_role("button", name="Complete Assessment")
            next_btn = page.get_by_role("button", name="Next")
            if complete_btn.count() > 0:
                complete_btn.click()
                wait_ready(page)
                break
            elif next_btn.count() > 0:
                next_btn.click()

        # Clinical judgement
        page.get_by_label("Clinical Judgement / Summary *").fill("Mild depressive symptoms noted.")
        click_btn(page, "Generate Report")
        wait_ready(page)
        time.sleep(2)  # extra wait for full render

        # Full-page screenshot
        page.screenshot(path=f"{SHOT_DIR}/report_fullpage.png", full_page=True)
        print("Full-page screenshot saved")

        # Check what text is actually on the page
        body_text = page.locator("body").inner_text()
        print("\n--- Page text (first 3000 chars) ---")
        print(body_text[:3000])
        print("---")

        # Check for any Streamlit error elements
        errors = page.locator('[data-testid="stException"]')
        if errors.count() > 0:
            print("\nStreamlit exceptions found:")
            for i in range(errors.count()):
                print("  " + errors.nth(i).inner_text()[:300])
        else:
            print("\nNo Streamlit exceptions detected")

        browser.close()


if __name__ == "__main__":
    main()
