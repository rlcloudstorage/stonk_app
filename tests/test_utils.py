import click#, pytest

from pkg.helper import utils


config_file = """\
[default]
work_dir = current_dir
config_file = config.ini
"""

ctx = click.Context(
    command=click.Command("config"),
    obj={
        'debug': True,
        'work_dir': 'current_dir',
        'config_file': None
    },
)
ctx.info_name = "config"
ctx.params = {'work_dir': 'new_dir', 'dummy': None}

key = "work_dir"


def test_write_config_file_case_work_dir(tmpdir):
    with ctx:
        ctx.obj["config_file"] = tmpdir.join(config_file)
        utils.write_config_file(ctx=ctx, key=key)
        assert "new_dir" in config_file

# def writetoafile(fname):
#     with open(fname, 'w') as fp:
#         fp.write('Hello\n')

# def test_writetofile(tmpdir):
#     file = tmpdir.join('output.txt')
#     writetoafile(file.strpath)  # or use str(file)
#     assert file.read() == 'Hello\n'

# print(f"result.output: {result.output}")
