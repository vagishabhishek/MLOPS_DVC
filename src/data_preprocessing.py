from src.logger.logger import setup_logger
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from nltk.stem import WordNetLemmatizer
from pathlib import Path
from src.utility.project_root import get_project_root
import string

logger = setup_logger("data preprocessing")

def transform_text(text):
    """
        Transforms the input text by converting it to lowercase,tokenizing ,
        removing stop words and puctuataion and lemmatizing.
    """
    try:
        
        lemmatizer = WordNetLemmatizer()
        
        text = text.lower()
        
        text = nltk.word_tokenize(text)
        
        text = [word for word in text if word.isalnum()]
        
        text = [word for word in text if word not in stopwords.words('english')\
            and word not in string.punctuation]
        
        text = [lemmatizer.lemmatize(word) for word in text]
        
        return " ".join(text)
    
    except Exception as e:
        raise RuntimeError(f'Preprocessing faild. {e}',exc_info=True)

    
def preprocess_df(df,text_column = 'text',target_column = 'target'):
    """
        Preprocess the dataFrame by encoding the target column ,removing duplicates and transforming text column
    """
    
    try:
        logger.debug('Starting preprocessing for DataFrame')
        
        encoder = LabelEncoder()
        df[target_column] = encoder.fit_transform(df[target_column])
        logger.debug(f'Target Column encoded ')
        
        df = df.drop_duplicates(keep= 'first')
        
        df.loc[:,text_column] = df[text_column].apply(transform_text)
        
        logger.debug(f"""Text column transformed \n {df.head(2)}""")
                    
        
        return df
    except KeyError as e:
        logger.error(f'column not found {e}')
        raise
    except Exception as e:
        logger.error(f"unexpectd error occureed {e}")
        raise

def main(text_column = "text",target_column = "target"):
    """
        Main function
    """   
    try:
        train_data = pd.read_csv('./data/raw/train.csv')
        test_data = pd.read_csv('./data/raw/test.csv')
        logger.debug('data loaded properly')
        
        train_processed_data = preprocess_df(train_data,text_column,target_column)
        logger.debug("Trainig data processed")
        test_processed_data = preprocess_df(test_data,text_column,target_column)
        logger.debug("Testing data preprocessed")
        
        data_path = Path(get_project_root())/"data"/"interim"
        Path.mkdir(data_path,exist_ok=True,parents=True)
        
        train_processed_data.to_csv(data_path/"train_processed.csv",index = False)
        test_processed_data.to_csv(data_path/"test_processed.csv",index = False)
        
        logger.debug('Processed data saved to %s',data_path)
        
    except FileNotFoundError as e:
        logger.error('File not found %s',e)
        raise
    except pd.errors.EmptyDataError as e:
        logger.error("No data %s",e)
        raise
    except Exception as e:
        logger.error(f'Failed to complete data preprocessing process {e}',exc_info=True)
        
if __name__ == "__main__":
    main()


        
         
        
        
        
        

    


    