from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.utils import get_collections_data_frame
from sensor.entity import config_entity
from sensor.components.data_ingestion import DATA_INGESITON
from sensor.entity.config_entity import DATA_INGESTION_CONFIG

from sensor.entity.config_entity import DATA_VALIDATION_CONFIG
from sensor.components.data_validaiton import DATA_VALIDATION

from sensor.entity.config_entity import DATA_TRANSFOMAITON_CONFIG




if __name__ == "__main__":
     try :
          training_pipeline_config= config_entity.TRAINING_PIPELINE_CONFIG()
          #data_ingestion
          data_ingestion_config = DATA_INGESTION_CONFIG(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dic())
          data_ingestion = DATA_INGESITON(data_ingestion_config= data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          #data_validation
          DVC = DATA_VALIDATION_CONFIG(training_pipeline_config=training_pipeline_config)
          data_validation = DATA_VALIDATION(data_validation_config= DVC, data_ingestion_artifact= data_ingestion_artifact)
          Data_V_artifact = data_validation.initiate_data_validation()
          #data_transformation
          DTC = DATA_TRANSFOMAITON_CONFIG(training_pipeline_config=training_pipeline_config)
          Data_transformation = Data_transformation
     
     except Exception as e:
          print(e)
          
        