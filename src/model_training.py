from pathlib import Path
from src.logger.logger import setup_logger
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from src.utility.load_yaml import read_yaml

logger = setup_logger('model-trainer')

def load_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"Data read from {file_path} ")
        return df
    except pd.errors.ParserError as e:
        logger.error(f"Could not parse {file_path}. Some error occurred")
        raise
    except FileNotFoundError:
        logger.error(f"{file_path} not found.")
        raise
    except Exception as e:
        logger.error(f"Could not read file from {file_path}. Some error occurred {e}")
        raise


def train_model(x_train: np.ndarray, y_train: np.ndarray, params: dict) -> RandomForestClassifier:
    try:
        if x_train.shape[0] != y_train.shape[0]:
            raise ValueError("Mismatch in number of samples of x_train and y_train")

        clf = RandomForestClassifier(**params)
        logger.debug(f"Initializing RandomForestClassifier with parameters {params}")

        clf.fit(x_train, y_train)
        logger.debug(f"Model Trained with {params}")
        return clf

    except Exception as e:
        logger.error(f"Model training failed {e}")
        raise


def save_model(model, file_path: str) -> None:
    """
        Save the trained model in a file
    """
    try:
        Path.mkdir(Path(file_path).parent, exist_ok=True, parents=True)

        with open(file=file_path, mode="wb") as f:
            pickle.dump(model, f)
        logger.debug(f"Model saved to {file_path}")

    except FileNotFoundError as e:
        logger.error(f"File could not be written to {file_path} ")
        raise
    except Exception as e:
        logger.error(f"Error occurred while saving model")
        raise


def main():
    try:
        params = read_yaml(file_path="./params.yaml")
        params = params['model_training']

        train_data = load_data('./data/processed/train_tfidf.csv')

        x_train = train_data.iloc[:, :-1].values
        y_train = train_data.iloc[:, -1].values

        clf = train_model(x_train=x_train, y_train=y_train, params=params)

        model_save_path = 'models/model.pkl'
        save_model(clf, model_save_path)
    except Exception as e:
        logger.error(f'Failed to complete the model building process {e}', exc_info=True)
        raise


if __name__ == "__main__":
    main()
