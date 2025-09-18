"""src/pkg/helper/utils.py\n
def print_okay(msg: str)->None\n
def write_config_file(ctx: object, key: str)->None
"""
import logging


logger = logging.getLogger(__name__)


def print_okay(msg: str)->None:
    print(f"okay: {msg}")


def write_config_file(ctx: object, option: str)->None:
    """
    Write new value to the appropriate config file
    ----------------------------------------------
    Args:
        ctx (click.Context): Dictionary like object.
        key (str): click.Context.params key
    Returns:
        None:
    """
    if ctx.obj["debug"]:
        logger.debug(
            f"write_config_file(ctx={ctx}, option={option})"
        )
    match option:
        case "work_dir":
            config_obj = ctx.obj["config_obj"]
            try:
                config_obj.set(section="default", option=option, value=ctx.params[option])
            except Exception as e:
                logger.debug(f"*** ERROR *** {e}")

            # import sys
            # config_obj.write(sys.stdout)

            with open(config_obj["default"]["config_file"], "w") as cf:
                config_obj.write(cf)

# # Create getlist() converter, used for reading ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]})
