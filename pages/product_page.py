import re

from playwright.sync_api import Page, expect

from data.test_data import (
    BASE_URL,
    PRODUCT_DATA,
    TIMEOUT,
)


def open_products_page(page: Page):
    """Open the Products page."""

    page.goto(
        f"{BASE_URL}/products",
        wait_until="domcontentloaded",
        timeout=TIMEOUT,
    )

    expect(
        page.locator("h2.title.text-center")
    ).to_have_text(
        re.compile(
            r"ALL PRODUCTS",
            re.IGNORECASE,
        ),
        timeout=TIMEOUT,
    )


def search_product(page: Page, keyword: str):
    """
    Search for a product.

    The search is retried once because the public
    website occasionally responds slowly.
    """

    for attempt in range(2):
        page.locator(
            "#search_product"
        ).fill(keyword)

        page.locator(
            "#submit_search"
        ).click()

        try:
            expect(
                page.locator(
                    "h2.title.text-center"
                )
            ).to_have_text(
                re.compile(
                    r"SEARCHED PRODUCTS",
                    re.IGNORECASE,
                ),
                timeout=TIMEOUT,
            )

            return

        except AssertionError:
            # Raise the error if the second attempt fails.
            if attempt == 1:
                raise

            # Reload the Products page before retrying.
            open_products_page(page)


def search_and_open_product(page: Page):
    """Search for Blue Top and open its details page."""

    open_products_page(page)

    search_product(
        page,
        PRODUCT_DATA["name"],
    )

    product_card = page.locator(
        ".product-image-wrapper"
    ).filter(
        has_text=PRODUCT_DATA["name"]
    ).first

    expect(
        product_card
    ).to_be_visible(timeout=TIMEOUT)

    # Open the product using its stable product ID.
    page.locator(
        f'a[href="/product_details/{PRODUCT_DATA["id"]}"]'
    ).first.click()

    # Verify the product-details page.
    product_information = page.locator(
        ".product-information"
    )

    expect(
        product_information.locator("h2")
    ).to_have_text(PRODUCT_DATA["name"])

    expect(
        product_information
    ).to_contain_text(PRODUCT_DATA["price"])

    expect(
        product_information
    ).to_contain_text(PRODUCT_DATA["category"])

    expect(
        product_information
    ).to_contain_text(PRODUCT_DATA["availability"])

    expect(
        product_information
    ).to_contain_text(PRODUCT_DATA["condition"])

    expect(
        product_information
    ).to_contain_text(PRODUCT_DATA["brand"])


def search_for_nonexistent_product(
    page: Page,
    product_name: str,
):
    """Search for a product that should not exist."""

    open_products_page(page)

    search_product(
        page,
        product_name,
    )

    # Product cards should not be displayed.
    product_cards = page.locator(
        ".features_items .product-image-wrapper"
    )

    expect(
        product_cards
    ).to_have_count(
        0,
        timeout=TIMEOUT,
    )