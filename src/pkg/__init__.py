"""src/pkg/__init__.py"""
import logging, logging.config
import os, tomllib

from configparser import ConfigParser

from dotenv import load_dotenv


root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(root_dir, "src")

# read environment variables from .env file
load_dotenv(os.path.join(src_dir, ".env"))

# check work_dir exists, if not create it
os.makedirs(os.path.join(root_dir, "work_dir"), exist_ok=True)

# set up logging
logging.config.fileConfig(fname=os.path.join(src_dir, "logger.ini"))

# create getlist() converter (used for reading ticker symbols)
config_obj = ConfigParser(
    allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]}
)

# create main config file if if does not exist
config_file = os.path.join(src_dir, "cfg_main.ini")
# if not os.path.isfile(config_file):

# create the config file
with open(config_file, "w") as cf:

    # gather config files from other apps
    for root, dirs, files in os.walk(os.path.join(src_dir, "pkg")):
        for filename in files:
            if filename.startswith("cfg_") and filename.endswith(".ini"):
                # f_name = filename.removeprefix('cfg_').removesuffix('.ini')
                # config_obj.add_section(f_name)
                config_obj.read(os.path.join(root, filename))

    # get info from pyproject.toml file and add to config
    with open(f"{root_dir}/pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        config_obj.add_section("app")
        config_obj["app"]["name"] = data['project']['name']
        config_obj["app"]["version"] = data['project']['version']
        config_obj["app"]["url"] = data['project']['urls']['Source']

    config_obj.add_section("config")
    config_obj.set(section="config", option="root_dir", value=root_dir)
    config_obj.set(section="config", option="work_dir", value=os.path.join(root_dir, "work_dir"))
    config_obj.set(section="config", option="config_file", value=config_file)
    config_obj.write(cf)

# config file exists, create configparser object
config_obj.read(config_file)

# put config section/option data into a dictionary
config_dict = dict(
    (section, dict((option, config_obj.get(section, option))
    for option in config_obj.options(section)))
    for section in config_obj.sections()
)

# # add to config_dict
# if os.getenv("CHART_LIST"):
#     config_dict["default"]["chart_list"] = os.getenv("CHART_LIST")
# if os.getenv("DATA_LIST"):
#     config_dict["default"]["data_list"] = os.getenv("DATA_LIST")

# Start command line interface
def start_cli():
    """pyproject.toml entry point for CLI"""
    from . import app_cli

    app_cli.group()
