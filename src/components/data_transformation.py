import numpy as np 
import pandas as pd 
import os
import sys 
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


@dataclass
class datatransformationconfig:
    preprosessing_obj_file_path= os.path.join('artifacts',"preprocesser.pkl")
    
class datatransformation:
    def __init__(self):
        self.data_transformation=datatransformationconfig()

#genrate all pickel file, converting feature into categoricale to numerical and perform sdandscalar
    def get_data_transformer_object(self):
        try:
            numerical_columns=["reading_score","writing_score"]
            categoricale_columns=["gender",
            "race_ethnicity",
            "parental_level_of_education",
            "lunch",
            "test_preparation_course",
            "math_score"]

            '''
            create pipiline 
            handle missing values
            1.inmputer
            'simpleimputer': for handle missing values
            strategy="median" : parameter specifies that missing values should be replaced with the median 
            (for catagorical data)strategy="most_frequent" specifies that missing values should be replaced with the most frequent value 

            '''
            num_pipe = Pipeline(

                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler)
                ]

            )

            cat_pipe=Pipeline(
                
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                
                ]
            )


            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")


            '''
            combine net_pipe and cat_pipe pipeline  with columns
            
            '''
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipe,numerical_columns),
                ("cat_pipeline",cat_pipe,categorical_columns)

                ]


            )
            return preprocesser


        except Exception as e:
            raise CustomException(e,sys)


    def data_transformation_start(self,train_path,test_path):

        try:
            train_df=pd.read_csv('train_path')
            test_df=pd.read_csv('test_path')

            logging.info('train and test data complete')
            logging.info('carry preprocessing obj')

            preprocessing_obj=self.get_data_transformer_object()

            target_column='math_score'
            numerical_columns=["reading_score","writing_score"]

            input_column_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_column_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]

            


            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_column_train_df)
            input_column_test_arr=preprocessing_obj.fit_transform(input_column_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr=np.c_[input_column_test_arr,np.array(target_feature_test_df) ]


            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path = self.data_transformation.preprosessing_obj_file_path,
                obj=preprocessing_obj
            )


            return(
                train_arr,
                test_arr,
                self.data_transformation.preprosessing_obj_file_path
            )



        except Exception as e:
            raise CustomException(e,sys)
    



            


