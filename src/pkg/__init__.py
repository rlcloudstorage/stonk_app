"""src/pkg/__init__.py"""
import logging, logging.config
import os, tomllib

from configparser import ConfigParser

from dotenv import load_dotenv


root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# read environment variables from .env file
load_dotenv(os.path.join(os.path.join(root_dir, "src/"), ".env"))

# check work_dir exists, if not create it
os.makedirs(os.path.join(root_dir, "work_dir"), exist_ok=True)

# set up logging
logging.config.fileConfig(fname=os.path.join(os.path.join(root_dir, "src/"), "logger.ini"))

# create getlist() converter (used for reading ticker symbols)
config_obj = ConfigParser(
    allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]}
)

# files = ["file1.txt", "file2.txt"]  # Example list of files
# checksums = [(filename, hashlib.md5(read_file_as_bytes(filename)).hexdigest()) for filename in files]
# print(checksums)

# create main config file if if does not exist
config_file = os.path.join(os.path.join(root_dir, "src/"), "config.ini")

if not os.path.isfile(config_file):

    # populate src/config.ini file
    with open(config_file, "w") as cf:

        # gather config files from other apps
        for root, dirs, files in os.walk(os.path.join(os.path.join(root_dir, "src/"), "pkg")):
            for filename in files:
                if filename == "config.ini":
                    config_obj.read(os.path.join(root, filename))

        # get info from pyproject.toml file and add to config
        with open(f"{root_dir}/pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            config_obj.add_section("app")
            config_obj["app"]["name"] = data['project']['name']
            config_obj["app"]["version"] = data['project']['version']
            config_obj["app"]["url"] = data['project']['urls']['Source']

        config_obj.add_section("config")
        config_obj.set(section="config", option="work_dir", value=os.path.join(root_dir, "work_dir"))
        config_obj.write(cf)

# config file exists, create configparser object
config_obj.read(config_file)

# # put config section/option data into a dictionary
# config_dict = dict(
#     (section, dict((option, config_obj.get(section, option))
#     for option in config_obj.options(section)))
#     for section in config_obj.sections()
# )

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
