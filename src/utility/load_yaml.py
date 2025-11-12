import yaml
from src.logger.logger import setup_logger

logger = setup_logger("yaml reader")
def read_yaml(file_path:str='./params.yaml')->dict:

    try:

        with open(file=file_path,mode='r') as file:
            params = yaml.safe_load(file)
            logger.debug(f'params loaded from {file_path}')
            return params
    except FileNotFoundError as e:
        logger.error(f'{file_path} not found')
        raise
    except yaml.YAMLError as e:
        logger.error(f'Error reading yaml {file_path}')
        raise
    except Exception as e:
        logger.error(f'Some error occurred while reading yaml file in {file_path}',exc_info=True)
        raise
