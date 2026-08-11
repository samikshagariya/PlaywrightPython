from pathlib import Path

from playwright.sync_api import Page, expect

from data.test_data import (
    ORDER_COMMENT,
    PAYMENT_DATA,
    TIMEOUT,
    USER_DATA,
)


def verify_checkout_addresses(page: Page):
    """Verify delivery and billing information."""

    delivery_address = page.locator(
        "#address_delivery"
    )

    billing_address = page.locator(
        "#address_invoice"
    )

    expect(
        delivery_address
    ).to_be_visible(timeout=TIMEOUT)

    expect(
        billing_address
    ).to_be_visible(timeout=TIMEOUT)

    # Important values that should appear
    # in both addresses.
    expected_values = [
        USER_DATA["first_name"],
        USER_DATA["last_name"],
        USER_DATA["address"],
        USER_DATA["city"],
        USER_DATA["state"],
        USER_DATA["zipcode"],
        USER_DATA["country"],
        USER_DATA["mobile_number"],
    ]

    for value in expected_values:
        expect(
            delivery_address
        ).to_contain_text(value)

        expect(
            billing_address
        ).to_contain_text(value)


def place_order(page: Page):
    """Add an order comment and continue to payment."""

    page.locator(
        'textarea[name="message"]'
    ).fill(ORDER_COMMENT)

    page.locator(
        'a[href="/payment"]'
    ).click()

    # A role locator avoids matching duplicate Payment text.
    expect(
        page.get_by_role(
            "heading",
            name="Payment",
            exact=True,
        )
    ).to_be_visible(timeout=TIMEOUT)


def complete_payment(page: Page):
    """Enter dummy payment information and place the order."""

    page.locator(
        '[data-qa="name-on-card"]'
    ).fill(PAYMENT_DATA["name_on_card"])

    page.locator(
        '[data-qa="card-number"]'
    ).fill(PAYMENT_DATA["card_number"])

    page.locator(
        '[data-qa="cvc"]'
    ).fill(PAYMENT_DATA["cvc"])

    page.locator(
        '[data-qa="expiry-month"]'
    ).fill(PAYMENT_DATA["expiry_month"])

    page.locator(
        '[data-qa="expiry-year"]'
    ).fill(PAYMENT_DATA["expiry_year"])

    page.locator(
        '[data-qa="pay-button"]'
    ).click()

    expect(
        page.locator(
            '[data-qa="order-placed"]'
        )
    ).to_be_visible(timeout=TIMEOUT)

    expect(
    page.locator(
        '[data-qa="order-placed"]'
    )
).to_have_text(
    "Order Placed!",
    timeout=TIMEOUT,
)


def download_invoice(
    page: Page,
    download_folder: Path,
):
    """
    Download the invoice and verify that
    the downloaded file is not empty.
    """

    with page.expect_download(
        timeout=TIMEOUT
    ) as download_information:

        page.get_by_role(
            "link",
            name="Download Invoice",
        ).click()

    download = download_information.value

    invoice_path = (
        download_folder
        / download.suggested_filename
    )

    download.save_as(str(invoice_path))

    assert invoice_path.exists(), (
        "The invoice was not downloaded."
    )

    assert invoice_path.stat().st_size > 0, (
        "The downloaded invoice is empty."
    )

    # Return to the home page.
    page.locator(
        '[data-qa="continue-button"]'
    ).click()

    return invoice_path