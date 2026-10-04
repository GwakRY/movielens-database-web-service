"""Read-only HTTP checks after Docker DB initialization; no mocks."""
import argparse
import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8001")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    def get(path):
        with urlopen(base + path, timeout=30) as response:
            return json.load(response)

    movies = get("/v1/movie?limit=2")
    assert isinstance(movies, list) and 0 < len(movies) <= 2, "movie list is empty/invalid"
    movie = movies[0]
    detail = get(f"/v1/movie/{movie['movieId']}")
    assert detail["movieId"] == movie["movieId"] and isinstance(detail["genres"], list)
    assert "avgRating" in detail
    matches = get("/v1/search?" + urlencode({"query": movie["movieTitle"], "limit": 10}))
    assert any(row["movieId"] == movie["movieId"] for row in matches), "search mismatch"
    users = get("/v1/user?limit=1")
    assert users and get(f"/v1/user/{users[0]['userId']}")["userId"] == users[0]["userId"]
    ratings = get(f"/v1/user/{users[0]['userId']}/rated")
    assert ratings and "ratingScore" in ratings[0]
    try:
        get("/v1/movie/2147483647")
    except HTTPError as error:
        assert error.code == 404, f"unexpected status {error.code}"
    else:
        raise AssertionError("missing movie did not return 404")
    assert "/v1/movie" in get("/v1/openapi.json")["paths"]
    print("Live API checks passed: list, detail/aggregate, search, user, rated movies, 404, OpenAPI")


if __name__ == "__main__":
    main()
