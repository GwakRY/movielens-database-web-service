import React from 'react';
import { useEffect, useState } from 'react';

import MovieGrid from '../components/MovieGrid';
import MovieSlider from '../components/MovieSlider';


const Home = () => {
	const [movies, setMovies] = useState([]);
	
	useEffect(() => {
		async function fetchMovies() {
			try {
				const response = await fetch('http://localhost:8001/v1/movie');
				const data = await response.json();
				setMovies(data);
			} catch (error) {
				console.error('Error fetching movies:', error);
			}
		}

		fetchMovies();
	}, []);

	//내 나이와 같은 유저들의 top10 리스트
	const [age_relatedMovies, set_age_relatedMovies] = useState([]);
	useEffect(() => {
		async function fetchMovies() {
			try {
				const response = await fetch('http://localhost:8001/v1/user/1/same_age_movies');
				const data = await response.json();
				set_age_relatedMovies(data);
			} catch (error) { }
		}

		fetchMovies();
	}, []);

	//내 직업과 같은 유저들의 top10 리스트
	const [occupation_relatedMovies, set_occupation_relatedMovies] = useState([]);
	useEffect(() => {
		async function fetchMovies() {
			try {
				const response = await fetch('http://localhost:8001/v1/user/1/same_occupation_movies');
				const data = await response.json();
				set_occupation_relatedMovies(data);
			} catch (error) { }
		}

		fetchMovies();
	}, []);

	//사용자 기반 협업 필터링 
	const [CF_relatedMovies, set_CF_relatedMovies] = useState([]);
	useEffect(() => {
		async function fetchMovies() {
			try {
				const response = await fetch('http://localhost:8001/v1/user/1/algorithm_1');
				const data = await response.json();
				set_CF_relatedMovies(data);
			} catch (error) { }
		}

		fetchMovies();
	}, []);

	//1950 이전 영화들
	const [before1950_relatedMovies, set_before1950_relatedMovies] = useState([]);
	useEffect(() => {
		async function fetchMovies() {
			try {
				const response = await fetch('http://localhost:8001/v1/movie/before1950');
				const data = await response.json();
				set_before1950_relatedMovies(data);
			} catch (error) { }
		}

		fetchMovies();
	}, []);

	return (
		<div className="max-w-screen-lg mx-auto w-full grid grid-cols-1 gap-10 pt-32 px-4 lg:px-0">
			<div className='grid grid-cols-1 gap-4'>
				<h1 className="text-2xl font-bold">Welcom to the Homepage</h1>
			</div>

			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold">Movies in Slider format</h2>
				<MovieSlider movies={movies} />
			</div>

			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold">Movies in Grid format</h2>
				<MovieGrid movies={movies} />
			</div>
			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold">Top10 movies with same Occupation users</h2>
				<MovieGrid movies={occupation_relatedMovies} />
			</div>
			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold">Top10 movies with same Age users</h2>
				<MovieGrid movies={age_relatedMovies} />
			</div>
			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold"> 나와 비슷한 취향의 영화들</h2>
				<MovieGrid movies={CF_relatedMovies} />
			</div>
			<div className='grid grid-cols-1 gap-4'>
				<h2 className="text-xl font-bold"> Movies Before 1950</h2>
				<MovieGrid movies={before1950_relatedMovies} />
			</div>
			
		</div>
	);
};

export default Home;