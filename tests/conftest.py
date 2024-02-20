# File where you will setup the test environment as well as anything that needs to be called before every test
# Fixture

import pytest
from application import create_app
from application.movies.models import Movie


# Fixture 
@pytest.fixture
def client():
    env = "TEST"
    # Initialise a test app
    app = create_app(env)
    
    # Create a test client to which we can make requests
    client = app.test_client()
    


    return client
