"""src/pkg/helper/utils.py\n
def write_config_file(ctx: object, key: str)->None
"""
import logging

from configparser import ConfigParser


logger = logging.getLogger(__name__)


def write_config_file(ctx: dict)->None:
    """
    Write new value to the appropriate config file
    ----------------------------------------------
    Args:
        ctx (dict): dictionary containing command, argument, option, and src_dir path
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"write_config_file(ctx={ctx})")

    match ctx["opt"]:

        case "work_dir":
            config_obj = ConfigParser()
            config_obj.read(f"{ctx['src_dir']}/{ctx['command']}.ini")

            try:
                config_obj.set(section=ctx["command"], option=ctx["opt"], value=ctx["arg"])
            except Exception as e:
                logger.debug(f"*** ERROR *** {e}")

            # import sys
            # config_obj.write(sys.stdout)

            with open(f"{ctx['src_dir']}/{ctx['command']}.ini", "w") as cf:
                config_obj.write(cf)

        case _:
            pass

# # Create getlist() converter, used for reading ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]})
