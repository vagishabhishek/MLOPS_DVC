import logging
from src.logger.logger import setup_logger
import pandas as pd
from sklearn.model_selection import train_test_split
from src.utility.load_yaml import read_yaml

logger = setup_logger("Data Loader")
def load_data(data_url : str) -> pd.DataFrame:
    """
        Load data from csv
    """
    
    logger.info("Data Loading Started .....")
    
    try:
        
        df = pd.read_csv(data_url,encoding='latin')
        logger.debug(f"Data loaded from  {data_url}")
        return df
    
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV File {e}',exc_info=True)
        
        raise
    except Exception as e:
        logger.error(f'Unexpected error occureed while loading data {e}',exc_info=True)
        
def preprocess_data(df : pd.DataFrame) ->pd.DataFrame:
    """
        Preprocess the details
    """
    try : 
        logger.debug("Data Preprocessing Started")
        df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],inplace=True)
        df.rename(
            columns={
                'v1' : 'target',
                'v2' : 'text'
            },inplace=True
        )
        logger.debug(f"Removed columns {['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']}")
        
        return df
        
    except KeyError as e:
        logger.error(f"Missing column in the dataframe : {e}",exc_info=True)
        
        raise
    except Exception as e:
        logger.error(f"Unexpected error during prepprocessing : {e}",exc_info=True)
        raise
    
def save_date(train_data : pd.DataFrame, test_data : pd.DataFrame,data_path : str) ->None:
    """
        save the train and test datasets
    """
    from pathlib import Path
    try :
        raw_data_path = Path(data_path) / "raw"
        Path.mkdir(raw_data_path,exist_ok=True,parents=True)
        train_data.to_csv(Path(raw_data_path)/"train.csv",index=False)
        test_data.to_csv(Path(raw_data_path)/"test.csv",index=False)
        logger.debug(f"Train and test data saved to {raw_data_path}")
        
    except Exception as e:
        logger.error(f"Unexpected error occurred : {e}",exc_info=True)
        raise
    
def main():
    try:
        params = read_yaml('./params.yaml')
        test_size = params['data_ingestion']['test_size']
        #test_size = 0.2
        data_path = r"C:\Users\Vagis\Downloads\spam.csv"
        df = load_data(data_url=data_path)
        
        final_df = preprocess_data(df)
        train_data ,test_data = train_test_split(final_df,test_size=test_size,random_state=42)
        
        save_date(train_data,test_data,data_path='./data')
        
    except Exception as e:
        logger.error(f'Failed to complete data ingestion process {e}')
        raise
        
if __name__ == "__main__":
    main()
        
        
     
