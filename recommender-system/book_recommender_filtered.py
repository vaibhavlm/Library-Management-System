import pandas as pd

# Pearson correlation
from scipy.stats import pearsonr


def user_colab(user, genre_chosen, ratings_df, books_df, book_tags_df, tags_df):
    # Create dataframe for new user (me)
    user = pd.DataFrame(columns=['title', 'rating'], data=user.items())

    # Create a list of categories with major genres
    categories = ["Art", "Biography", "Business", "Chick Lit", "Children's", "Christian", "Classics", "Comics",
                  "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Gay and Lesbian",
                  "Graphic Novels", "Historical Fiction", "History", "Horror", "Humor and Comedy", "Manga", "Memoir",
                  "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion",
                  "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports",
                  "Thriller", "Travel", "Young Adult"]

    genres = [s.lower() for s in categories]

    # Get the available tags and genres
    available_genres = tags_df[tags_df['tag_name'].isin(genres)]
    available_tags = available_genres['tag_id']

    # Adding genre names to the tag ids
    # Note: a single book can be tagged as multiple genres
    tmp = book_tags_df[book_tags_df['tag_id'].isin(available_tags)]
    result = pd.merge(tmp, available_genres, on=["tag_id"])

    # Adding genre to books dataframe
    books_df_with_genres = pd.merge(books_df, result, on=['goodreads_book_id'])

    # Add book_id from books_df
    new_user = pd.merge(user, books_df, on='title', how='inner')
    new_user = new_user[['book_id', 'title', 'rating']].sort_values(by='book_id')

    new_user_with_genres = pd.merge(user, books_df_with_genres, on='title', how='inner')
    new_user_with_genres = new_user_with_genres[['book_id', 'title', 'rating', 'tag_name']].sort_values(by='tag_name')

    other_users = ratings_df[ratings_df['book_id'].isin(new_user['book_id'].values)]

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

    # Top-10 Global Recommendations
    recommendation_non_filtered = books_df[books_df['book_id'].isin(recommend_books['book_id'])][
        ['authors', 'title']].sample(10)

    # Top-10 Filtered Recommendations
    recommendation = books_df_with_genres[books_df_with_genres['book_id'].isin(recommend_books['book_id'])][
        ['authors', 'title', 'book_id', 'tag_name']]
    recommendation_filtered = recommendation[recommendation['tag_name'] == genre_chosen][
        ['authors', 'title', 'book_id']]
    limit = min(10, len(recommendation_filtered))
    filtered = recommendation_filtered.sample(limit)

    return filtered.to_dict('records')


def main(data, genre):
    user_info = {}

    for book, rating in zip(data[0], data[1]):
        user_info[book] = int(rating)

    # my_list = {'Martin Eden': 5,
    #            'Pet Sematary': 5,
    #            'One Hundred Years of Solitude': 5,
    #            'Ham on Rye': 5,
    #            'The Grapes of Wrath': 4,
    #            "Cat's Cradle": 5,
    #            'Crime and Punishment': 4,
    #            'The Trial': 4}

    genre_chosen = genre.lower()

    # books_url = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv'
    # ratings_url = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv'
    # book_tags_url = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/book_tags.csv'
    # tags_url = "https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/tags.csv"

    books_url = 'data/books.csv'
    ratings_url = 'data/ratings.csv'
    book_tags_url = 'data/book_tags.csv'
    tags_url = 'data/tags.csv'

    books_df = pd.read_csv(books_url)
    ratings_df = pd.read_csv(ratings_url)
    book_tags_df = pd.read_csv(book_tags_url)
    tags_df = pd.read_csv(tags_url)

    recommendation = user_colab(user_info, genre_chosen, ratings_df, books_df, book_tags_df, tags_df)
    return recommendation


if __name__ == "__main__":
    main()
