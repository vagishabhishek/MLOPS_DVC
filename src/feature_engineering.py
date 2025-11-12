
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from src.logger.logger import setup_logger
from src.utility.load_yaml import read_yaml

logger = setup_logger("feature_engineering")

def fill_nulls_data(file_path : str) ->pd.DataFrame :
    #laod data

    try:
        df = pd.read_csv(file_path)
        df.fillna('',inplace=True)
        logger.debug("Data loaded and NaN's filled from %s",file_path)
        return df

    except pd.errors.ParserError as e:
        logger.error(f'Failed to parse the csv file{e}')
        raise
    except Exception as e:
        logger.error("Unexpected error occurred while loading the data %s",e)
        raise

def apply_tfidf(train_data: pd.DataFrame,test_data : pd.DataFrame,max_features:int)->tuple:

    try:
        vectorizer = TfidfVectorizer(max_features=max_features)

        x_train , x_test = train_data['text'].values,test_data['text'].values
        y_train , y_test = train_data['target'].values,test_data['target'].values

        x_train_vec = vectorizer.fit_transform(x_train)
        x_test_vec = vectorizer.transform(x_test)

        train_df = pd.DataFrame(x_train_vec.toarray())
        train_df['label'] = y_train
        test_df = pd.DataFrame(x_test_vec.toarray())
        test_df['label'] = y_test

        logger.debug('TfIdf Applied and data transformed')
        return train_df,test_df
    
    except Exception as e:
        logger.error("Error occurred during Tfidf Application %s ",e)
        raise

def save_data(df:pd.DataFrame,file_path:str) -> None:
    try:
        #make parent directory of file path if it does not exist
        Path.mkdir(Path(file_path).parent,exist_ok=True,parents=True)

        #write to file path
        df.to_csv(file_path,index=False)

        #log file write action
        logger.debug('Data Saved to %s',file_path)
    except Exception as e:
        logger.error(f'Unexpected error occurred while saving file : {e}')
        raise

def main():
    try:
        params = read_yaml(file_path='./params.yaml')
        max_features = params['feature_engineering']['max_features']
        # max_features = 50

        train_data = fill_nulls_data('./data/interim/train_processed.csv')
        logger.debug("train data nulls removed")

        test_data = fill_nulls_data('./data/interim/test_processed.csv')
        logger.debug('test data nulls removed')

        train_df , test_df = apply_tfidf(train_data=train_data,test_data=test_data,max_features=max_features)

        save_data(train_df,Path("./data")/"processed" /"train_tfidf.csv")
        save_data(test_df,Path('./data')/"processed"/"test_tfidf.csv" )
    except Exception as e:
        logger.error(f'Failed to complete the feature engineering process : {e}')
        raise

if __name__ == "__main__":
    main()

    



    
    

    


