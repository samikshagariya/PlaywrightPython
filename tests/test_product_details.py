from pathlib import Path
import re

import allure
from playwright.sync_api import Page, expect


BASE_URL = "https://automationexercise.com"
TIMEOUT = 60_000


@allure.title("Verify First Product Details")
@allure.feature("Products")
@allure.story("View Product Information")
@allure.severity(allure.severity_level.NORMAL)
def test_verify_first_product_details(page: Page):
    """Verify the information displayed for the first product."""

    page.set_default_timeout(15_000)

    with allure.step("Open the Products page"):
        page.goto(
            f"{BASE_URL}/products",
            wait_until="domcontentloaded",
            timeout=TIMEOUT,
        )

        expect(
            page.get_by_role(
                "heading",
                name="All Products",
                exact=True,
            )
        ).to_be_visible()

    with allure.step("Open the first product"):
        first_product = page.locator(
            'a[href="/product_details/1"]'
        ).first

        first_product.scroll_into_view_if_needed()
        first_product.click()

        expect(page).to_have_url(
            re.compile(r"/product_details/1$")
        )

    with allure.step("Verify the product information"):
        product_information = page.locator(
            ".product-information"
        )

        expect(product_information).to_be_visible()

        expect(
            product_information.get_by_role(
                "heading",
                name="Blue Top",
                exact=True,
            )
        ).to_be_visible()

        expect(product_information).to_contain_text(
            "Category: Women > Tops"
        )
        expect(product_information).to_contain_text(
            "Rs. 500"
        )
        expect(product_information).to_contain_text(
            "Availability: In Stock"
        )
        expect(product_information).to_contain_text(
            "Condition: New"
        )
        expect(product_information).to_contain_text(
            "Brand: Polo"
        )

    with allure.step("Save and attach the screenshot"):
        screenshot_directory = Path("screenshots")
        screenshot_directory.mkdir(exist_ok=True)

        screenshot_path = (
            screenshot_directory
            / "product_details_passed.png"
        )

        screenshot = page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        allure.attach(
            screenshot,
            name="Verified product details",
            attachment_type=allure.attachment_type.PNG,
        )