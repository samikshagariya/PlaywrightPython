from playwright.sync_api import Page, expect

from data.test_data import (
    BASE_URL,
    TIMEOUT,
    USER_DATA,
)


def register_new_user(page: Page, email: str):
    """Register a new user and verify login."""

    # Open the website.
    page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=TIMEOUT,
    )

    expect(
        page.locator(
            'img[alt="Website for automation practice"]'
        )
    ).to_be_visible(timeout=TIMEOUT)

    # Open the Signup/Login page.
    page.locator('a[href="/login"]').click()

    expect(
        page.locator(".signup-form h2")
    ).to_have_text("New User Signup!")

    # Enter name and unique email.
    page.locator(
        '[data-qa="signup-name"]'
    ).fill(USER_DATA["name"])

    page.locator(
        '[data-qa="signup-email"]'
    ).fill(email)

    page.locator(
        '[data-qa="signup-button"]'
    ).click()

    # Verify the account-information form.
    expect(
    page.get_by_role(
        "heading",
        name="Enter Account Information",
        exact=True,
    )
).to_be_visible(timeout=TIMEOUT)

    # Select title.
    if USER_DATA["title"] == "Mrs":
        page.locator("#id_gender2").check()
    else:
        page.locator("#id_gender1").check()

    # Enter password and date of birth.
    page.locator(
        '[data-qa="password"]'
    ).fill(USER_DATA["password"])

    page.locator("#days").select_option(
        USER_DATA["birth_day"]
    )

    page.locator("#months").select_option(
        USER_DATA["birth_month"]
    )

    page.locator("#years").select_option(
        USER_DATA["birth_year"]
    )

    # Select the newsletter options.
    page.locator("#newsletter").check()
    page.locator("#optin").check()

    # Enter address information.
    form_fields = {
        "first_name": USER_DATA["first_name"],
        "last_name": USER_DATA["last_name"],
        "company": USER_DATA["company"],
        "address": USER_DATA["address"],
        "address2": USER_DATA["address_2"],
        "state": USER_DATA["state"],
        "city": USER_DATA["city"],
        "zipcode": USER_DATA["zipcode"],
        "mobile_number": USER_DATA["mobile_number"],
    }

    for field_name, value in form_fields.items():
        page.locator(
            f'[data-qa="{field_name}"]'
        ).fill(value)

    page.locator(
        '[data-qa="country"]'
    ).select_option(USER_DATA["country"])

    # Create the account.
    page.locator(
        '[data-qa="create-account"]'
    ).click()

    expect(
        page.locator(
            '[data-qa="account-created"]'
        )
    ).to_be_visible(timeout=TIMEOUT)

    page.locator(
        '[data-qa="continue-button"]'
    ).click()

    # Verify successful login.
    expect(
        page.locator(
            'a:has-text("Logged in as")'
        )
    ).to_contain_text(
        USER_DATA["name"],
        timeout=TIMEOUT,
    )


def delete_test_account(page: Page):
    """Delete the temporary account created by the test."""

    delete_link = page.locator(
        'a[href="/delete_account"]'
    )

    # Do nothing if registration was not completed.
    if not delete_link.is_visible():
        return

    delete_link.click()

    expect(
        page.locator(
            '[data-qa="account-deleted"]'
        )
    ).to_be_visible(timeout=TIMEOUT)

    continue_button = page.locator(
        '[data-qa="continue-button"]'
    )

    if continue_button.is_visible():
        continue_button.click()