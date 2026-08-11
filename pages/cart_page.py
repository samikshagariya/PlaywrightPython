import re
from playwright.sync_api import Page, expect

from data.test_data import (
    BASE_URL,
    PRODUCT_DATA,
    TIMEOUT,
)


def add_product_and_open_cart(page: Page):
    """
    Set the product quantity, add it to the cart
    and open the Shopping Cart page.
    """

    quantity = PRODUCT_DATA["quantity"]

    # Set the required product quantity.
    quantity_input = page.locator("#quantity")

    quantity_input.fill(str(quantity))

    expect(
        quantity_input
    ).to_have_value(str(quantity))

    # Add the product to the cart.
    page.locator(
        "button.cart"
    ).click()

    # Verify the cart confirmation window.
    cart_modal = page.locator("#cartModal")

    expect(
        cart_modal
    ).to_be_visible(timeout=TIMEOUT)

    expect(
        cart_modal
    ).to_contain_text(
        "Your product has been added to cart."
    )

    # Open the cart from the confirmation window.
    cart_modal.locator(
        'a[href="/view_cart"]'
    ).click()


def verify_cart(page: Page):
    """
    Verify the product name, price, quantity
    and total amount shown in the cart.
    """

    product_id = PRODUCT_DATA["id"]
    expected_quantity = PRODUCT_DATA["quantity"]

    cart_row = page.locator(
        f"#product-{product_id}"
    )

    expect(
        cart_row
    ).to_be_visible(timeout=TIMEOUT)

    # Verify the product name.
    expect(
        cart_row.locator(
            ".cart_description h4 a"
        )
    ).to_have_text(PRODUCT_DATA["name"])

    # Verify the unit price.
    expect(
        cart_row.locator(
            ".cart_price p"
        )
    ).to_have_text(PRODUCT_DATA["price"])

    # Verify the quantity.
    expect(
        cart_row.locator(
            ".cart_quantity button"
        )
    ).to_have_text(str(expected_quantity))

    # Calculate the expected total.
    unit_price = int(
        PRODUCT_DATA["price"]
        .replace("Rs.", "")
        .strip()
    )

    expected_total = (
        f"Rs. {unit_price * expected_quantity}"
    )

    # Verify the total amount.
    expect(
        cart_row.locator(
            ".cart_total p"
        )
    ).to_have_text(expected_total)


def proceed_to_checkout(page: Page):
    """
    Open the checkout page.

    The navigation is retried once because the
    public website occasionally ignores the click.
    """

    for attempt in range(2):
        checkout_button = page.locator(
            "a.check_out"
        )

        expect(
            checkout_button
        ).to_be_visible(timeout=TIMEOUT)

        checkout_button.click()

        try:
            expect(page).to_have_url(
                re.compile(r".*/checkout"),
                timeout=TIMEOUT,
            )

            expect(
                page.locator("#address_delivery")
            ).to_be_visible(timeout=TIMEOUT)

            return

        except AssertionError:
            if attempt == 1:
                raise

            # Wait briefly before retrying.
            page.wait_for_timeout(2000)

            # Return to the cart while keeping
            # the same logged-in session.
            page.goto(
                f"{BASE_URL}/view_cart",
                wait_until="domcontentloaded",
                timeout=60000,
            )