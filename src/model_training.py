from pathlib import Path
from src.logger.logger import setup_logger
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from src.utility.load_yaml import read_yaml
from dvclive import Live

logger = setup_logger("model-trainer")


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV."""
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"Data read from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Could not read file from {file_path}. Error: {e}")
        raise


def train_model(x_train: np.ndarray, y_train: np.ndarray, params: dict) -> RandomForestClassifier:
    """Train RandomForest model incrementally to log step-wise metrics."""
    try:
        if x_train.shape[0] != y_train.shape[0]:
            raise ValueError("Mismatch in number of samples between x_train and y_train")

        n_estimators = params.get("n_estimators", 100)
        random_state = params.get("random_state", 42)

        logger.debug(f"Initializing RandomForestClassifier with params: {params}")

        # Step-by-step training simulation for DVCLive plotting
        with Live(save_dvc_exp=True) as live:
            for step in range(10, n_estimators + 1, 10):
                clf = RandomForestClassifier(
                    n_estimators=step,
                    random_state=random_state,
                )
                clf.fit(x_train, y_train)

                acc = clf.score(x_train, y_train)
                live.log_metric("train_accuracy", acc)
                live.log_param("n_estimators", step)
                live.next_step()

                logger.debug(f"Step {step}: Train Accuracy = {acc:.4f}")

        # Final model with full estimators
        clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        clf.fit(x_train, y_train)
        logger.debug("Final model trained with all estimators.")
        return clf

    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise


def save_model(model, file_path: str) -> None:
    """Save the trained model to disk."""
    try:
        Path(file_path).parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "wb") as f:
            pickle.dump(model, f)
        logger.debug(f"Model saved to {file_path}")
    except Exception as e:
        logger.error(f"Error occurred while saving model: {e}")
        raise


def main():
    """Main entry for training."""
    try:
        params = read_yaml("./params.yaml")["model_training"]
        train_data = load_data("./data/processed/train_tfidf.csv")

        x_train = train_data.iloc[:, :-1].values
        y_train = train_data.iloc[:, -1].values

        clf = train_model(x_train, y_train, params)
        save_model(clf, "models/model.pkl")

    except Exception as e:
        logger.error(f"Failed to complete the model building process {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
