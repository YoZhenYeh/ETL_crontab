import toml
from sqlalchemy import *
from sqlalchemy.dialects.mysql import insert
# from getRate import get_sql_config

def get_sql_config(filename="config.toml"):
    with open (filename) as file:
        config_all = toml.load(file)
        config_mysql = config_all["MySQL"]
        mysql_info = f'{config_mysql["driver"]}://{config_mysql["username"]}:{config_mysql["password"]}@{config_mysql["host"]}:{config_mysql["port"]}/{config_mysql["db_name"]}'
    return mysql_info


def insert_update_data(table_name = "table_update_record"):
    try:
        # create metadata
        metadata = MetaData()
        # define table
        table_info = Table(
            table_name, 
            metadata, 
            Column("tableName", String(255), index=True),
            Column("tableUpdateTime", DateTime), 
            Column("modifyTime", DateTime, server_default=func.now(), onupdate=func.now())
            )

        # connect to sql
        engine = create_engine(get_sql_config())
        metadata.create_all(engine) # Implement

        query_stmt = "SELECT TABLE_NAME, UPDATE_TIME FROM information_schema.TABLES;"

        with engine.connect() as conn:
            result = conn.execute(text(query_stmt)) # Use sqlalchemy text to wrap stmt, otherwise it will be treated as str
            
            for row in result:
                insert_data = {
                    "tableName" : row[0],
                    "tableUpdateTime" : row[1], 
                    "modifyTime" : func.now()
                    }
                
                insert_stmt = insert(table_info).values(insert_data).on_duplicate_key_update(
                    tableUpdateTime = row[1], 
                    modifyTime = func.now()
                    ) # insert and update
                
                conn.execute(insert_stmt)
            conn.commit()
        print(f"[Table:mysql_info.py] Insert and update '{table_name}' successful.")

    except Exception as e:
        print("[Error:mysql_info.py]", e)

if __name__ == "__main__":
    insert_update_data()
