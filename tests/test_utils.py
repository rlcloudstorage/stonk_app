from click import Command, Context

from pkg.helper import utils


config_file = ("""
[default]
work_dir = current_dir
config_file = config.ini
""")

ctx = Context(
    command=Command("config"),
    obj={
        'debug': False,
        'work_dir': 'current_dir',
        'config_file': None
    },
)
ctx.info_name = "config"
ctx.params = {'work_dir': 'new_dir', 'dummy': None}

option = "work_dir"


def test_write_config_file_work_dir_case(tmp_path):
    # create temp_dir
    temp_dir = tmp_path/"temp_dir"
    temp_dir.mkdir()
    # create file in temp_dir
    temp_file = temp_dir/"config.ini"
    temp_file.write_text(config_file)
    # check if file exists
    assert temp_file.is_file()
    # read file's contents
    assert temp_file.read_text() == config_file
    assert "work_dir = current_dir" in temp_file.read_text()

    ctx.obj["config_file"] = temp_file

    with ctx:
        utils.write_config_file(ctx=ctx, option=option)
        assert "work_dir = new_dir" in temp_file.read_text()

# print(f"result.output: {result.output}")
