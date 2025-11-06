
from src.Logger.logger_factory import LoggerFactory
import pandas as pd
def main():
    logger = LoggerFactory().create()
    logger.info("App started")
    print("Hello from mlops-dvc!")
    
    try : 
        df = pd.read_csv("data/raw/winequality-red.csv", sep=";")
    except Exception as e:
        logger.error(f"Error reading the CSV file: {e}")
        return


if __name__ == "__main__":
    
    main()
