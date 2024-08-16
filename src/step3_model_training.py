import os
import sys
import numpy as np
from dataclasses import dataclass

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from exception import CustomException
from logger import logging
from utils import save_to_pkl_file

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('model', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def evaluate_models(self, X_train, y_train, X_test, y_test, models, param):
        try:
            report = {}

            for i in range(len(list(models))):
                logging.info("Started hyperparameter tuning for: "+ str(list(models.keys())[i]))
                model = list(models.values())[i]
                para=param[list(models.keys())[i]]

                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train,y_train)

                model.set_params(**gs.best_params_)
                model.fit(X_train,y_train)

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                train_model_score = accuracy_score(y_train, y_train_pred)
                test_model_score = accuracy_score(y_test, y_test_pred)

                report[list(models.keys())[i]] = test_model_score

            return report

        except Exception as e:
                raise CustomException(e, sys)

    def execute_model_training(self, train_arr, test_arr):
        try:
            logging.info("Started model training")
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                'Random Forest': RandomForestClassifier(),
                'Decision Tree': DecisionTreeClassifier(),
                'k Nearest Neighbors': KNeighborsClassifier()
            }
            
            params={
                'Decision Tree': {
                    'max_depth': [10, 20, 30],
                    'min_samples_leaf': [5, 10, 20, 50],
                    'criterion': ["gini", "entropy"]
                },
                'Random Forest': {
                    'n_estimators': [50, 100, 200], 
                    'max_features': ['sqrt', 'log2', None], 
                    'max_depth': [12, 15, 21], 
                    'max_leaf_nodes': [12, 15, 21],
                },
                'k Nearest Neighbors': {
                    'n_neighbors': list(range(1, 21))
                }
            }

            model_report:dict = self.evaluate_models(X_train, y_train, X_test, y_test, models, params)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            file_path=self.model_trainer_config.trained_model_file_path
            save_to_pkl_file(file_path, best_model)
            logging.info(f"Saved best model object to pkl file.")

            predictions=best_model.predict(X_test)
            test_acc = accuracy_score(y_test, predictions)
            return test_acc
                       
        except Exception as e:
            raise CustomException(e,sys)