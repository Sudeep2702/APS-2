from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd 
import numpy as np 
import sys , os
from datetime import datetime
BASE_FILE = "sensor.csv"
TRAIN_FILE= "train.csv"
TEST_FILE= "test.csv"
# TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
# TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
# MODEL_FILE_NAME = "model.pkl"




class TRAINING_PIPELINE_CONFIG :
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

        except Exception as e:
            raise SensorException(e,sys)

class DATA_INGESTION_CONFIG :
    def __init__(self,training_pipeline_config : TRAINING_PIPELINE_CONFIG):
        try:
            self.data_base_name = "aps"
            self.collection_name = "sensor"
            self.data_ingestion = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion,"feature_store",BASE_FILE)
            self.train_file_path = os.path.join(self.data_ingestion,"data_set",TRAIN_FILE)
            self.test_file_path = os.path.join(self.data_ingestion,"data_set",TEST_FILE)
            self.test_size = 0.2
        except Exception as e:
            raise SensorException(e, sys)

    def to_dic(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise SensorException(e,sys)  

class DATA_VALIDATION_CONFIG :
    
    def __init__(self,training_pipeline_config : TRAINING_PIPELINE_CONFIG):
        try:
            self.data_validaiton_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path = os.path.join(self.data_validaiton_dir,"report.yaml")
            self.missing_threshold:float = 0.2
            self.base_file_path = os.path.join("/config/workspace/aps_failure_training_set1.csv")
        
        except Exception as e:

            raise SensorException(e, sys)

# class DATA_TRANSFOMAITON_CONFIG :
#      def __init__(self,training_pipeline_config : TRAINING_PIPELINE_CONFIG):
#         try :
#             self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
#             self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
#             self.transformed_train_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE.replace("csv"," npz"))
#             self.transformed_test_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE.replace("csv", "npz"))
#             self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)


        
        # except Exception as e:

        #     raise SensorException(e, sys)              


            

