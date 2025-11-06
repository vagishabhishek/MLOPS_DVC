import yaml
from pathlib import Path
from src.Logger.logger_factory import LoggerFactory
from src.utils.get_project_root import get_project_root

logger = LoggerFactory().create()

try:
    project_root = Path(get_project_root())
    config_path = project_root / 'config/data_paths.yaml'
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)  # <-- actually read YAML
    
    raw_data_path = project_root / config['raw_data']
    cleaned_data_path = project_root / config['data_cleaned']
    processed_data_path = project_root / config['data_processed']
    
    logger.info(f"Project root determined: {project_root}")
    logger.info(f"Configuration path determined: {config_path}")
    
except Exception as e:
    logger.error(f"Error determining paths: {e}, set paths correctly in config/data_paths.yaml")

with open(raw_data_path, 'r',encoding='utf-8') as file:
    for i, line in enumerate(file):
        print(line)
        if i >= 4:  # print first 5 lines
            break

    