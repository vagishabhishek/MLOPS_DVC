from src.logger.logger import setup_logger
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from pathlib import Path
import json
from src.utility.load_yaml import read_yaml
from dvclive import Live

logger = setup_logger("model-evaluater")


def load_model(file_path: str):
    """Load the trained model from a file."""
    try:
        with open(file_path, "rb") as file:
            model = pickle.load(file)
        logger.debug(f"Model loaded from {file_path}")
        return model
    except FileNotFoundError as e:
        logger.error(f"File not found {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while loading the model {e}")
        raise


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV File."""
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"Data loaded from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Some error occurred {e}")
        raise


def evaluate_model(clf, x_test: np.ndarray, y_test: np.ndarray, params: dict) -> dict:
    """Evaluate trained model and log metrics to DVCLive."""
    try:
        y_pred = clf.predict(x_test)

        # Use predict_proba for ROC AUC
        if hasattr(clf, "predict_proba"):
            y_pred_proba = clf.predict_proba(x_test)[:, 1]
        else:
            # fallback for models without predict_proba
            y_pred_proba = y_pred

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)

        metrics_dict = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "auc": auc,
        }

        # Log metrics and params to DVCLive with step tracking
        with Live(save_dvc_exp=True, resume=True) as live:
            live.log_metric("val_accuracy", accuracy)
            live.log_metric("val_precision", precision)
            live.log_metric("val_recall", recall)
            live.log_metric("val_auc", auc)
            live.log_params(params)
            live.next_step()

        logger.debug(f"Evaluation metrics calculated: {metrics_dict}")
        return metrics_dict

    except Exception as e:
        logger.error(f"Error during model evaluation {e}")
        raise


def save_metrics(metrics: dict, file_path: str) -> None:
    """Save evaluation metrics to JSON file."""
    try:
        Path(file_path).parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "w") as file:
            json.dump(metrics, file, indent=4)
        logger.debug(f"Metrics saved to {file_path}")
    except Exception as e:
        logger.error(f"Some error occurred {e}")
        raise


def main():
    """Main entry point for model evaluation."""
    try:
        params = read_yaml("./params.yaml")
        clf = load_model("./models/model.pkl")
        test_data = load_data("./data/processed/test_tfidf.csv")

        x_test = test_data.iloc[:, :-1].values
        y_test = test_data.iloc[:, -1].values

        metrics = evaluate_model(clf, x_test, y_test, params=params)
        save_metrics(metrics, "reports/metrics.json")

    except Exception as e:
        logger.error(f"Failed to complete the model evaluation process {e}", exc_info=True)


if __name__ == "__main__":
    main()
