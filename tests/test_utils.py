
import os
import sys
import inspect
import pytest

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils # noqa


@pytest.mark.incremental
class TestUtils(object):
    def test_read_from_configuration(self):
        config = utils.read_from_configuration('../config.yaml')
        assert config

    def test_get_db_connect_string(self):
        config = utils.read_from_configuration('../config.yaml')
        connect_string = utils.get_db_connect_string(config)

        assert connect_string
        assert 'anoop' in connect_string
        assert 'iamanoop' in connect_string

    def test_get_db_connect_string_with_credentials(self):
        config = utils.read_from_configuration('../config.yaml')
        connect_string = utils.get_db_connect_string(
            config, username='rob', password='iamrob')

        assert connect_string
        assert 'rob' in connect_string
        assert 'iamrob' in connect_string
