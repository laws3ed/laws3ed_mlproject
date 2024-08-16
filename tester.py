from src.utils import save_to_pkl_file
from src.step1_data_ingestion import DataIngestion
from src.step2_data_transformation import DataTransformation
from src.step3_model_training import ModelTrainer
from src.logger import logging

data_ingestion = DataIngestion()
_, train_data, test_data = data_ingestion.execute_data_ingestion()
data_tranformation = DataTransformation()
train_arr, test_arr, _ = data_tranformation.execute_data_transformation(train_data, test_data)
model_trainer = ModelTrainer()
test_acc = model_trainer.execute_model_training(train_arr, test_arr)
logging.info('Test accuracy for the best model:' + str(test_acc))