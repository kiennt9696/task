from common_utils.util import load_config

from task import create_app
import os


config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
config = None
if os.path.isfile(config_file):
    config = load_config(config_file)

application = create_app()
