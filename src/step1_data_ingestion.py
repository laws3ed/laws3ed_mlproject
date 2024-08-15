import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from exception import CustomException
from logger import logging

@dataclass
class DataIngestionConfig:
    input_dataset_path = os.path.join("data", "input_dataset.csv") 
    train_dataset_path = os.path.join("data", "train_dataset.csv")
    test_dataset_path = os.path.join("data", "test_dataset.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def execute_data_ingestion(self):
        try:
            logging.info("Started data ingestion.")
            os.makedirs(os.path.dirname(self.data_ingestion_config.input_dataset_path), exist_ok=True)
            logging.info("Data directory created.")
            df = pd.read_csv("../online_shoppers_intention.csv")
            logging.info("Completed reading the input dataset.")

            train_data, test_data = train_test_split(df, test_size=0.2, random_state=17)
            logging.info("Completed train-test split.")
            logging.info("Saving input, train and test datasets.")
            df.to_csv(self.data_ingestion_config.input_dataset_path, index=False, header=True)
            train_data.to_csv(self.data_ingestion_config.train_dataset_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.test_dataset_path, index=False, header=True)
            logging.info("Completed data ingestion.")
            return(
                self.data_ingestion_config.input_dataset_path, 
                self.data_ingestion_config.train_dataset_path,
                self.data_ingestion_config.test_dataset_path
            )
        except Exception as e:
            raise CustomException(e, sys)

# Test data ingestion step
if __name__ == "__main__":
    di= DataIngestion()
    di.execute_data_ingestion()

