from playwright.sync_api import sync_playwright, expect
import time
import random

def verify_register_loading():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to registration page
        print("Navigating to http://127.0.0.1:5000/register")
        page.goto("http://127.0.0.1:5000/register")

        # Fill in dummy data
        dni = f"A{random.randint(100000, 999999)}"
        page.fill("input[name='first_name']", "Test")
        page.fill("input[name='last_name']", "User")
        page.fill("input[name='dni']", dni)
        page.fill("input[name='password']", "password123")
        page.fill("input[name='confirm_password']", "password123")

        # Intercept POST request to introduce delay
        def handle_route(route):
            if route.request.method == "POST":
                print("Intercepted POST /register, delaying for 2s...")
                time.sleep(2)
                route.continue_()
            else:
                route.continue_()

        page.route("**/register", handle_route)

        # Click submit
        submit_btn = page.locator("#submitBtn")
        print("Clicking submit button...")
        submit_btn.click()

        # Capture state immediately after click
        print("Checking assertions...")
        try:
            expect(submit_btn).to_be_disabled(timeout=2000)
            print("ASSERTION: Button disabled -> PASS")
        except Exception as e:
            print(f"ASSERTION: Button disabled -> FAIL: {e}")

        try:
            expect(submit_btn).to_contain_text("Registrando", timeout=2000)
            print("ASSERTION: Button text changed -> PASS")
        except Exception as e:
            print(f"ASSERTION: Button text changed -> FAIL: {e}")

        # Take screenshot of the loading state
        page.screenshot(path="verification/register_loading_state.png")
        print("Screenshot saved to verification/register_loading_state.png")

        browser.close()

if __name__ == "__main__":
    verify_register_loading()