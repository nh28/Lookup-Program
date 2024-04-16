import oracledb
import pandas as pd
import logging

class ARKEON:
    def __init__(self):
        self.driver = 'oracle'
        self.ARKEON_host = 'ARC-CLUSTER.CMC.EC.GC.CA'
        self.ARKEON_port = '1521'
        self.ARKEON_service = 'archive.cmc.ec.gc.ca'
        self.connection = None
        
    def connect(self, usern, passw):
        """
        Connect to database

        Parameters:
        usern: Username that the user entered
        passw: Password that the user entered

        Returns:
        src_conn: The connection to the database
        """
        try:
            src_conn = oracledb.connect(
                user = usern,
                password = passw,
                host = self.ARKEON_host,
                port = self.ARKEON_port,
                service_name = self.ARKEON_service
            )
            self.connection = src_conn
            return True
        except oracledb.DatabaseError as err:
            error, = err.args
            logging.error('Unable to establish connection, due to: %s', error.message)
            return False
        
    def get_dataframe(self):
        """
        Turn the SQL query into a DataFrame

        Parameters:
        None

        Returns:
        pd.DataFrame(rows, columns = column_headers): A DataFrame of the normals query
        """
        
        query =\
        '''
        SELECT
            *
        FROM
            NORMALS_WMO_9120.normals_data       
        '''

        cursor = self.connection.cursor()

        if cursor is not None:
            logging.info('Executing query...')
            logging.info(query)
            try:
                cursor.execute(query)
            except Exception as err:
                msg = 'Unable to execute query, due to: %s' % str(err)
                logging.error(msg)
            logging.info('Query execution complete.')
        else:
            logging.error('Unable to execute query, due to: no cursor.')
        
        column_headers = [desc[0] for desc in cursor.description]
        rows = []
        for row in cursor:
            rows.append(row)
            
        cursor.close()
        logging.info('Cursor closed.')

        return pd.DataFrame(rows, columns = column_headers)
