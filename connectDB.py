import psycopg2
from configparser import ConfigParser

def insertValues(cur, values):
    insert_script = """INSERT INTO camperdata
    (id, ispublished, path, price, year, brand, model, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur.execute(insert_script, values)
    
def createTable(cur):
    query = """ CREATE TABLE IF NOT EXISTS camperdata(
    id BIGSERIAL not NULL PRIMARY KEY,
    ispublished int not NULL,
    path varchar(100) not NULL,
    year int not NULL,
    price int not NULL,
    brand varchar(20) not NULL,
    model varchar(20) not NULL,
    description varchar(65535) not NULL);
    """ 
    cur.execute(query)

def connection():
    configObj = ConfigParser();
    configObj.read("configDB.ini");
    args = configObj["CREDENTIALS"];
    
    conn = psycopg2.connect(host = args["hostname"], dbname = args["database"], user = args["username"],
                                    password = args["pwd"], port = args["port_id"])
    return conn
        #createTable(cur)        
        #insertValues(cur)
        
        #conn.commit()
        

if __name__ == "main":
    pass
        
        
    ##startup = Program(hostname=args["hostname"], database='', username='', pwd='', port_id='')
