#!/usr/bin/env python

"""Tests for `timelapser` package."""


import unittest
from click.testing import CliRunner

from timelapser import timelapser
from timelapser import cli


class TestTimelapser(unittest.TestCase):
    """Tests for `timelapser` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        #result = runner.invoke(cli.main)
        #assert result.exit_code == 0
        #assert 'timelapser.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help' in help_result.output
        assert 'Show this message and exit.' in help_result.output
