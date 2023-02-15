
from src.autoexplain.subcommands import generate_readme, generate_unittests, set_key
import configparser
import os

def test_generate_readme():
    """
    This function tests the generate_readme function
    """
    os.remove()
    generate_readme(output_file="fake_README.md", silent=True)
    assert os.path.exists("fake_README.md")
    os.remove("fake_README.md")

def test_generate_unittests():
    """
    This function tests the generate_unittests function
    """
    generate_unittests(files=["test.py", "fake_test_unittests.py"], silent=True)
    assert os.path.exists("test_unittests.py")

def test_set_key():
    """
    This function tests the set_key function
    """
    set_key(["1234567890123456789012345678901234567890"])
    config = configparser.ConfigParser()
    config.read('.aexconfig')
    assert config.has_section('openai')
    assert config.has_option('openai', 'openai_key')
    assert config.get('openai', 'openai_key') == "1234567890123456789012345678901234567890"

