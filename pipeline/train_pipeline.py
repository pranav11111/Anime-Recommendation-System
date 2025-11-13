from src.model_training import ModelTraining
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from config.paths_config import *
from utlis.common_functions import read_yaml

if __name__ == "__main__":
    processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    processor.run_processor()

    modeltrainer = ModelTraining(PROCESSED_DIR)
    modeltrainer.train_model()