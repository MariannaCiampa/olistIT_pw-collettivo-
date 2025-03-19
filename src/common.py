import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import psycopg
#common è un file di test. Verifichiamo che funzioni tutto e poi implementiamo

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


pd.set_option("display.max.columns", None)
pd.set_option("display.width", None)
#pd.set_option("display.max.rows", None)



def read_file():
    isValid = False
    df = pd.DataFrame()
    while not isValid:
        path = input("Inserire il path del file:\n").strip()
        try:
            path_list = path.split(".")
            if path_list[-1] == "csv" or path_list[-1] == "txt":
                df = pd.read_csv(path)
            elif path_list[-1] == "xlsx" or path_list[-1] == "xls":
                df = pd.read_excel(path)
            else:
                df = pd.read_json(path)

        except FileNotFoundError as ex:
            print(ex)
        except OSError as ex:
            print(ex)
        else:
            print("Path inserito correttamente")
            isValid = True

    else:
        return df



'''def caricamento_barra(df,cur,sql):
    print(f"Caricamento in corso... \n{str(len(df))} righe da inserire.")
    print("┌──────────────────────────────────────────────────┐")
    print("│",end="")
    perc_int = 2
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print("█",end="")
            #print(perc,end="")
            perc_int += 2
        cur.execute(sql, row.to_list())
    print("│ 100% Completato!")
    print("└──────────────────────────────────────────────────┘")
'''


def caricamento_barra(df,cur,sql):
    print(f"Caricamento in corso... \n{str(len(df))} righe da inserire.")
    Tmax = 50
    if len(df)/2 < 50:
        Tmax = len(df)
    print("┌" + "─" * Tmax + "┐")
    print("│",end="")
    perc_int = 2
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print("\r│" + "█" * (perc_int//2) + str(int(perc)) + "%",end="")
            #print(perc,end="")
            perc_int += 2
        cur.execute(sql, row.to_list())
    print("\r│" + "█" * Tmax + "│ 100% Completato!")
    print("└" + "─" * Tmax + "┘")




def format_cap(df):
    # Converte in stringa e riempie con zeri fino a 5 cifre
    #if "cap" in df.columns:
    #df["cap"] = df["cap"].fillna(0).astype(int).astype(str).str.zfill(5)
    df["cap"] = df["cap"].apply(lambda cap: str(int(cap)).zfill(5) if cap == cap else cap)
    return df



# serie = 1 colonna
# dataframe = più colonne
def format_string(df, cols):
    #print(df.info())
    #print(df.select_dtypes("object"))
    #print(df[cols])
    for col in cols:
        df[col] = df[col].str.strip()
        df[col] = df[col].str.replace("[0-9]","", regex=True)
        #se avessi scritto [^0-9] avrebbe lasciato SOLO i caratteri numerici
        df[col] = df[col].str.replace("[\\[\\]$&+:;=?@#|<>.^*(/_)%!]", "", regex=True)
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)

    return df




def drop_duplicates(df):
    print("Valori duplicati rimossi:", df.duplicated().sum(), "\n")
    df.drop_duplicates(inplace=True)
    return df



#serve per non dare un parametro: così facendo considera la prima colonna
def check_nulls(df,subset=""):
    print(f"Valori nulli per colonna : {df.isnull().sum()}")
    subset = df.columns.tolist()[0] if not subset else subset
    df.dropna(axis=0, subset=subset, inplace= True, ignore_index=True)
    #df = fill_null(df)
    return df



#inplace sovrascrive i cambiamenti
def fill_null(df):
    # gestione del tipo di valore da cambiare
    df.fillna(value= "nd", axis=0, inplace=True)
    return df


def format_region():
    print("Formattazione dei nomi delle regioni per PowerBI")
    nome_tabella = input("Inserisci il nome della tabella da modificare:").strip().lower()

    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = f"""
            UPDATE {nome_tabella} 
            SET region = 'Emilia-Romagna'
            WHERE region = 'Emilia Romagna'
            RETURNING *;
            """

            cur.execute(sql)

            print("Record con region aggiornata (per PowerBI)")
            for record in cur:
                print(record)


            sql = f"""
            UPDATE {nome_tabella} 
            SET region = 'Valle d''Aosta'
            WHERE region = 'Valled''Aosta'
            RETURNING *;
            """

            cur.execute(sql)

            print("Record con region aggiornata (per PowerBI)")
            for record in cur:
                print(record)

            sql = f"""
            UPDATE {nome_tabella} 
            SET region = 'Trentino-AltoAdige'
            WHERE region = 'Trentino Alto Adige'
            RETURNING *;
            """

            cur.execute(sql)

            print("Record con region aggiornata (per PowerBI)")
            for record in cur:
                print(record)





    #Salvataggio
def save_processed(df):
    #print(datetime.datetime.now())
    name = input("Qual è il nome del file?").strip().lower()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = name + "_processed" + "_datetime " + timestamp + ".csv"
    print(file_name)
    if __name__ == "__main__":
        directory_name = "../data/processed/"
    else:
        directory_name = "data/processed/"
    df.to_csv(directory_name + file_name, index=False)



if __name__ == "__main__":
    #print(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    #df = read_file()
    #df = format_string(df,["region", "city"])
    #print("Visualizzo i dati PRIMA di FORMAT CAP")
    #print(df)
    #df = format_cap(df)
    #print("Visualizzo i dati DOPO il FORMAT CAP")
    #print(df)
    #check_nulls(df)
    #save_processed(df)
    format_region()




'''def caricamento_percentuale(df, cur, sql):
    # eseguo la query per caricare i dati (il risultato del caricamento è in percentuale)
    print(f"Caricamento in corso... {str(len(df))} righe da inserire.")
    perc_int = 0
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print(f"{round(perc)}% Completato")
            perc_int += 5
        cur.execute(sql, row.to_list())'''



#subset è una lista
#se io mettessi subset=0  o subset=df.iloc[:, 0] come parametro considererebbe la 1 colonna
'''def check_null(df, subset):
    #print("Valori nulli per colonna:\n", df.isnull().sum(), "\n")
    print(f"Valori nulli per la colonna customer_id: \n {df.isnull().sum()}")
    #se metto ANY (how) mi cancella qualsiasi riga abbia QUALCHE valore nullo, ALL li vuole tutti nulli (forse ho capito male...)
    #se volessimo droppare le colonne ->  axis=1
    #how controlla le colonne elencate in subset(in questo caso ne abbiamo una sola, ma potremmo fare un elenco)
    #any cancella anche se solo una colonna ha valori nulli (..)
    #come parametro possiamo sia passare il DATAFRAME che un tot di colonna, che una sola colonna
    df.dropna(axis=0, how="all", subset=subset, inplace= True, ignore_index=True)
    print(df)
    return df'''