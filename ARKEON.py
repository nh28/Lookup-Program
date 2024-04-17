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
        
    def get_dataframe(self, column_name, from_section):
        """
        Turn the SQL query into a DataFrame

        Parameters:
        None

        Returns:
        pd.DataFrame(rows, columns = column_headers): A DataFrame of the normals query
        """
        
        query = f'''
        SELECT
            {column_name}
        FROM
            {from_section}     
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
            
        rows = [row[0] for row in cursor.fetchall()]
        cursor.close()
        logging.info('Cursor closed.')

        return pd.DataFrame({column_name: rows})
    
    def get_all_stations(self):
        all_stations = []
        stations_1981 = self.get_dataframe('eng_stn_name', 'ECODAT.STATION_INFORMATION')
        # ADD THE OTHER YEARS
        # Question: will stations with same id potentially have different names?
        for row in stations_1981.values:
            for value in row:
                if value != None and value not in all_stations:
                    all_stations.append(value)
        #put in alphabetical order
        return all_stations
    
    def get_all_elements(self):
        all_elements = []
        elements_1971 = self.get_dataframe('e_normal_element_name', 'NORMALS.valid_normals_elements')
        elements_1981 = self.get_dataframe('e_normal_element_name', 'NORMALS_1981.valid_normals_elements')
        # add 1991

        for row in elements_1971.values:
            for value in row:
                if value != None and value not in all_elements:
                    all_elements.append(value)
        
        for row in elements_1981.values:
            for value in row:
                if value != None and value not in all_elements:
                    all_elements.append(value)
        
        return all_elements
