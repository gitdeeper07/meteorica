"""
Unit tests for command line interface
"""

import unittest
import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.cli import main


class TestCLI(unittest.TestCase):
    """Test CLI commands"""
    
    @patch('sys.argv', ['meteorica', '--help'])
    def test_help(self):
        """Test help command"""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['meteorica', 'calculate', '--mcc', '0.85', '--twi', '0.25'])
    def test_calculate(self):
        """Test calculate command"""
        # This should run without errors
        try:
            main()
        except SystemExit:
            pass
    
    @patch('sys.argv', ['meteorica', 'fireball', '--velocity', '18.6', 
                       '--angle', '18.5', '--diameter', '19'])
    def test_fireball(self):
        """Test fireball command"""
        try:
            main()
        except SystemExit:
            pass


if __name__ == '__main__':
    unittest.main()
