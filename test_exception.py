#Test exception handling
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException

def load_dataset(file_name):
    try:
        # load the dataset from file_name
        df = pd.read_csv(file_name)
        
    except FileNotFoundError as e:
        logging.error("File not found.")
        raise CustomException('File not found', error_detail=sys)

if __name__ == "__main__":
    try:
        load_dataset('online_shoppers_intention.csv')       
    except Exception as e:
        raise CustomException(e, sys)