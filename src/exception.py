import sys
from logger import logging

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = "Error: file name [{0}] line number [{1}] message[{2}]".format(file_name,line_number,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

# Test exception handling
#import pandas as pd
#def load_dataset(file_name):
#    try:
#        # load the dataset from file_name
#        df = pd.read_csv(file_name)
#        
#    except FileNotFoundError as e:
#        logging.error("File not found.")
#        raise CustomException('File not found', error_detail=sys)
#
#if __name__ == "__main__":
#    try:
#        load_dataset('online_shoppers_intention.csv')       
#    except Exception as e:
#        raise CustomException(e, sys)

