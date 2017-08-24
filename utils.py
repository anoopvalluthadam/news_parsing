# -*- coding: utf-8; -*-
#

# This file is part of Mandriva Management Console (MMC).
#
# News Parsing is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# News Parsing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
#
# @author : Anoop Valluthadam <anoopvalluthadam@gmail.com>

import yaml


def get_db_connect_string(configuraion, username='anoop',
                          password='iamanoop', name='mongodb'):
    """
    Get Db connect string from the configuraion
    Args:
        configuraion (Dictionary): configuraion
    Returns:
        connect_string (string): DB connect string
    """

    connect_string = None
    if 'DB' in configuraion:
        for db in configuraion['DB']:
            if name == db['name']:
                connect_string = db['connect_string']
    else:
        print('No DB details in the configuraion')
        exit(1)
    if connect_string:
        connect_string = connect_string.replace('username', username)
        connect_string = connect_string.replace('password', password)
    else:
        print('Could not find connect_string!')
        exit(1)

    return connect_string


def read_from_configuration(file_name):
    """
    Read from configuraion file
    Args:
        file_name (string): File name of the configuraion
    Returns:
        yaml_content (Dictionary): configuraion
    """

    with open(file_name, 'r') as yaml_fobj:
        yaml_content = yaml.load(yaml_fobj)

    return yaml_content


if __name__ == '__main__':
    configuraion = read_from_configuration('config.yaml')
    get_db_connect_string(configuraion)
