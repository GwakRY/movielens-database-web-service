from fastapi import HTTPException, status
from database.connector import DatabaseConnector


# Movie Controllers


def get_movies(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return movies
	
def get_before_1950_movies(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		WHERE year<1950
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return movies
	

def get_movie(id: int) -> dict:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		WHERE movie.movieId = %s
		""",
		(id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
	return movies[0]


def get_movie_rating(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.movieId = %s
		""",
		(movie_id),
	)
	if len(ratings) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
	return ratings


def get_average_rating(movie_id: int) -> float:
	database = DatabaseConnector()
	rating = database.query_get(
		"""
		SELECT
			AVG(ratings.ratingScore)
		AS average_rating
		FROM ratings
		WHERE ratings.movieId = %s
		""",
		(movie_id),
	)
	if len(rating) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ratings found for this movie")
	return rating[0]['average_rating']


def get_movie_genre(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		WHERE movie_genres.movieId = %s
		""",
		(movie_id),
	)
	if len(genres) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
	return genres


def search_movies(query: str, limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		WHERE movie.movieTitle LIKE %s
		LIMIT %s OFFSET %s
		""",
		(f"%{query}%", limit, offset),
	)
	return movies


# User Controllers


def get_users(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	users = database.query_get(
		"""
		SELECT
			user.userId,
			user.age,
			user.gender,
			user.occupation,
			user.ZIPCODE
		FROM user
		LIMIT %s OFFSET %s;
		""",
		(limit, offset),
	)
	return users


def get_user(id: int) -> dict:
	database = DatabaseConnector()
	users = database.query_get(
		"""
		SELECT
			user.userId,
			user.age,
			user.gender,
			user.occupation,
			user.ZIPCODE
		FROM user
		WHERE user.userId = %s
		""",
		(id),
	)
	if len(users) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return users[0]


def get_user_rated_movies(user_id: int) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path,
			ratings.ratingScore,
			ratings.timestamp
		FROM movie
		INNER JOIN ratings ON movie.movieId = ratings.movieId
		WHERE ratings.userId = %s
		
		""",
		(user_id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
	return movies

# 1. user와 같은 직업 top10 무비 리스트 sql query문
def get_user_same_occupation_rated_movies(user_id: int) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
SELECT 
    m.movieId,
	m.movieTitle,
	m.releaseDate,
	m.videoReleaseDate,
	m.year, 
	m.backdrop_path,
	m.poster_path,
	r.ratingScore,
	r.timestamp
FROM 
    ratings r
    JOIN movie m ON r.movieId = m.movieId
    JOIN user u ON r.userId = u.userId
WHERE 
    u.occupation = (
        SELECT 
            occupation
        FROM 
            user
        WHERE 
            userId = %s
    )
LIMIT 10;
		""",
		(user_id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
	return movies

# 2. 유저와 같은나이 top10 리스트
def get_user_same_age_rated_movies(user_id: int) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
SELECT 
    m.movieId,
	m.movieTitle,
	m.releaseDate,
	m.videoReleaseDate,
	m.year, 
	m.backdrop_path,
	m.poster_path,
	r.ratingScore,
	r.timestamp
FROM 
    ratings r
    JOIN movie m ON r.movieId = m.movieId
    JOIN user u ON r.userId = u.userId
WHERE 
    u.age = (
        SELECT 
            age
        FROM 
            user
        WHERE 
            userId = %s
    )
LIMIT 10;		
		""",
		(user_id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
	return movies


# 3.유저1 협업 필터링 알고리즘
def get_user_algorithm_1_movies(user_id: int) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
    m.movieId,
	m.movieTitle,
	m.releaseDate,
	m.videoReleaseDate,
	m.year, 
	m.backdrop_path,
	m.poster_path,
	r1.ratingScore,
	r1.timestamp
FROM
    (
        SELECT
            r1.movieId,
            MAX(r1.ratingScore) AS max_rating_score
        FROM
            ratings r1
            JOIN (
                SELECT
                    user1,
                    user2,
                    similarity
                FROM
                    (
                        SELECT
                            u1.userId AS user1,
                            u2.userId AS user2,
                            ROUND(
                                SUM(
                                    POWER(r1.ratingScore - r2.ratingScore, 2)
                                ) / (
                                    SUM(r1.ratingScore * r1.ratingScore) *
                                    SUM(r2.ratingScore * r2.ratingScore)
                                ),
                                2
                            ) AS similarity
                        FROM
                            ratings r1
                            JOIN ratings r2 ON r1.movieId = r2.movieId
                            JOIN user u1 ON r1.userId = u1.userId
                            JOIN user u2 ON r2.userId = u2.userId
                        WHERE
                            u1.userId < u2.userId
                        GROUP BY
                            u1.userId, u2.userId
                        ORDER BY
                            similarity DESC
                    ) t
                WHERE
                    user1 = 1
            ) s ON r1.userId = s.user1
        WHERE
            r1.userId = 1
        GROUP BY
            r1.movieId
        ORDER BY
            max_rating_score DESC
        LIMIT 10
    ) t
    JOIN movie m ON t.movieId = m.movieId
    JOIN ratings r1 ON t.movieId = r1.movieId AND r1.userId = %s
ORDER BY
    r1.ratingScore DESC
LIMIT 10;
		""",
		(user_id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
	return movies



# Genre Controllers


def get_genres(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return genres


def get_genre(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		WHERE movie_genres.mgenreId = %s
		""",
		(movie_id),
	)
	if len(genres) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
	return genres


# Rating Controllers


def get_ratings(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return ratings


def get_rating(id: int) -> dict:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.ratingId = %s
		""",
		(id),
	)
	if len(ratings) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
	return ratings[0]


def get_user_movie_rating(user_id: int, movie_id: int) -> dict:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.userId = %s AND ratings.movieId = %s
		""",
		(user_id, movie_id),
	)
	if len(ratings) == 0:
		return None
	return ratings[0]
