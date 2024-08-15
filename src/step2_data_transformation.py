import os
import sys
from dataclasses import dataclass

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from exception import CustomException
from logger import logging
from utils import save_to_pkl_file

@dataclass
class DataTransformationConfig:
    data_preprocessor_file_path = os.path.join("preprocessor", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_preprocessor_config = DataTransformationConfig()

    def get_data_preprocessor(self):
        try:
            float_columns = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 
            'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
            int_columns = ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 
            'Browser', 'Region', 'TrafficType']
            string_columns = ['Month', 'VisitorType', 'Weekend']
            
            categorical_features_pipeline = Pipeline(
                steps = [
                    ('step1_impute_missing_values', SimpleImputer(strategy='most_frequent')),
                    ('step2_one_hot_encode_values', OneHotEncoder())
                ]
            )

            numerical_features_pipeline = Pipeline(
                steps = [
                    ('step1_impute_missing_values', SimpleImputer(strategy='median')),
                    ('step2_scale_values', StandardScaler())
                ]
            )
            
            int_features_pipeline = Pipeline(
                steps = [
                    ('step1_impute_missing_values', SimpleImputer(strategy='median'))
                ]
            )
            
            preprocessor = ColumnTransformer(
                [
                    ('categorical_features_pipeline', categorical_features_pipeline, string_columns),
                    ('numerical_features_pipeline', numerical_features_pipeline, float_columns),
                    ('int_features_pipeline', int_features_pipeline, int_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def execute_data_transformation(self, train_dataset_path, test_dataset_path):
        try:
            logging.info('Started data transformation.')

            train_df=pd.read_csv(train_dataset_path)
            logging.info('Read train dataset.')
            
            test_df=pd.read_csv(test_dataset_path)           
            logging.info('Read test dataset.')

            preprocessor = self.get_data_preprocessor()
            target_column_name="Revenue"

            train_features_df=train_df.drop(columns=[target_column_name],axis=1)
            train_target_df=train_df[target_column_name]

            test_features_df=test_df.drop(columns=[target_column_name],axis=1)
            test_target_df=test_df[target_column_name]

            train_features_arr=preprocessor.fit_transform(train_features_df)
            logging.info('Preprocessing train dataset completed.')
            
            test_features_arr=preprocessor.transform(test_features_df)
            logging.info('Preprocessing test dataset completed.')

            train_target_arr = np.array(train_target_df)
            test_target_arr = np.array(test_target_df)
            train_arr = np.c_[train_features_arr, train_target_arr]
            test_arr = np.c_[test_features_arr, test_target_arr]

            file_path=self.data_preprocessor_config.data_preprocessor_file_path
            save_to_pkl_file(file_path, preprocessor)
            logging.info(f"Saved preprocessor object to pkl file.")

            return (train_arr, test_arr, file_path)


        except Exception as e:
            raise CustomException(e, sys)
