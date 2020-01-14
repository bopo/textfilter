#!/usr/bin/env python

"""Tests for `textfilter` package."""
from click.testing import CliRunner

from textfilter import __main__
from textfilter.textfilter import TextFilter


# def test_first_character():
#     gfw = TextFilter()
#     gfw.add("1989年")
#
#     assert gfw.filter("1989", "*") == "****"
#     # assert '****' == '1989'

    # gfw = NaiveFilter()
    # # gfw = BSFilter()
    # # gfw = DFAFilter("keywords")
    # gfw.parse("keywords")
    #
    # t = time.time()
    # print(gfw.filter("法轮功 我操操操", "*"))
    # print(gfw.filter("针孔摄像机 我操操操", "*"))
    # print(gfw.filter("售假人民币 我操操操", "*"))
    # print(gfw.filter("传世私服 我操操操", "*"))
    # print(time.time() - t)


# @pytest.fixture
# def response():
#     """Sample pytest fixture.
#
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
#
#
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string
#
#
def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(__main__.main)

    assert result.exit_code == 0
    assert 'textfilter.__main__.main' in result.output

    help_result = runner.invoke(__main__.main, ['--help'])

    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
