import pytest

from app.recipes_app import steps
from app.recipes_app import searching_recipes
from app.recipes_app import requesting_ingredients
from app.recipes_app import requesting_instructions



def test_steps():
    result = steps()
    assert result in str(response.data)

def test_searching():
    result searching_recipes()
    assert result in str(response.data)

def test_ingredients():
    result test_ingredients()
    assert result in str(response.data)

def test_instructions():
    result requesting_instructions()
    assert result in str(response.data)    
