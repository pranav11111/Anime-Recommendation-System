import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'file is not in the given path')
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            return config
            logger.info('Succesfully read YAML file')
    
    except Exception as e:
        logger.error('Error while loading yaml')
        raise CustomException('failed to read yaml file', e)