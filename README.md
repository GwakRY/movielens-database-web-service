# MovieLens Database Web Service

데이터베이스 전공 과목에서 진행한 웹 서비스 프로젝트입니다.  
MovieLens 데이터를 활용해 영화, 사용자, 평점, 장르 정보를 관계형 데이터베이스로 구성하고, SQL 기반 조회·검색·추천 데이터를 FastAPI REST API와 React 화면에 연동했습니다.

\---

## Project Overview

* **Backend**: FastAPI
* **Database**: MySQL
* **Database Driver**: PyMySQL
* **Frontend**: React
* **Main Focus**: 관계형 데이터 모델링, SQL 조회, 조건 기반 영화 데이터 제공, REST API 연동

\---

## Database Schema

주요 테이블은 다음과 같습니다.

### `movie`

영화 기본 정보를 저장합니다.

* `movieId` (PK)
* `movieTitle`
* `releaseDate`
* `videoReleaseDate`
* `IMDbURL`

### `user`

사용자 정보를 저장합니다.

* `userId` (PK)
* `age`
* `gender`
* `occupation`
* `ZIPCODE`

### `ratings`

사용자의 영화 평점 정보를 저장합니다.

* `ratingId` (PK)
* `userId` (FK → `user.userId`)
* `movieId` (FK → `movie.movieId`)
* `ratingScore`
* `timestamp`

### `movie\_genres`

영화별 장르 정보를 저장합니다.

* `mgenreId` (PK)
* `movieId` (FK → `movie.movieId`)
* `genre`

### Relationship

```text
user
  └──< ratings >── movie
                    └──< movie\_genres
```

\---

## Backend Structure

프로젝트는 FastAPI 기반으로 Router, Controller, Database Connector 계층을 나누어 구성했습니다.

```text
React Frontend
      │
      ▼
FastAPI Router
      │
      ▼
Controller
      │
      ▼
DatabaseConnector
      │
      ▼
MySQL
```

### DatabaseConnector

PyMySQL을 활용해 MySQL에 연결하고, 조회와 변경 쿼리를 분리했습니다.

* 환경변수 기반 DB 접속 정보 관리
* `DictCursor` 사용
* `query\_get()`을 통한 조회 쿼리 실행
* `query\_put()`을 통한 데이터 변경 및 commit 처리
* SQL parameter binding 적용

\---

## Main Features

### 1\. 영화 목록 조회

* 전체 영화 목록 조회
* `LIMIT` / `OFFSET` 기반 페이징
* 특정 연도 이전 영화 조회

사용 SQL 예시:

```sql
SELECT
    movieId,
    movieTitle,
    releaseDate,
    videoReleaseDate
FROM movie
LIMIT %s OFFSET %s;
```

\---

### 2\. 영화 상세 조회

특정 영화의 기본 정보와 함께 평균 평점, 장르, 사용자의 평가 정보를 조합해 제공합니다.

주요 처리:

* 영화 기본 정보 조회
* `AVG()` 기반 평균 평점 계산
* 영화 장르 조회
* 사용자 ID가 전달된 경우 해당 사용자의 평점 정보 추가

\---

### 3\. 영화 검색

영화 제목을 기준으로 검색합니다.

```sql
WHERE movieTitle LIKE %s
```

사용자 입력은 parameter binding 방식으로 전달했습니다.

\---

### 4\. 사용자별 평가 영화 조회

`movie`와 `ratings` 테이블을 JOIN하여 특정 사용자가 평가한 영화 목록을 조회합니다.

```sql
FROM movie
INNER JOIN ratings
    ON movie.movieId = ratings.movieId
WHERE ratings.userId = %s;
```

\---

### 5\. 동일 직업 사용자 기반 영화 조회

기준 사용자의 직업을 서브쿼리로 조회하고, 같은 직업을 가진 사용자들의 평가 데이터를 기준으로 영화 목록을 조회합니다.

주요 SQL 요소:

* `JOIN`
* Subquery
* `WHERE`
* `LIMIT`

\---

### 6\. 동일 연령 사용자 기반 영화 조회

기준 사용자의 나이를 서브쿼리로 조회하고, 동일 연령 사용자의 평가 데이터를 기반으로 영화 목록을 조회합니다.

주요 SQL 요소:

* `JOIN`
* Subquery
* 조건 기반 데이터 조회
* `LIMIT`

\---

### 7\. 사용자 평점 기반 추천 데이터 조회

사용자 간 평점 데이터를 활용한 SQL 기반 추천 데이터 조회 로직을 구현했습니다.

쿼리 내부에서 다음 요소를 사용합니다.

* `JOIN`
* `GROUP BY`
* `ORDER BY`
* `MAX()`
* Subquery
* 사용자 간 평점 비교 계산

\---

## REST API

주요 API는 다음과 같습니다.

### Movie

```text
GET /v1/movie
GET /v1/movie/before1950
GET /v1/movie/{movie\_id}
GET /v1/movie/{movie\_id}/rating
GET /v1/search
```

### User

```text
GET /v1/user
GET /v1/user/{user\_id}
GET /v1/user/{user\_id}/rated
GET /v1/user/{user\_id}/same\_occupation\_movies
GET /v1/user/{user\_id}/same\_age\_movies
GET /v1/user/{user\_id}/algorithm\_1
```

### Genre / Rating

```text
GET /v1/genre
GET /v1/genre/{genre\_id}
GET /v1/rating
GET /v1/rating/{rating\_id}
GET /v1/user/{user\_id}/movie/{movie\_id}/rating
```

\---

## Frontend

React에서 FastAPI REST API를 호출해 영화 및 사용자 데이터를 화면에 표시했습니다.

주요 화면 기능:

* 영화 목록
* 영화 상세
* 영화 제목 검색
* 사용자 평가 영화 목록
* 동일 연령 사용자 기반 영화 목록
* 동일 직업 사용자 기반 영화 목록
* 사용자 평점 기반 추천 데이터 목록
* 영화 평균 평점 및 장르 표시

\---

## SQL Concepts Used

* `SELECT`
* `WHERE`
* `INNER JOIN`
* `JOIN`
* Subquery
* `AVG()`
* `MAX()`
* `GROUP BY`
* `ORDER BY`
* `LIKE`
* `LIMIT`
* `OFFSET`

\---

## Tech Stack

* **Backend**: FastAPI
* **Database**: MySQL
* **Database Driver**: PyMySQL
* **Frontend**: React
* **Language**: Python, JavaScript, SQL
* **API**: REST API

\---

## Suggested Repository Structure

```text
movielens-database-web-service/
├── api/
│   ├── database/
│   │   └── connector.py
│   └── movieLens/
│       ├── controllers.py
│       ├── models.py
│       └── routers.py
├── frontend/
│   └── src/
│       └── pages/
├── movielens\_DDL.sql
└── README.md
```

\---

## Environment Variables

DB 접속 정보는 환경변수에서 읽도록 구성되어 있습니다.

```text
DATABASE\_HOST
DATABASE\_USERNAME
DATABASE\_PASSWORD
DATABASE
DATABASE\_PORT
```

\---

## What I Learned

* PK·FK를 활용한 관계형 데이터 모델 구성
* 테이블 간 관계를 고려한 JOIN 쿼리 작성
* 서브쿼리와 집계 함수를 활용한 조건 기반 데이터 조회
* PyMySQL을 활용한 FastAPI–MySQL 연동
* SQL 결과를 REST API로 제공하고 React 화면에 연결하는 흐름
* 사용자 특성을 기준으로 데이터를 조회하는 추천 데이터 처리 방식

\---

