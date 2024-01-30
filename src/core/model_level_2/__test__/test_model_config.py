import logging

from src.model_level_2.model import ModelConfigs

class CustomConfigs(ModelConfigs):
    name: str

def test_config():
    m = CustomConfigs(name='A')
    logging.error(m.__repr__())