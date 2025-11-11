"""
src/pkg/__init__.py
-------------------
Setup logger, configuration setting, and CLI entry point

Functions:
    click_logger(): Log some click Contest object info
    start_cli(): pyproject.toml entry point for CLI
Variables:
    config_obj: ConfigParser object
"""
import logging, logging.config
import os, tomllib

from configparser import ConfigParser

from dotenv import load_dotenv


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# read environment variables from .env file
load_dotenv(os.path.join(os.path.join(ROOT_DIR, "src/"), ".env"))

# set up logging
logging.config.fileConfig(fname=os.path.join(os.path.join(ROOT_DIR, "src/"), "logger.ini"))

# check work_dir exists, if not create it
os.makedirs(os.path.join(ROOT_DIR, "work_dir"), exist_ok=True)

# create chart folder in work_dir
os.makedirs(os.path.join(f"{ROOT_DIR}/work_dir", "chart"), exist_ok=True)

# create data folder in work_dir
os.makedirs(os.path.join(f"{ROOT_DIR}/work_dir", "data"), exist_ok=True)

# create heatmap folder in work_dir
os.makedirs(os.path.join(f"{ROOT_DIR}/work_dir", "heatmap"), exist_ok=True)

# create strategy folder in work_dir
os.makedirs(os.path.join(f"{ROOT_DIR}/work_dir", "strat"), exist_ok=True)

# create getlist() converter (used for reading ticker symbols)
config_obj = ConfigParser(
    allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]}
)

# get info from pyproject.toml file
with open(f"{ROOT_DIR}/pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    config_obj.add_section("app")
    config_obj["app"]["name"] = data['project']['name']
    config_obj["app"]["version"] = data['project']['version']
    config_obj["app"]["url"] = data['project']['urls']['Source']

# add work directory to config
config_obj.add_section("config")
config_obj.set(section="config", option="work_dir", value=os.path.join(ROOT_DIR, "work_dir"))

# create main config file
config_file = os.path.join(os.path.join(ROOT_DIR, "src/"), "config.ini")

# populate main config.ini file
with open(config_file, "w") as cf:
    # gather config files from other apps
    for root, dirs, files in os.walk(os.path.join(os.path.join(ROOT_DIR, "src/"), "pkg")):
        for filename in files:
            if filename == "config.ini":
                config_obj.read(os.path.join(root, filename))

    # add values from .env file (if any)
    if os.getenv("CHART_POOL"):
        config_obj.set(section="scrape", option="chart_pool", value=os.getenv("CHART_POOL"))
    if os.getenv("HEATMAP_POOL"):
        config_obj.set(section="scrape", option="heatmap_pool", value=os.getenv("HEATMAP_POOL"))
    if os.getenv("OHLC_POOL"):
        config_obj.set(section="data", option="ohlc_pool", value=os.getenv("OHLC_POOL"))
    if os.getenv("SIGNAL_POOL"):
        config_obj.set(section="data", option="signal_pool", value=os.getenv("SIGNAL_POOL"))

    config_obj.write(cf)

# config file exists, create configparser object
config_obj.read(config_file)

# # put config section/option data into a dictionary
# config_dict = dict(
#     (section, dict((option, config_obj.get(section, option))
#     for option in config_obj.options(section)))
#     for section in config_obj.sections()
# )


# start command line interface
def start_cli():
    """pyproject.toml entry point for CLI"""
    from . import app_cli

    app_cli.group()


def click_logger(ctx: object, logger: object) -> None:
    """
    Log some click Contest object info
    ----------------------------------
    Args:
        ctx (click.core.Context object):
        logger (logging.Logger):
    Returns:
        None:
    """
    logger.debug(
        f"{ctx.info_name}()\n - ctx: {ctx}\n"
        f" - ctx.parent: {ctx.parent}\n"
        f" - ctx.command: {ctx.command} {type(ctx.command)}\n"
        f" - ctx.info_name: {ctx.info_name} {type(ctx.info_name)}\n"
        f" - ctx.params: {ctx.params} {type(ctx.params)}\n"
        f" - ctx.args: {ctx.args} {type(ctx.args)}\n"
        f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
        f" - ctx.default_map: {ctx.default_map} {type(ctx.default_map)}\n"
    )
