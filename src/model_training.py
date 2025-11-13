import joblib
import comet_ml
import numpy as np
import os
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from src.logger import get_logger
from src.base_model import BaseModel
from src.custom_exception  import CustomException
from config.paths_config import *

logger = get_logger(__name__)


class ModelTraining:
    def __init__(self, data_path):
        self.data_path = data_path
        self.experiment = comet_ml.Experiment(api_key = 'JgtHTRDJxz8YJN1IiCbzXiIUN',
                                                  project = 'Anime recommendation system',
                                                  workspace = 'pranav11111')

        logger.info(" Model Training initalized")

    def load_data(self):
        try:
            x_train_array = joblib.load(X_TRAIN_ARRAY)
            x_test_array = joblib.load(X_Test_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_Test)

            
            logger.info('Data loaded for model training')

            return x_train_array,x_test_array,y_train,y_test

        except Exception as e:
            raise CustomException('Loading failed', e)
    
    def extract_weights(self, name, model):
        try: 
            weight_layer = model.get_layer(name)
            weights = weight_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights,axis = 1).reshape((-1,1))
            logger.info('extracting weights for {name}')
            return weights
        except Exception as e:
            raise CustomException('Could not extract weights...', e)
            
    

    def save_model(self, model):
        try:
            model.save(MODEL_PATH)
            logger.info('Model Saved to model path...')

            anime_weights = self.extract_weights('anime_embedding', model)
            user_weights = self.extract_weights('user_embedding', model)

            joblib.dump(user_weights, USER_WEIGHTS_PATH)
            joblib.dump(anime_weights,ANIME_WEIGHTS_PATH)

            logger.info('Model and weights saved')
            
            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGHTS_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)
            

        except Exception as e:
            raise CustomException("Could not save weightss.. ", e)
        
    def train_model(self):
        try:
            x_train_array,x_test_array,y_train,y_test = self.load_data()
            
            n_user = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))


            base_model = BaseModel(CONFIG_PATH)

            model = base_model.RecommenderNet(n_user = n_user, n_anime= n_anime)

            start_lr = 0.00001
            min_lr = 0.00001
            max_lr = 0.00005
            batch_size = 10000

            rampup_epochs = 5
            susatian_epoch = 0
            exp_deacy = 0.8

            def lrfn(epoch):
                if epoch< rampup_epochs:
                    return (max_lr - start_lr)/rampup_epochs*epoch + start_lr
                elif epoch< rampup_epochs+susatian_epoch:
                    return max_lr
                else:
                    return (max_lr - min_lr) *exp_deacy **(epoch- rampup_epochs-susatian_epoch) +min_lr
                

            lr_callbakc = LearningRateScheduler( lambda epoch: lrfn(epoch), verbose = 0)

            

            model_checkpoint = ModelCheckpoint(filepath= CHECKPOINT_FILE_PATH, save_weights_only= True, monitor= "val_loss", mode = 'min', save_best_only= True)

            early_stopping = EarlyStopping(patience=3,monitor="val_loss", mode = 'min', restore_best_weights= True)

            my_callbacks = [model_checkpoint, lr_callbakc, early_stopping]

            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok= True)
            os.makedirs(WEIGHTS_DIR, exist_ok= True)
            os.makedirs(MODEL_DIR, exist_ok= True)

            try: 
                history = model.fit(x = x_train_array, y =y_train, 
                                    batch_size= batch_size, 
                                    epochs= 20, verbose= 1, 
                                    validation_data= (x_test_array, y_test),
                                    callbacks = my_callbacks)
                

                model.load_weights(CHECKPOINT_FILE_PATH)
                logger.info('Training done!')

                for epoch in range(len(history.history['loss'])):
                    train_loss = history.history['loss'][epoch]
                    val_loss = history.history['val_loss'][epoch]
                    self.experiment.log_metric('train_loss', train_loss, step = epoch)
                    self.experiment.log_metric('val_loss', val_loss, step = epoch)


            except Exception as e:
                raise CustomException('Training Failed', e)
            self.save_model(model)
        except Exception as e:
            raise CustomException('Error during training process', e)
        

if __name__ == '__main__':
    modeltrainer = ModelTraining(PROCESSED_DIR)
    modeltrainer.train_model()
    
