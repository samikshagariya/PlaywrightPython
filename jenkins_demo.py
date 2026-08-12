from pathlib import Path
from playwright.sync_api import sync_playwright


def run_test():

    screenshot_folder = Path("jenkins_screenshots")
    screenshot_folder.mkdir(exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        print("Opening SauceDemo...")
        page.goto("https://www.saucedemo.com/")

        print("Entering login details...")

        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")

        print("Logging in...")

        page.locator("#login-button").click()

        assert "inventory.html" in page.url

        print("Login successful.")

        page.screenshot(
            path="jenkins_screenshots/login_success.png",
            full_page=True
        )

        print("Screenshot saved.")
        print("Playwright automation automatically executed after GitHub update.")

        browser.close()


if __name__ == "__main__":
    run_test()