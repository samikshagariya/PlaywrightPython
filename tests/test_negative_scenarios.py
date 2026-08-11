import pytest
from playwright.sync_api import Page

from data.test_data import (
    create_nonexistent_product_name,
    create_unique_email,
)
from pages.login_page import (
    login_with_invalid_credentials,
)
from pages.product_page import (
    search_for_nonexistent_product,
)


@pytest.mark.negative
def test_login_with_invalid_credentials(
    page: Page,
):
    """
    Verify that an unregistered user
    cannot log in.
    """

    invalid_email = create_unique_email(
        prefix="invalid_user"
    )

    login_with_invalid_credentials(
        page,
        invalid_email,
    )


@pytest.mark.negative
@pytest.mark.search
def test_search_for_nonexistent_product(
    page: Page,
):
    """
    Verify that searching for a random
    nonexistent product returns no results.
    """

    nonexistent_product = (
        create_nonexistent_product_name()
    )

    search_for_nonexistent_product(
        page,
        nonexistent_product,
    )