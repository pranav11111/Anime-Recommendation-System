import os
from src.custom_exception import CustomException
from src.logger import get_logger
from google.cloud import storage
import pandas as pd
from config.paths_config import *
from utlis.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_names = self.config['bucket_file_names']

        os.makedirs(RAW_DIR, exist_ok= True)

        logger.info('Data ingestion started ........')

    def download_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            
            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)
                if file_name == "animelist.csv":

                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    data = pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index= False)

                    logger.info("Large file detected downloading 5mil instead of 70 mil")

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)    

                    logger.info("Downloading smaller file")
        except Exception as e:
            logger.error("error while downloading data from gcp")
            raise CustomException("Failed to download...", e)
        
    def run_ingestion(self):
        try:
            logger.info("Data ingestion run fuction called..")
            self.download_from_gcp()
            logger.info("Ingestion completed successfully..")
        except Exception as e:
            logger.error("Ingestion failed..")
            raise CustomException('Problem during ingestion..',e)
        
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run_ingestion()
