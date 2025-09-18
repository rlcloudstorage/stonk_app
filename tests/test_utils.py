from configparser import ConfigParser
from pathlib import Path

from click import Command, Context

from pkg.helper import utils


# fake config file
config_file = ("""
[default]
root_dir = root_dir
work_dir = current_dir
config_file = temp_file
""")

# instanciate config object
config_obj = ConfigParser()
config_obj.read_string(config_file)


def test_write_config_file_work_dir_case(tmp_path):
    # create temp_file
    temp_dir = tmp_path/"temp_dir"
    temp_dir.mkdir()
    temp_file = temp_dir/"test_config.ini"
    temp_file.write_text(config_file)
    # check if file exists
    assert temp_file.is_file()
    # read config data into temp_file
    config_text = temp_file.read_text()
    assert config_text == config_file

    # fake click.Context object and option
    ctx = Context(
        command=Command("config"),
        obj={
            'debug': False,
            'root_dir': 'root_dir',
            'config_obj': None,
            'config_obj': config_obj
        },
    )
    ctx.info_name = "config"
    ctx.params = {'work_dir': 'new_dir', 'dummy': None}
    option = "work_dir"

    with ctx:
        # test with fake click.Context and option
        utils.write_config_file(ctx=ctx, option=option)

        # new config is in io.TextIOWrapper with name="temp_file"
        with open("temp_file", 'r') as f1:
            result = f1.read()

        assert "work_dir = new_dir" in result

    Path.unlink("temp_file")

# print(f"result.output: {result.output}")
