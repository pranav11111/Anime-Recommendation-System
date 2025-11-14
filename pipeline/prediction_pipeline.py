from config.paths_config import *
from utlis.helper import *

def hybrid_recom(user_id, user_weight = 0.5, content_weight = 0.5):
    #User Recommendation
    
    similar_users = find_similar_users(int(user_id),USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
    user_pref = get_user_preferences(int(user_id), RATING_DF, DF)
    user_rec_anime = get_user_recommendations(similar_users,user_pref,DF, SYNOPSIS, RATING_DF)

    user_rec_anime_list = user_rec_anime['anime_name'].to_list()

    #Contnet Recommendation
    content_rec_anime = []

    for anime in user_rec_anime_list:
        similar_content = find_similar_animes(anime, ANIME_WEIGHTS_PATH,ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, DF)

        if similar_content is not None and not similar_content.empty:
            content_rec_anime.extend(similar_content['name'].to_list())
        else:
            print(f'no similar anime found {anime}')

    combine_score = {}

    for anime in user_rec_anime_list:
        combine_score[anime] = combine_score.get(anime,0) + user_weight
    for anime in content_rec_anime:
        combine_score[anime] = combine_score.get(anime,0) + content_weight

    sorted_anime = sorted(combine_score.items(), key = lambda x:x[1], reverse = True)

    return [anime for anime, score in sorted_anime[:10]]