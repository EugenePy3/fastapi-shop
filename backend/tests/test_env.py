import os


def test_env():
    print("\nDATABASE_URL =", os.getenv("DATABASE_URL"))
    assert "shop_test" in os.getenv("DATABASE_URL")
