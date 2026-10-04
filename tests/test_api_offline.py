"""API wiring/serialization tests only; SQL and MySQL are NOT executed."""
from decimal import Decimal
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app


class ApiOfflineTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_openapi_routes_without_database(self):
        response = self.client.get("/v1/openapi.json")
        self.assertEqual(response.status_code, 200)
        paths = response.json()["paths"]
        for path in ("/v1/movie", "/v1/search", "/v1/user/{user_id}/rated"):
            self.assertIn(path, paths)

    def test_movie_list_pagination(self):
        with patch("movieLens.routers.get_movies", return_value=[{"movieId": 1}]) as query:
            response = self.client.get("/v1/movie?limit=2&offset=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"movieId": 1}])
        query.assert_called_once_with(2, 3)

    def test_detail_serializes_aggregate_and_genres(self):
        with patch("movieLens.routers.get_movie", return_value={"movieId": 1}), \
             patch("movieLens.routers.get_average_rating", return_value=Decimal("4.25")), \
             patch("movieLens.routers.get_movie_genre", return_value=[{"genre": "Comedy"}]):
            response = self.client.get("/v1/movie/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["avgRating"], 4.25)
        self.assertEqual(response.json()["genres"], [{"genre": "Comedy"}])

    def test_not_found_remains_404(self):
        with patch("movieLens.routers.get_movie", side_effect=HTTPException(404, "Movie not found")):
            response = self.client.get("/v1/movie/999999")
        self.assertEqual(response.status_code, 404)

    def test_frontend_cors_preflight(self):
        response = self.client.options("/v1/movie", headers={
            "Origin": "http://localhost:3001", "Access-Control-Request-Method": "GET"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], "http://localhost:3001")


if __name__ == "__main__":
    unittest.main(verbosity=2)
