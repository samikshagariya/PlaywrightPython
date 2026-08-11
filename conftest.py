import pytest
from playwright.sync_api import (
    Page,
    Route,
)

from data.test_data import TIMEOUT


# Advertisement and tracking domains
# blocked during test execution.
BLOCKED_DOMAINS = (
    "doubleclick.net",
    "googlesyndication.com",
    "google-analytics.com",
    "googletagmanager.com",
    "adservice.google.com",
)


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args,
):
    """
    Apply common settings to every
    Playwright browser context.
    """

    return {
        **browser_context_args,
        "viewport": {
            "width": 1366,
            "height": 768,
        },
        "ignore_https_errors": True,
    }


def block_unwanted_requests(route: Route):
    """Block advertisement and tracking requests."""

    request_url = route.request.url.lower()

    if any(
        domain in request_url
        for domain in BLOCKED_DOMAINS
    ):
        route.abort()
    else:
        route.continue_()


@pytest.fixture(autouse=True)
def configure_test_page(page: Page):
    """
    Configure Playwright's standard page fixture.

    Playwright remains responsible for closing the
    page and saving failure screenshots, traces
    and videos.
    """

    page.set_default_timeout(TIMEOUT)

    page.set_default_navigation_timeout(
        60000
    )

    page.route(
        "**/*",
        block_unwanted_requests,
    )

    yield