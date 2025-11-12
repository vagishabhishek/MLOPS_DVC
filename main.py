# src/pipeline.py
import src.logger.logger as logger # Import logger module globally first
import src.data_ingestion as ingestion
import src.data_preprocessing as preprocessing
import src.feature_engineering as featureengineering
import src.model_training as model_trainer
import src.model_evaluater as model_evaluator 
import pandas as pd

# The global timestamp and folder are set here, once.

# Get a logger for the pipeline script itself
logger = logger.setup_logger("Pipeline Runner")

def run_full_pipeline():
    logger.info("Starting MLOps pipeline run.")
    
    # Run Data Ingestion (will reuse the global timestamp)
    logger.info("--- Starting Data Ingestion ---")
    # ingestion.main() handles the logic to load data and save raw files
    ingestion.main() 

    # Run Data Preprocessing (will reuse the global timestamp)
    logger.info("--- Starting Data Preprocessing ---")
    # preprocessing.main() handles the logic to load raw and save processed
    preprocessing.main()
    
    logger.info("--- Starting Feature Engineering ---")
    featureengineering.main()

    logger.info("--- Starting Model Training ---")
    model_trainer.main()

    logger.info("--- Starting Model Evaluation ---")
    model_evaluator.main()

    logger.info("Pipeline run complete.")

if __name__ == "__main__":
    run_full_pipeline()
