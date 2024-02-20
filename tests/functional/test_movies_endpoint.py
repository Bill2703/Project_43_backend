import json

# Testing the overall functionality - is the route rendering the correct data?
def test_index_page(client):
    response = client.get("/") 
    expected_data = b'{\n  "message": "Welcome to the Reddy 43 - Movies Application",\n  "description": "Movies API",\n  "endpoints": [\n    "GET / 200|500",\n    "GET /movies",\n    "GET /movies/<int:id>",\n    "GET /movies/top",\n    "GET /movies/recent",\n    "GET /genres"\n  ]\n}\n'
    
    print("response_data =", response.data)

    assert response.status_code == 200    
    assert response.data == expected_data

# GET /movies
def test_movies_page(client):
    response = client.get("/movies")
    assert response.status_code == 200
    data = json.loads(response.data)
    print("type of data=",type(data))
    assert type(data) == list
    assert len(data) > 1