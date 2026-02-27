from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000/register")

    # Fill in the form just to show it works
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "Citizen")
    page.fill('input[name="dni"]', "A12345678")

    # Assertions
    # 1. No file inputs
    file_inputs = page.locator('input[type="file"]')
    count = file_inputs.count()
    if count == 0:
        print("✅ No file inputs found.")
    else:
        print(f"❌ Found {count} file inputs (should be 0).")

    # 2. Check DNI Note
    note = page.locator('.dni-note')
    if note.is_visible():
        print("✅ DNI Note is visible.")
        if "Debes colocar 'A' delante" in note.inner_text():
            print("✅ DNI Note text is correct.")
        else:
            print("❌ DNI Note text is incorrect.")
    else:
        print("❌ DNI Note is not visible.")

    page.screenshot(path="verification_register_form.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
