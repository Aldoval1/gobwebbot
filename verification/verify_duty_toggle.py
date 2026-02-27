
from playwright.sync_api import sync_playwright, expect

def verify_toggle_duty():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Login...")
        page.goto("http://127.0.0.1:5000/official/login")

        page.fill("input[name='badge_id']", "000")
        page.fill("input[name='password']", "admin123")
        page.click("button[type='submit']")

        page.wait_for_load_state("networkidle")
        print(f"Dashboard Title: {page.title()}")

        # Check for logout link as indicator of dashboard presence
        if not page.locator(".logout").is_visible():
             print("Dashboard not fully loaded or login failed.")
             print(page.content())
             browser.close()
             return

        # 3. Take screenshot before toggle
        page.screenshot(path="verification/dashboard_before.png")

        # 4. Find the Toggle Duty button by text content
        # "ENTRAR EN SERVICIO" or "SALIR DE SERVICIO"
        toggle_button = page.locator("button:has-text('EN SERVICIO'), button:has-text('DE SERVICIO')")

        # Wait for button
        try:
            toggle_button.wait_for(state="visible", timeout=5000)
            print("Toggle button found via text locator.")
        except:
             print("Toggle button NOT found via text locator.")
             print(page.content()) # Debug HTML
             browser.close()
             return

        # 5. Verify button is enabled initially
        expect(toggle_button).to_be_enabled()
        print("Toggle button is enabled.")

        # 6. Click logic verification
        print("Clicking toggle button...")
        toggle_button.click()

        # 7. Wait for navigation/reload
        page.wait_for_load_state("networkidle")
        print("Page reloaded.")

        # 8. Take screenshot after toggle
        page.screenshot(path="verification/dashboard_after.png")

        print("Verification script ran successfully.")
        browser.close()

if __name__ == "__main__":
    verify_toggle_duty()
