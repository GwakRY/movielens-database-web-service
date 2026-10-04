# MovieLens Database Web Service

데이터베이스 전공 과목에서 진행한 웹 서비스 프로젝트입니다.  
MovieLens 데이터를 활용해 영화, 사용자, 평점, 장르 정보를 관계형 데이터베이스로 구성하고, SQL 기반 조회·검색·추천 데이터를 FastAPI REST API와 React 화면에 연동했습니다.

---

## Project Overview

* **Backend**: FastAPI
* **Database**: MySQL
* **Database Driver**: PyMySQL
* **Frontend**: React
* **Main Focus**: 관계형 데이터 모델링, SQL 조회, 조건 기반 영화 데이터 제공, REST API 연동

---

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

### `movie_genres`

영화별 장르 정보를 저장합니다.

* `mgenreId` (PK)
* `movieId` (FK → `movie.movieId`)
* `genre`

### Relationship

```text
user
  └──< ratings >── movie
                    └──< movie_genres
```

---

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
* `query_get()`을 통한 조회 쿼리 실행
* `query_put()`을 통한 데이터 변경 및 commit 처리
* SQL parameter binding 적용

---

## Main Features

### 1. 영화 목록 조회

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

---

### 2. 영화 상세 조회

특정 영화의 기본 정보와 함께 평균 평점, 장르, 사용자의 평가 정보를 조합해 제공합니다.

주요 처리:

* 영화 기본 정보 조회
* `AVG()` 기반 평균 평점 계산
* 영화 장르 조회
* 사용자 ID가 전달된 경우 해당 사용자의 평점 정보 추가

---

### 3. 영화 검색

영화 제목을 기준으로 검색합니다.

```sql
WHERE movieTitle LIKE %s
```

사용자 입력은 parameter binding 방식으로 전달했습니다.

---

### 4. 사용자별 평가 영화 조회

`movie`와 `ratings` 테이블을 JOIN하여 특정 사용자가 평가한 영화 목록을 조회합니다.

```sql
FROM movie
INNER JOIN ratings
    ON movie.movieId = ratings.movieId
WHERE ratings.userId = %s;
```

---

### 5. 동일 직업 사용자 기반 영화 조회

기준 사용자의 직업을 서브쿼리로 조회하고, 같은 직업을 가진 사용자들의 평가 데이터를 기준으로 영화 목록을 조회합니다.

주요 SQL 요소:

* `JOIN`
* Subquery
* `WHERE`
* `LIMIT`

---

### 6. 동일 연령 사용자 기반 영화 조회

기준 사용자의 나이를 서브쿼리로 조회하고, 동일 연령 사용자의 평가 데이터를 기반으로 영화 목록을 조회합니다.

주요 SQL 요소:

* `JOIN`
* Subquery
* 조건 기반 데이터 조회
* `LIMIT`

---

### 7. 사용자 평점 기반 추천 데이터 조회

사용자 간 평점 데이터를 활용한 SQL 기반 추천 데이터 조회 로직을 구현했습니다.

쿼리 내부에서 다음 요소를 사용합니다.

* `JOIN`
* `GROUP BY`
* `ORDER BY`
* `MAX()`
* Subquery
* 사용자 간 평점 비교 계산

---

## REST API

주요 API는 다음과 같습니다.

### Movie

```text
GET /v1/movie
GET /v1/movie/before1950
GET /v1/movie/{movie_id}
GET /v1/movie/{movie_id}/rating
GET /v1/search
```

### User

```text
GET /v1/user
GET /v1/user/{user_id}
GET /v1/user/{user_id}/rated
GET /v1/user/{user_id}/same_occupation_movies
GET /v1/user/{user_id}/same_age_movies
GET /v1/user/{user_id}/algorithm_1
```

### Genre / Rating

```text
GET /v1/genre
GET /v1/genre/{genre_id}
GET /v1/rating
GET /v1/rating/{rating_id}
GET /v1/user/{user_id}/movie/{movie_id}/rating
```

---

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

---

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

---

## Tech Stack

* **Backend**: FastAPI
* **Database**: MySQL
* **Database Driver**: PyMySQL
* **Frontend**: React
* **Language**: Python, JavaScript, SQL
* **API**: REST API

---

## Environment Variables

DB 접속 정보는 환경변수에서 읽도록 구성되어 있습니다.

```text
DATABASE_HOST
DATABASE_USERNAME
DATABASE_PASSWORD
DATABASE
DATABASE_PORT
```

---

## Build & Run

Docker Engine 또는 Docker Desktop과 **Docker Compose v2**가 필요합니다. 아래 명령은 저장소 최상위 디렉터리에서 실행합니다.

### 1. 환경변수 준비

```bash
cp mysql/local.env.example mysql/local.env
cp api/local.env.example api/local.env
cp frontend/local.env.example frontend/local.env
```

Windows에서는 파일을 복사한 뒤 이름에서 `.example`을 제거해도 됩니다.

- 예시 비밀번호는 로컬 데모용입니다. `mysql/local.env`의 비밀번호를 바꾸면 `api/local.env`의 DB 비밀번호도 맞춰 주세요.
- 컨테이너 내부 API는 `DATABASE_HOST=mysql`, `DATABASE_PORT=3306`을 사용합니다. 호스트에서 DB에 접속할 때는 `127.0.0.1:3307`입니다.
- 브라우저는 `REACT_APP_API_BASE_URL=http://localhost:8001`로 API에 접속합니다. `mysql` 같은 컨테이너 서비스 이름을 브라우저 주소에 사용하지 않습니다.
- `local.env`는 Git과 Docker 이미지 복사 대상에서 제외합니다.

