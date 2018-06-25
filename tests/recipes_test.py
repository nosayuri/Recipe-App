import pytest

from app.recipes_app import steps

def test_steps():
    result = steps()
    assert result in str(response.data)
