from pkg.helper import utils


# fake config file
CONTENT = ("""
[config]
work_dir = current_dir
""")


def test_write_config_file_work_dir_case(tmp_path):
    # create temp config.ini
    temp_dir = tmp_path / "src"
    temp_dir.mkdir()
    temp_file = temp_dir / "config.ini"
    temp_file.write_text(CONTENT, encoding="utf-8")
    assert temp_file.read_text(encoding="utf-8") == CONTENT
    assert len(list(tmp_path.iterdir())) == 1

    ctx = {
        'debug': True,
        'command': 'config',
        'src_dir': f'{temp_dir}',
        'arg': 'new_dir',
        'opt': 'work_dir'
    }

    utils.write_config_file(ctx=ctx)

    with open(f"{ctx['src_dir']}/config.ini", 'r') as f1:
        result = f1.read()

    assert "work_dir = new_dir" in result

    # Path.unlink("temp_file")

# print(f"result.output: {result.output}")
