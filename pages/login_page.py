from playwright.sync_api import Page, expect

from data.test_data import (
    BASE_URL,
    INVALID_PASSWORD,
    TIMEOUT,
)


def login_with_invalid_credentials(
    page: Page,
    email: str,
):
    """
    Attempt to log in using an unregistered
    email and an incorrect password.
    """

    # Open the website.
    page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=TIMEOUT,
    )

    # Open the Signup/Login page.
    page.locator(
        'a[href="/login"]'
    ).click()

    # Verify the login form.
    expect(
        page.locator(".login-form h2")
    ).to_have_text(
        "Login to your account"
    )

    # Enter invalid credentials.
    page.locator(
        '[data-qa="login-email"]'
    ).fill(email)

    page.locator(
        '[data-qa="login-password"]'
    ).fill(INVALID_PASSWORD)

    page.locator(
        '[data-qa="login-button"]'
    ).click()

    # Verify the expected error message.
    expect(
        page.locator(
            ".login-form form p"
        )
    ).to_have_text(
        "Your email or password is incorrect!",
        timeout=TIMEOUT,
    )

    # Confirm that the user was not logged in.
    expect(
        page.locator(
            'a[href="/logout"]'
        )
    ).to_have_count(0)