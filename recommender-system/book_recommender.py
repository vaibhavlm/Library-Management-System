import pandas as pd

# Pearson correlation
from scipy.stats import pearsonr


def user_colab(user, ratings_df, books_df):
    # Create dataframe for new user (me)
    user = pd.DataFrame(columns=['title', 'rating'], data=user.items())

    # Add book_id from books_df
    new_user = pd.merge(user, books_df, on='title', how='inner')
    new_user = new_user[['book_id', 'title', 'rating']].sort_values(by='book_id')

    other_users = ratings_df[ratings_df['book_id'].isin(new_user['book_id'].values)]

    other_users['user_id'].nunique()

    # Sort users by count of most mutual books with me
    users_mutual_books = other_users.groupby(['user_id'])
    users_mutual_books = sorted(users_mutual_books, key=lambda x: len(x[1]), reverse=True)

    # Get the top 100 mutual users
    top_users = users_mutual_books[:100]

    # Initialize the pearson correlation
    pearson_corr = {}

    for user_id, features in top_users:
        # Books should be sorted
        features = features.sort_values(by='book_id')
        features_list = features['book_id'].values

        new_user_ratings = new_user[new_user['book_id'].isin(features_list)]['rating'].values
        user_ratings = features[features['book_id'].isin(features_list)]['rating'].values

        corr = pearsonr(new_user_ratings, user_ratings)
        pearson_corr[user_id] = corr[0]

    # Get top50 users with the highest similarity indices
    pearson_df = pd.DataFrame(columns=['user_id', 'similarity_index'], data=pearson_corr.items())
    pearson_df = pearson_df.sort_values(by='similarity_index', ascending=False)[:50]

    # Get all books for these users and add weighted book's ratings
    users_rating = pearson_df.merge(ratings_df, on='user_id', how='inner')
    users_rating['weighted_rating'] = users_rating['rating'] * users_rating['similarity_index']

    # Calculate sum of similarity index and weighted rating for each book
    grouped_ratings = users_rating.groupby('book_id').sum()[['similarity_index', 'weighted_rating']]

    recommend_books = pd.DataFrame()

    # Add average recommendation score
    recommend_books['avg_recommend_score'] = grouped_ratings['weighted_rating'] / grouped_ratings['similarity_index']
    recommend_books['book_id'] = grouped_ratings.index
    recommend_books = recommend_books.reset_index(drop=True)

    # Books with the highest score
    recommend_books = recommend_books[(recommend_books['avg_recommend_score'] == 5)]

    # Top-10 Recommendations
    recommendation = books_df[books_df['book_id'].isin(recommend_books['book_id'])][
        ['book_id', 'authors', 'title']].sample(10)

    return recommendation.to_dict('records')


def main(data):
    """
    User object attributes:

        user likes
        user played(audio)
        users liked audio(from other people)
        users interacted tags
        user lat
        user lng
        user replies
    """
    user_info = {'Martin Eden': 5,
                 'Pet Sematary': 5,
                 'One Hundred Years of Solitude': 5,
                 'Ham on Rye': 5,
                 'The Grapes of Wrath': 4,
                 "Cat's Cradle": 5,
                 'Crime and Punishment': 4,
                 'The Trial': 4}

    user_info = {}

    for book, rating in zip(data[0], data[1]):
        user_info[book] = int(rating)

    # books_url = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv'
    # ratings_url = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv'

    books_url = 'data/books.csv'
    ratings_url = 'data/ratings.csv'

    books_df = pd.read_csv(books_url)
    ratings_df = pd.read_csv(ratings_url)

    recommendation = user_colab(user_info, ratings_df, books_df)
    return recommendation

if __name__ == "__main__":
    main()
