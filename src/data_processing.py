import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.rating_df = None
        self.anime_df = None
        self.x_train_array = None
        self.x_test_array = None
        self.y_train_array = None
        self.y_test_array = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        os.makedirs(self.output_dir, exist_ok= True)
        logger.info("Data Processor initialized")

    def load_data(self, usecsols):
        try:    
            self.rating_df = pd.read_csv(self.input_file, low_memory = True, usecols = usecsols)
            logger.info("data loaded")
        except Exception as e:
            raise CustomException("Failed to load data", e)
        
    def filteruser(self,min_rating = 400):
        try:
            n_rating = self.rating_df['user_id'].value_counts()
            self.rating_df = self.rating_df[self.rating_df['user_id'].isin(n_rating[n_rating >= min_rating].index)] 
            logger.info('filtered user successfully..')
        except Exception as e:
            raise CustomException("Failed to filter data", e)
    
    def scaling(self):
        try:
            min_rating = min(self.rating_df['rating'])
            max_rating = max(self.rating_df['rating'])
            self.rating_df['rating'] = self.rating_df['rating'].apply(lambda x: (x - min_rating)/(max_rating-min_rating)).astype(np.float64)
            logger.info('Scaling done...')
        except Exception as e:
            raise CustomException("Failed to scale data", e)
        
    def enc_data(self):
        try: 
            ##users
            unqiue_user_id = self.rating_df['user_id'].unique().tolist()

            self.user2user_encoded = {x: i for i, x in enumerate(unqiue_user_id)}  # Encoding to eliminate gaps
            self.user2user_decoded = {i: x for i, x in enumerate(unqiue_user_id)}

            self.rating_df['user'] = self.rating_df['user_id'].map(self.user2user_encoded)
            logger.info('Encoding done for user')

            ## Anime

            unqiue_anime_id = self.rating_df['anime_id'].unique().tolist()

            self.anime2anime_encoded = {x: i for i, x in enumerate(unqiue_anime_id)}  # Encoding to eliminate gaps
            self.anime2anime_decoded = {i: x for i, x in enumerate(unqiue_anime_id)}

            self.rating_df['anime'] = self.rating_df['anime_id'].map(self.anime2anime_encoded)

            logger.info('Encoding done for anime')
        except Exception as e:
            raise CustomException("Failed to encode data", e)
        
    def split_data(self, test_size = 1000, random_state = 43):
        try:
            self.rating_df = self.rating_df.sample(frac=1, random_state=43).reset_index(drop = True)
            x = self.rating_df[['user','anime']].values
            y = self.rating_df['rating']
            train_indices = self.rating_df.shape[0] - test_size
            x_train, x_test, y_train, y_test = (
            x[:train_indices],
            x[train_indices :],
            y[:train_indices],
            y[train_indices :],
            )
            self.x_train_array = [x_train[:, 0], x_train[:,1]]
            self.x_test_array = [x_test[:, 0], x_test[:,1]]
            self.y_train_array = y_train
            self.y_test_array = y_test

            logger.info('Splitting done..')
        except Exception as e:
            raise CustomException("Failed to split data", e)
        
    def save_artifacts(self):
        try:
            artifacts = {
                'user2user_enc': self.user2user_encoded,
                'user2user_dec': self.user2user_decoded,
                'anime2anime_enc': self.anime2anime_encoded,
                'anime2anime_dec': self.anime2anime_decoded,
            }

            for name, data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir,f'{name}.pkl'))
                logger.info(f'{name} save in {self.output_dir}')

            joblib.dump(self.x_train_array,X_TRAIN_ARRAY)
            joblib.dump(self.x_test_array,X_Test_ARRAY)
            joblib.dump(self.y_train_array,Y_TRAIN)
            joblib.dump(self.y_test_array, Y_Test)

            logger.info("Features and target saved")


            self.rating_df.to_csv(RATING_DF, index = False)

            logger.info('rating_df saved')
        
        except Exception as e:
            raise CustomException("Failed to save data", e)
        
    def process_anime_data(self):
        try:
            df = pd.read_csv(ANIME_CSV)
            cols = ['MAL_ID', 'Name', 'Genres', 'sypnopsis']
            synopsis_df = pd.read_csv(SYNOPSIS_CSV, usecols= cols)

            df = df.replace('Unknown', np.nan)

            def GetAnimeName(anime_id):
                try:
                    name = df[df.anime_id == anime_id].eng_version.values[0]
                    if name is np.nan:
                        name = df[df.anime_id == anime_id].Name.values[0]
                except:
                    print('Error')
                return name
            
            df['anime_id'] = df['MAL_ID']
            df['eng_version'] = df['English name']
            df['eng_version'] = df.anime_id.apply(lambda x: GetAnimeName(x))

            df.sort_values(by = 'Score',
               ascending= False,
               na_position= 'last',
               inplace= True)
            
            df = df[['anime_id', 'eng_version','Score', "Genres", "Episodes", "Type", 'Premiered', 'Members']]

            df.to_csv(DF, index= False)
            synopsis_df.to_csv(SYNOPSIS, index= False)

            logger.info('df and synopsis_df saved')
        
        except Exception as e:
            raise CustomException("Failed to save dataframes df and synopsis", e)
        
    def run_processor(self):
        try:
            self.load_data(usecsols=['user_id', 'anime_id', 'rating'])
            self.filteruser()
            self.scaling()
            self.enc_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()

            logger.info("Full Preprocessing done...")
        
        except Exception as e:
            raise CustomException("Final Preprocessing failed", e)
        
if __name__ == "__main__":
    processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    processor.run_processor()

        
