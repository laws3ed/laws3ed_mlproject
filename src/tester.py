from utils import save_to_pkl_file
from step1_data_ingestion import DataIngestion
from step2_data_transformation import DataTransformation

data_ingestion = DataIngestion()
_, train_data, test_data = data_ingestion.execute_data_ingestion()
data_tranformation = DataTransformation()
train_arr, test_arr, _ = data_tranformation.execute_data_transformation(train_data, test_data)