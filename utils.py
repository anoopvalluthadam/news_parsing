import yaml


def get_db_connect_string(configuraion, username='admin',
                          password='iamadmin', name='mongodb'):
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
    print(connect_string)
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
