from time import time_ns


# Main website URL
BASE_URL = "https://automationexercise.com"


# Common timeout used for slower website responses
TIMEOUT = 15000


# Registration and address information
USER_DATA = {
    "name": "Samiksha",
    "password": "Test@12345",
    "title": "Mrs",
    "birth_day": "15",
    "birth_month": "5",
    "birth_year": "2000",
    "first_name": "Samiksha",
    "last_name": "Test",
    "company": "Test Company",
    "address": "123 Test Street",
    "address_2": "Near Test Market",
    "country": "India",
    "state": "Uttarakhand",
    "city": "Dehradun",
    "zipcode": "248001",
    "mobile_number": "9876543210",
}


# Product used in the complete purchase journey
PRODUCT_DATA = {
    "id": "1",
    "name": "Blue Top",
    "price": "Rs. 500",
    "quantity": 2,
    "category": "Women > Tops",
    "availability": "In Stock",
    "condition": "New",
    "brand": "Polo",
}


# Dummy payment information for the practice website
PAYMENT_DATA = {
    "name_on_card": "Samiksha",
    "card_number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}


# Comment added during checkout
ORDER_COMMENT = (
    "Please deliver this test order safely."
)


# Incorrect password used in the negative login test
INVALID_PASSWORD = "WrongPassword123"


def create_unique_email(prefix="samiksha"):
    """
    Creates a new email every time the tests run.

    This prevents the registration test from failing
    because of an already registered email address.
    """
    return f"{prefix}_{time_ns()}@test.com"


def create_nonexistent_product_name():
    """
    Creates a product name that should not exist.

    It is used in the negative product-search test.
    """
    return f"ProductThatDoesNotExist{time_ns()}"