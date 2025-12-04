"""
Pytest configuration file.

Defines fixtures and test configuration for the entire test suite.
"""

import pytest


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "auth: mark test as authentication related"
    )
    config.addinivalue_line(
        "markers", "search: mark test as search related"
    )
    config.addinivalue_line(
        "markers", "booking: mark test as booking related"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
