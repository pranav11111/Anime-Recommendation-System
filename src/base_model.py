from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense, Activation, BatchNormalization
from utlis.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info('Loaded configuration')
        except Exception as e:
            raise CustomException('Error loading config',e)
    
    def RecommenderNet(self, n_user, n_anime):
        try: 
            embedding_size = self.config['model']['embedding_size']
            user = Input(name = 'user', shape = [1])
            user_embed = Embedding(name = "user_embedding", input_dim = n_user, output_dim= embedding_size)(user)
            
            anime = Input(name= 'anime', shape = [1])
            anime_embed = Embedding(name = "anime_embedding", input_dim = n_anime, output_dim= embedding_size)(anime)


            x = Dot(name = 'dot_prod', normalize= True, axes= 2)([user_embed,anime_embed])

            x = Flatten()(x)

            x = Dense(1, kernel_initializer= 'he_normal')(x)
            x = BatchNormalization()(x)
            x = Activation('sigmoid')(x)

            model = Model(inputs = [user, anime], outputs = x)
            model.compile(
                        loss = self.config['model']['loss'], 
                        metrics = self.config['model']['metrics'],
                        optimizer = self.config['model']['optimizer']
                            )
            logger.info('Model Created succesfully')
            return model
        
        except Exception as e:
            logger.error('Model not created')
            raise CustomException("Model creation failed", e)