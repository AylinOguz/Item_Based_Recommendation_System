######################################
#  Preparing the Dataset
######################################
import pandas as pd
pd.set_option('display.max_columns', 500)
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
df.head()


######################################
# Creating the User-Movie DataFrame
######################################

df["title"].nunique()
# There are 27,262 movies in total.


df["title"].value_counts().head()
# Pulp Fiction (1994)                 67310
# Forrest Gump (1994)                 66172
# Shawshank Redemption, The (1994)    63366
# Silence of the Lambs, The (1991)    63299
# Jurassic Park (1993)                59715

# We looked at the frequency of each movie. Some movies might have only 1 review.
# As a lower limit, we will remove movies with fewer than 1,000 reviews.

movie_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = movie_counts[movie_counts["count"] <= 1000].index
rare_movies_index = df[df["title"].isin(rare_movies)].index
common_movies = df.drop(rare_movies_index, axis=0)

common_movies["title"].value_counts()

df["title"].nunique()
#  27,262

common_movies["title"].nunique()
# The number of unique movies decreased to 3,159


# Remove users with fewer than 50 reviews
common_movies["userId"].value_counts()
rare_user = pd.DataFrame(common_movies["userId"].value_counts())
rare_user_ID = rare_user[rare_user["count"]<50].index
common_movies = common_movies[~common_movies["userId"].isin(rare_user_ID)]


# Creating the User-Movie matrix
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")


######################################
# Step 3: Making Item-Based Movie Recommendations
######################################

movie_name = "Matrix, The (1999)"
movie_name = "Ocean's Twelve (2004)"
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)



movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)



# Additional work

# Important note: corrwith is used to check the correlation between a DataFrame and a Series.
# Here, 'movie' comes out as a DataFrame, so we reduce it to a Series by using ["Inception (2010)"] in the correlation.

movie = user_movie_df.loc[:,user_movie_df.columns.str.contains("Inception")]
# Inception (2010)

user_movie_df.corrwith(movie["Inception (2010)"]).sort_values(ascending=False).head(10)


def check_film(keyword, user_movie_df):
    return [col for col in user_movie_df.columns if keyword in col]

check_film("Insomnia", user_movie_df)


######################################
# Step 4: Preparing the Script
######################################

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["count"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return  user_movie_df


user_movie_df = create_user_movie_df()


def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

item_based_recommender("Inception", user_movie_df)
movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]
item_based_recommender(movie_name, user_movie_df)


# 2nd method (in this function, you don't need to write the exact movie name as in the dataset)
# When we just write "Inception", the previous function won't work, but this one does.

def item_based_recommender2(movie_name, user_movie_df):
    movie = user_movie_df.loc[:, user_movie_df.columns.str.contains(movie_name)]
    return user_movie_df.corrwith(movie[movie.columns]).sort_values(ascending=False)[1:11].index.tolist()

item_based_recommender2("Inception", user_movie_df)
