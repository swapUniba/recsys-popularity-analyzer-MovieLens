import pandas as pd
from enum import Enum


class Category(Enum):
    COLD = 1
    REGULAR = 2
    HOT = 3


################## EDIT HERE TO CHANGE CONFIGS ############################
RECS_FILE_NAME = ''
RECS_PATH = '../recs/cb-word-embedding/'  # input recs file
OUTPUT_FOLDER = '../recs_user/'
OUTPUT_FILE_NAME = 'HOT'
TAG = True
COLD_USER_RANGE = 23
REGULAR_USER_MIN = 24
REGULAR_USER_MAX = 175
MODE = Category.HOT
###########################################################################

def pick_tag():
    if TAG:
        return '_'

'''
MOVIELENS
From line 35 to 40
Extract the data that interests me from the file indicated in the path.
Change path and separator for different files.
I create two lists with the respective values of interest, in this case, 
user and rating and with the use of the dictionary I associate to each user the respective rating. 
'''
get_id_user_movie = lambda col: (line.split('::')[col - 1] for line in open('../datasets/ml-1m/users.dat'))
get_id_rating = lambda col: (line.split('::')[col - 1] for line in open('../datasets/ml-1m/ratings.dat'))

users_id = list(get_id_user_movie(1))
ratings_id = list(get_id_rating(1))
users_rating_match = {}

for index in users_id:
    users_rating_match[index] = ratings_id.count(index)
'''
Initialization 3 dictionaries, one for each category of users.
Through the for, based on the rating expressed by the user will be inserted in the appropriate dictionary.
'''
user_cold_start = {}
user_regular = {}
user_hot_start = {}
for values in users_rating_match:
    # I store the value in a variable and the comparison with threshold values.
    rating = int(users_rating_match[values])
    if rating <= COLD_USER_RANGE:
        user_cold_start[values] = rating
    elif REGULAR_USER_MIN <= rating <= REGULAR_USER_MAX:
        user_regular[values] = rating
    else:
        user_hot_start[values] = rating

if MODE == Category.COLD:
    category = user_cold_start
elif MODE == Category.REGULAR:
    category = user_regular
else:
    category = user_hot_start

#file output
output_path = OUTPUT_FOLDER + RECS_FILE_NAME + pick_tag() + OUTPUT_FILE_NAME
#file recs
recommender_file = pd.read_csv(RECS_PATH)
# select rows from a DataFrame on column values, as a query.
filtered_recommender = pd.DataFrame(recommender_file.loc[recommender_file['user'].isin(category.keys())])
filtered_recommender.to_csv(output_path, index=False)
