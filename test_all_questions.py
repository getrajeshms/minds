"""
Walks through the complete MindView assessment flow via Playwright,
answering every question with rating=1 (Mild) and capturing screenshots.
"""
import time
import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8501"
SHOT_DIR = "c:/Users/rajes/Documents/Python Projects/mindview_streamlit/screenshots"
shots = []


def ss(page, name):
    path = f"{SHOT_DIR}/{name}.png"
    page.screenshot(path=path)
    shots.append(name)
    print("  [screenshot] " + name)


def wait_ready(page):
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.7)


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

        # --- Welcome ---
        print("Step: Welcome")
        page.goto(BASE, wait_until="networkidle")
        wait_ready(page)
        ss(page, "01_welcome")
        click_btn(page, "Start New Assessment")
        ss(page, "02_patient_info")
        print("  Navigated to Patient Info")

        # --- Patient Info ---
        print("Step: Patient Info")
        page.get_by_label("Patient Name *").fill("Test Patient")
        page.get_by_label("Age *").fill("35")
        page.get_by_label("Interviewer Name *").fill("Dr. Test")

        gender_box = page.locator('[data-testid="stSelectbox"]').first
        gender_box.click()
        wait_ready(page)
        page.get_by_role("option", name="Male", exact=True).click()
        wait_ready(page)

        click_btn(page, "Continue")
        ss(page, "03_background")
        print("  Navigated to Background")

        # --- Background ---
        print("Step: Background")
        page.get_by_label("Present Problems *").fill("Patient reports persistent low mood and anxiety.")
        click_btn(page, "Continue")
        ss(page, "04_assessment_q1")
        print("  Navigated to Assessment")

        # --- Assessment: walk all questions ---
        print("Step: Assessment questions")
        q_count = 0

        while True:
            wait_ready(page)

            # Check if we landed on clinical judgement
            heading_els = page.locator("h3")
            heading = ""
            if heading_els.count() > 0:
                heading = heading_els.first.inner_text()
            if "Clinical" in heading:
                print("  Reached Clinical Judgement after %d questions" % q_count)
                break

            # Print step indicator
            indicator = page.locator(".step-indicator")
            step_txt = indicator.first.inner_text() if indicator.count() > 0 else "?"
            print("  Q%d: %s" % (q_count + 1, step_txt))

            # Select "Mild" (index 1) to activate follow-up branching
            radios = page.locator('[data-testid="stRadio"] label')
            if radios.count() >= 2:
                radios.nth(1).click()
                wait_ready(page)

            if q_count % 5 == 0:
                ss(page, "q_%03d" % (q_count + 1))

            q_count += 1

            # Navigate
            complete_btn = page.get_by_role("button", name="Complete Assessment")
            next_btn     = page.get_by_role("button", name="Next")

            if complete_btn.count() > 0:
                complete_btn.click()
                wait_ready(page)
                print("  Clicked Complete Assessment on Q%d" % q_count)
                break
            elif next_btn.count() > 0:
                next_btn.click()
                wait_ready(page)
            else:
                print("  WARNING: no navigation button found, stopping")
                ss(page, "stuck_q%d" % q_count)
                break

        ss(page, "05_clinical_judgement")

        # --- Clinical Judgement ---
        print("Step: Clinical Judgement")
        page.get_by_label("Clinical Judgement / Summary *").fill(
            "Patient presents with mild depressive and anxiety symptoms. No acute risk identified."
        )
        click_btn(page, "Generate Report")
        wait_ready(page)
        ss(page, "06_report")
        print("  Report generated")

        # --- Report checks ---
        print("Step: Report verification")
        errors = []

        if page.locator("text=GMHAT/PC Mental Health Assessment Report").count() == 0:
            errors.append("Report header not found")

        if page.locator("text=Test Patient").count() == 0:
            errors.append("Patient name missing from report")

        sym_rows = page.locator(".symptom-row")
        sym_count = sym_rows.count()
        print("  Symptom rows in report: %d" % sym_count)
        if sym_count == 0:
            errors.append("No symptom rows in report")

        # Try scrolling down to see more of the report
        page.evaluate("window.scrollBy(0, 600)")
        time.sleep(0.5)
        ss(page, "07_report_bottom")

        browser.close()

        # --- Summary ---
        print("\n" + "=" * 50)
        print("Questions answered : %d" % q_count)
        print("Symptom rows shown : %d" % sym_count)
        print("Screenshots taken  : %d" % len(shots))
        if errors:
            print("FAILURES (%d):" % len(errors))
            for e in errors:
                print("  FAIL: " + e)
        else:
            print("All checks PASSED")
        print("=" * 50)


if __name__ == "__main__":
    main()
