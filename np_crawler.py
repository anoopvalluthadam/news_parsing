
import utils
from db import np_mongodb as mdb


if __name__ == '__main__':
    configuraion = utils.read_from_configuration('config.yaml')
    connect_string = utils.get_db_connect_string(configuraion)
    client = mdb.create_connection(connect_string)

    db = client.admin
    print(db)
