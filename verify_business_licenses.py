from playwright.sync_api import sync_playwright
import time

def verify_business_licenses():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Login
            page.goto("http://127.0.0.1:5000/login")
            page.fill("input[name='dni']", "12345678A") # Assuming this user exists from previous test setup or manual creation
            page.fill("input[name='password']", "password")
            # In login.html, the button is just <button type="submit"> not <input type="submit">
            page.click("button[type='submit']")

            # Wait for navigation
            page.wait_for_url("**/citizen/dashboard")

            # 2. Go to Licenses
            page.goto("http://127.0.0.1:5000/licenses")

            # 3. Open Business Modal
            # Click "Licencias de Negocio" tab
            page.click("#business-tab")
            time.sleep(1)

            # Find the button to open modal.
            # In template: <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#businessModal">
            # or <button class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#businessModal">

            # Use attribute selector for robustness
            page.click("[data-bs-target='#businessModal']")

            # Wait for modal to be visible
            page.wait_for_selector("#businessModal", state='visible')
            time.sleep(1) # Wait for bootstrap animation

            # 4. Fill form and check cost updates

            # Select "Bar"
            page.select_option("#businessTypeSelect", "Bar")
            time.sleep(0.5)

            # Check cost display
            # Base 5500 + Alcohol 3500 + Night 3500 = 12500
            content = page.text_content("#costEstimateContainer")
            print(f"Bar Content: {content}")
            if "$12500" not in content:
                print("ERROR: Expected $12500 for Bar")

            # Take screenshot of Bar estimate
            page.screenshot(path="/home/jules/verification/bar_estimate.png")

            # Select "Mechanic"
            page.select_option("#businessTypeSelect", "Mechanic")
            time.sleep(0.5)

            # Check cost display
            # Base 5500
            content = page.text_content("#costEstimateContainer")
            print(f"Mechanic Content: {content}")
            if "$5500" not in content:
                print("ERROR: Expected $5500 for Mechanic")

            # Take screenshot of Mechanic estimate
            page.screenshot(path="/home/jules/verification/mechanic_estimate.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_business_licenses()