### 2. 실행

```bash
docker compose config -q
docker compose up --build -d
docker compose ps
docker compose logs -f mysql api
```

DB 최초 실행 시 [dump.sql](mysql/db/dump.sql)이 자동 적재됩니다. DB의 네 테이블을 조회할 수 있게 된 뒤 API가 시작됩니다. 최초 적재에는 시간이 걸릴 수 있으며 로그 관찰은 `Ctrl+C`로 끝낼 수 있습니다.

| 대상 | 주소 |
|---|---|
| React 화면 | http://localhost:3001 |
| API 문서 | http://localhost:8001/v1/docs |
| 영화 목록 | http://localhost:8001/v1/movie?limit=2 |
| 영화 검색 | http://localhost:8001/v1/search?query=Toy |
| 호스트의 DB 접속 | 127.0.0.1:3307 |

화면의 User ID 입력은 데이터셋 사용자 선택 기능이며 비밀번호 기반 인증이 아닙니다. 이미지 표시는 외부 TMDB 이미지 호스트의 접근 상태에도 영향을 받습니다.

### 3. 실제 DB 연동 확인

DB와 API가 실행된 후 호스트의 Python 3에서:

```bash
python3 tests/check_live_api.py
```

[검증 스크립트](tests/check_live_api.py)는 실제 API를 호출해 영화 목록·상세/평균 평점·검색·사용자·평가 영화·404·OpenAPI를 확인합니다. 데이터를 수정하지 않습니다. 실패 시 API와 DB 로그를 확인하세요.

### 4. 종료와 데이터 유지

```bash
docker compose down
```

DB는 `movie_db` 볼륨에 남습니다. 덤프 자동 적재는 **빈 데이터 볼륨의 최초 실행**에만 수행됩니다. 기존 볼륨에서는 환경변수의 DB 비밀번호를 바꿔도 저장된 계정 비밀번호가 자동 변경되지 않습니다.

로컬 데모 DB를 완전히 삭제하고 초기화할 때만:

```bash
docker compose down -v
docker compose up --build -d
```

`down -v`는 해당 Compose 프로젝트의 DB 볼륨 데이터를 삭제합니다.

### 문제 확인

- 환경변수 파일 오류: 세 `local.env` 파일을 만들었는지 확인합니다.
- DB가 `unhealthy`: `docker compose logs mysql`에서 초기화·덤프 오류와 비밀번호 일치를 확인합니다.
- API 500: `docker compose logs api`와 DB 상태를 확인합니다.
- 포트 충돌: 기존 서비스를 종료하거나 Compose의 호스트 포트를 바꿉니다. API 포트를 바꾸면 프런트엔드 환경변수도 변경하고 다시 시작합니다.
- 화면 목록이 비어 있음: API 주소를 직접 열어 응답을 확인합니다. 프런트엔드 환경변수는 시작/빌드 시 반영됩니다.

### 이번 검증 범위

2026-10-04 후속 정리에서 다음을 확인했습니다.

| 항목 | 결과 |
|---|---|
| API Python 문법 검사 | 통과 |
| DB를 모의 처리한 API 테스트 | 5개 통과 |
| React 의존성 설치와 프로덕션 빌드 | 통과, Node 24.19.0 / npm 11.9.0 |
| Compose YAML·환경변수 예시 일관성 | 정적 확인 |
| Docker Compose 실제 기동 | 미검증: 검증 환경에 Docker 없음 |
| 실제 MySQL 덤프 적재와 API 통합 | 미검증: 검증 환경에 MySQL 없음 |
| 실제 브라우저 화면 동작 | 미검증 |

오프라인 API 테스트는 SQL을 실행하지 않으며 DB 연동 성공의 근거가 아닙니다. 재실행:

```bash
python3 -m pip install -r api/requirements.txt -r tests/requirements.txt
python3 tests/test_api_offline.py
```

이번 환경변수 예시·기동 순서·Docker 빌드·API 주소 설정·검증 스크립트는 **프로젝트 당시 구현과 구분되는 후속 개선**입니다. 현재 추천 조회는 학습용 SQL이며 내부의 사용자 1 조건과 일부 `LIMIT 10` 조회가 남아 있습니다. 추천 품질·성능·운영용 인증을 검증한 프로젝트로 설명하지 않습니다.

기본 구조와 화면 일부는 외부 구성요소를 활용합니다. 기존 [MIT License와 원저작자 표기](LICENSE)를 유지합니다.

---

## What I Learned

* PK·FK를 활용한 관계형 데이터 모델 구성
* 테이블 간 관계를 고려한 JOIN 쿼리 작성
* 서브쿼리와 집계 함수를 활용한 조건 기반 데이터 조회
* PyMySQL을 활용한 FastAPI–MySQL 연동
* SQL 결과를 REST API로 제공하고 React 화면에 연결하는 흐름
* 사용자 특성을 기준으로 데이터를 조회하는 추천 데이터 처리 방식

---

일부 기본 구조 및 오픈소스 구성요소를 활용한 수업 프로젝트이며, 본 README는 직접 구현·수정한 SQL 조회 로직, 데이터 처리, API 연동 내용을 중심으로 정리했습니다.
