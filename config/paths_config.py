import os


################ DATA INGESTION PATHS ##############################

RAW_DIR = 'artifacts/raw'
CONFIG_PATH = 'config/config.yaml'


################ DATA PROCESSING PATH ###############################

PROCESSED_DIR = 'artifacts/processed'
ANIMELIST_CSV = 'artifacts/raw/animelist.csv'
ANIME_CSV = 'artifacts/raw/anime.csv'
SYNOPSIS_CSV = 'artifacts/raw/anime_with_synopsis.csv'

X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR, "x_train_array.pkl")
X_Test_ARRAY = os.path.join(PROCESSED_DIR, "x_test_array.pkl")
Y_TRAIN = os.path.join(PROCESSED_DIR, "y_train.pkl")
Y_Test= os.path.join(PROCESSED_DIR, "y_test.pkl")


RATING_DF = os.path.join(PROCESSED_DIR,'ratings_df.csv')
DF = os.path.join(PROCESSED_DIR,'anime_df.csv')
SYNOPSIS = os.path.join(PROCESSED_DIR,'synopsis_df.csv')


USER2USER_ENCODED = "artifacts/processed/user2user_enc.pkl" 
USER2USER_DECODED = "artifacts/processed/user2user_dec.pkl"

ANIME2ANIME_ENCODED = 'artifacts/processed/anime2anime_enc.pkl'
ANIME2ANIME_DECODED = "artifacts/processed/anime2anime_dec.pkl"



################# MODEL TRAINING ################

MODEL_DIR = 'artifacts/model'
WEIGHTS_DIR = 'artifacts/weigths'
MODEL_PATH = os.path.join(MODEL_DIR, 'model.h5')
ANIME_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, 'anime_weights.pkl')
USER_WEIGHTS_PATH =os.path.join(WEIGHTS_DIR,'user_weights.pkl')
CHECKPOINT_FILE_PATH = 'artifacts/model_checkpoint/weights.weights.h5'