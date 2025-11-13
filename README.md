# Item_Based_Recommendation_System
![image](https://github.com/AylinOguz/Item_Based_Recommendation_System/blob/main/item_based.png?raw=true)

## Project Overview

This project implements an Item-Based Collaborative Filtering movie recommendation system using the MovieLens dataset

The system recommends movies based on similarity between items (movies) rather than users.

If two movies are rated similarly by many users, they are considered similar.

For example, if a user liked Inception, the system may recommend The Dark Knight or Interstellar.

Note: This project uses Pearson correlation (pandas corrwith) to calculate similarity

## How It Works

1- Data Preparation:

- Load movie.csv and rating.csv from MovieLens dataset.

- Remove movies with fewer than 1000 ratings to improve recommendation quality.

- Optionally, remove users who rated fewer than 50 movies.

2- User–Movie Matrix:

- Create a pivot table with users as rows and movies as columns.

- Each cell contains the rating the user gave to that movie.

3- Finding Similar Movies:

- For a target movie, calculate the Pearson correlation between that movie and all other movies.

- Sort correlations and recommend the top N similar movies.

4- Reusable Function:

- item_based_recommender(movie_name, user_movie_df) returns the top 10 similar movies.

- item_based_recommender2(movie_name, user_movie_df) allows partial movie name matching.
