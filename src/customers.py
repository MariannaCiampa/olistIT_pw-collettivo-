# 3 metodi ETL per customers
#from src.common import read_file -> con questa scrittura basta richiamare semplicemente il metodo "read_file()"
#import src.common
import src.common as common
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


def extract():
    print("questo è il metodo EXTRACT")
    #src.common.read_file()
    df = common.read_file()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM dei customers\n")
    print(df)
    df = common.drop_duplicates(df)
    df = common.check_null(df)
    df = common.format_cap(df)
    common.save_processed(df)
    print(df)
    return df

def load(df):
    print("questo è il metodo LOAD dei customers\n")
    #print(df)
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE customers (
                pk_customer VARCHAR PRIMARY KEY,
                region VARCHAR,
                city VARCHAR,
                cap VARCHAR
                );
                """

            try:
                cur.execute(sql)  # Inserimento report nel database
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Vuoi cancellare la tabella? si/no").strip().lower()
                if domanda == "si":
                    # se risponde si: cancellare tabella
                    sql_delete = """
                DROP TABLE customers;
                """
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Ricreo la tabella customers")
                    cur.execute(sql)


            sql = """
                    INSERT INTO customers
                    (pk_customer, region, city, cap)
                    VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
                    """

            common.caricamento_barra(df, cur, sql)
            conn.commit()



def main():
    print("questo è il metodo MAIN dei customers")
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    main()