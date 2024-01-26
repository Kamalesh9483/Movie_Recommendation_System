import pandas as pd 
import numpy as np 
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# converting all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
  
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

def get_recommendations(title, indices, df2, cosine_sim=None):
    # index of the movie that matches the title
    idx = indices[title]

    #pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # movie indices
    movie_indices = [i[0] for i in sim_scores]
    df_html = pd.DataFrame()
    df_html['Similar_Movies'] = (df2['title'].iloc[movie_indices])
    # df_html = df_html
    # print(type(df_html))
    return df_html

class movieNameLength(Exception):
    pass

# if __name__ == "__main__":

class MovieReccomendation():

    def movie(movieInput):
        try:
            if len(movieInput) <= 50:
                df1=pd.read_csv('tmdb_5000_credits.csv')
                df2=pd.read_csv('tmdb_5000_movies.csv')
                df1.columns = ['id','tittle','cast','crew']
                df2= df2.merge(df1,on='id')
                #Genre, keyword based
                features = ['cast', 'crew', 'keywords', 'genres']
                for feature in features:
                    df2[feature] = df2[feature].apply(literal_eval)

                
                df2['director'] = df2['crew'].apply(get_director)

                features = ['cast', 'keywords', 'genres']
                for feature in features:
                    df2[feature] = df2[feature].apply(get_list)
                
          
                features = ['cast', 'keywords', 'director', 'genres']

                for feature in features:
                    df2[feature] = df2[feature].apply(clean_data)
                
                df2['soup'] = df2.apply(create_soup, axis=1)

                # Count Matrix
                count = CountVectorizer(stop_words='english')
                count_matrix = count.fit_transform(df2['soup'])

                #Cosine Similarity
                cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

           
                df2 = df2.reset_index()
                indices = pd.Series(df2.index, index=df2['title'])

            
                #movieInput = input('Enter the Movie Name for a similar movie recommendation\n')
                
                result_df = get_recommendations(movieInput, indices, df2, cosine_sim2)
                return result_df
            else:
                raise movieNameLength
        
        except movieNameLength as e1:
            print('The Entered Movie length name exceeded 50 characters please retry...')
            return e1
        except Exception as e:
            print(f'The Movie {e} is not in the Database Please retry... ')

            return e
