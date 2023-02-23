from sensor.entity import artifact_entity,config_entity
from sensor.logger import logging
from scipy.stats import ks_2samp
from typing import Optional
import os,sys 
import pandas as pd
from sensor import utils
import numpy as np
from sensor.config import TARGET_COLUMN
from sensor.exception import SensorException





class DATA_VALIDATION :
    def __init__(self,data_validation_config :config_entity.DATA_VALIDATION_CONFIG,
                       data_ingestion_artifact : artifact_entity.DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:
            raise SensorException(e, sys)

    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name : str)->pd.DataFrame:
        try :

            threshold =self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            drop_columns_names = null_report[null_report>threshold].index
            df.drop(list(drop_columns_names),axis = 1,inplace=True)
            self.validation_error[report_key_name]= list(drop_columns_names)
            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise SensorException(e, sys)

    def if_required_columns_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->pd.DataFrame:
        try :
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns= []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(base_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True

        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report =dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[column],current_df[column]

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)


                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    #different distribution

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:

        try:
            

            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)

            base_df= self.drop_missing_values_columns(df= base_df, report_key_name="missing_values_name_within_the_dataset")


            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df = self.drop_missing_values_columns(df= train_df, report_key_name="missing values of train data")
            test_df = self.drop_missing_values_columns(df= test_df, report_key_name="missing values of test data")

            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)
            

            train_df_column_status= self.if_required_columns_exist(base_df= base_df, current_df= train_df, report_key_name="missing_columns_train_df")
            test_df_column_status = self.if_required_columns_exist(base_df= base_df, current_df= test_df, report_key_name="missing_columns_test_df")

            if train_df_column_status:
                self.data_drift(base_df=base_df, current_df= train_df, report_key_name="data_drift_train_data")
            if test_df_column_status:
                self.data_drift(base_df= base_df, current_df=test_df, report_key_name="data_drift_test_data")


            utils.write_yaml_file(file_path= self.data_validation_config.report_file_path, data= self.validation_error)
            Data_validaiton_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)

            return Data_validaiton_artifact

        except Exception as e :
            raise SensorException(e,sys)


            






        




        




    
        
    




