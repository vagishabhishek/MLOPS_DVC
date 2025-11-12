from src.logger.logger import setup_logger
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score,precision_score,recall_score,roc_auc_score
from pathlib import Path
import json


logger = setup_logger("model-evaluater")

def load_model(file_path:str):
    """
        Load the trained model from a file
    """

    try:
        with open (file_path,'rb') as file:
            model = pickle.load(file)
        logger.debug(f'Model loaded from {file_path}')
        return model
    except FileNotFoundError:
        logger.error(f'File not found {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error ocurred while loadinf the model {e}')
        raise

def load_data(file_path:str)->pd.DataFrame:
    """
        Load data from CSV File
    """
    try : 
        df = pd.read_csv(file_path)
        logger.debug(f'Data loaded from {file_path}')
        return df
    except Exception as e:
        logger.error(f"Some error occurred {e}")
        raise

def evaluate_model(clf,x_test:np.ndarray,y_test:np.ndarray)->dict:
    try:

        y_pred = clf.predict(x_test)
        y_pred_proba = clf.predict(x_test)

        accuracy = accuracy_score(y_test,y_pred)
        precision = precision_score(y_test,y_pred)
        recall = recall_score(y_test,y_pred)
        auc = roc_auc_score(y_test,y_pred_proba)

        metrics_dict = {
            'accuracy' : accuracy,
            'precision' : precision,
            'recall' :recall,
            'auc' : auc
        }
        logger.debug(f"Evaluation metrics calculated \n {metrics_dict}",exc_info=True)
        return metrics_dict
    
    except Exception as e:
        logger.error('Error during model evaluation {e}')
        raise

def save_metrics(metrics:dict, file_path : str) ->None:
    try:
        Path.mkdir(Path(file_path).parent,exist_ok=True,parents=True)

        with open(file_path ,'w') as file:
            json.dump(metrics,file,indent=4)

        logger.debug(f'Metrics saved to {file_path}')
        return 

    except Exception as e:
        logger.error(f'Some error occurred {e}')
        raise
def main():
    try:
        clf = load_model('./models/model.pkl')
        test_data = load_data('./data/processed/test_tfidf.csv')

        x_test = test_data.iloc[:,:-1].values
        y_test = test_data.iloc[:,-1].values

        metrics = evaluate_model(clf,x_test,y_test)
        save_metrics(metrics,'reports/metrics.json')
    
    except Exception as e:
        logger.error(f'Failed to complete the model evaluation process {e}')

if __name__ == "__main__":
    main()

    