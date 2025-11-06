from src.Logger.logger_factory import LoggerFactory


logger = LoggerFactory().create()
logger.info("Inside Linear regression")

try:
    print(df)
    
except Exception as e:
    logger.exception(e)