#%%
import requests
import json
import toml
from sqlalchemy import *
from sqlalchemy.dialects.mysql import insert 
from datetime import datetime
from pytz import timezone

# get config info
def get_sql_config(filename="config.toml"):
    with open (filename) as file:
        config_all = toml.load(file)
        config_mysql = config_all["MySQL"] # get MySQL config
        # {MySQLDriver}://{username}:{password}@{host}/{dbname}
        mysql_info = f'{config_mysql["driver"]}://{config_mysql["username"]}:{config_mysql["password"]}@{config_mysql["host"]}:{config_mysql["port"]}/{config_mysql["db_name"]}' # ?host={config_mysql["host"]}
    return mysql_info

def get_rate(url="https://tw.rter.info/capi.php"):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        print("[Request:mysql_info.py] Rate info request successful.")
    else:
        print(f"[Request:mysql_info.py] Rate info request fail, status code: {response.status_code}")
    return json_data

def insert_update_sql(table_name="RateInfo", data=None)->dict:
    try:
        # create metadata 
        metadata = MetaData()
        # define table
        table_info = Table(
            table_name,
            metadata,
            Column("currency1", String(20), index=True),
            Column("currency2", String(20), index=True),
            Column("exRate", Float),
            Column("utcTime", DateTime),
            Index("composite_index", "currency2", "currency1", unique=True) # define composite index
            )
        
        # connect to sql
        engine = create_engine(get_sql_config()) 
        metadata.create_all(engine) # Implement
        
        # insert and update data to sql
        key_ls = [k for k in data.keys()]
        with engine.connect() as conn:
            for key_ in key_ls:
                # transfer utc to taipei zone
                utc_time = datetime.strptime(data[key_]["UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone("UTC"))
                taipei_zone = utc_time.astimezone(timezone("Asia/Taipei"))

                # check coherer
                if key_[:3] == "USD":
                    curr2 = key_[3:]
                else:
                    curr2 = key_

                insert_data = {
                    "currency1" : "USD",
                    "currency2" : curr2,
                    "exRate" : data[key_]["Exrate"],
                    "utcTime" : taipei_zone
                    }

                insert_stmt = insert(table_info).values(insert_data).on_duplicate_key_update(
                    exRate = data[key_]["Exrate"],
                    utcTime = taipei_zone
                    ) # insert and update

                conn.execute(insert_stmt)
            conn.commit()
            print(f"[Table:mysql_info.py] Insert and update '{table_name}' successful.")
    
    except Exception as e:
        print("[Error:getRate.py]", e)

if __name__ == "__main__":
    insert_update_sql(table_name="RateInfo", data=get_rate())