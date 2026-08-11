from pathlib import Path

import pytest
from playwright.sync_api import Page

from data.test_data import create_unique_email
from pages.cart_page import (
    add_product_and_open_cart,
    proceed_to_checkout,
    verify_cart,
)
from pages.checkout_page import (
    complete_payment,
    download_invoice,
    place_order,
    verify_checkout_addresses,
)
from pages.product_page import (
    search_and_open_product,
)
from pages.registration_page import (
    delete_test_account,
    register_new_user,
)


@pytest.mark.e2e
def test_complete_purchase_journey(
    page: Page,
    tmp_path: Path,
):
    """
    Complete journey:

    Registration
        ↓
    Product search
        ↓
    Cart
        ↓
    Checkout
        ↓
    Payment
        ↓
    Invoice download
        ↓
    Account deletion
    """

    email = create_unique_email()

    try:
        # Step 1: Register a new user.
        register_new_user(
            page,
            email,
        )

        # Step 2: Search for Blue Top
        # and verify its details.
        search_and_open_product(page)

        # Step 3: Set quantity and add
        # the product to the cart.
        add_product_and_open_cart(page)

        # Step 4: Verify cart values.
        verify_cart(page)

        # Step 5: Continue to checkout.
        proceed_to_checkout(page)

        # Step 6: Verify delivery and
        # billing addresses.
        verify_checkout_addresses(page)

        # Step 7: Add a comment and
        # open the Payment page.
        place_order(page)

        # Step 8: Complete payment.
        complete_payment(page)

        # Step 9: Download and verify
        # the invoice.
        download_invoice(
            page,
            tmp_path,
        )

    finally:
        # Delete the temporary account,
        # even if a later test step fails.
        delete_test_account(page)