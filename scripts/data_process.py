# process_data.py
import os
import logging
import pandas as pd
import win32com.client
from scripts.db_connection import SessionLocal, engine
from scripts.models import Base
from scripts.data_transformation import clean_data
from scripts.db_operations import save_to_db
from scripts.convert_xlsb_xlsx import convert_xlsb_to_xlsx

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_date(xlsb_file):
    excel = win32com.client.Dispatch("Excel.Application")
    wb = excel.Workbooks.Open(xlsb_file, ReadOnly=True)
    data_salvamento = wb.BuiltinDocumentProperties("Last Save Time").Value
    wb.Close()
    excel.Quit()
    return data_salvamento.strftime('%Y-%m-%d %H:%M:%S')
    
def process_file(xlsb_file, converted_dir="converted_files"):
    # Cria as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)

    # Criar sessão
    db = SessionLocal()

    xlsx_file = None

    try:
        # Converte o arquivo .xlsb para .xlsx
        xlsx_file = convert_xlsb_to_xlsx(xlsb_file, converted_dir)

        # Carregar os dados
        with pd.ExcelFile(xlsx_file) as xls:
            df_bom = xls.parse(dtype=str)

        # Extrair data do arquivo
        plan_date = get_file_date(xlsb_file)
        logging.info(f"Data do ARQUIVO -> {plan_date}")

        # Limpar os dados
        df_bom = clean_data(df_bom)

        # Salvar no banco
        save_to_db(df_bom, db, plan_date)
    except Exception as e:
        logging.error(f"Ocorreu um erro na execução do processo: {e}")
        logging.exception("Detalhes do erro: ")
    finally:
        # Deletar o arquivo convertido para evitar acúmulo
        if xlsx_file and os.path.exists(xlsx_file):
            try:
                #os.remove(xlsx_file)
                logging.info(f"Arquivo temporário removido: {xlsx_file}")
            except Exception as e:
                logging.error(f"Não foi possível excluir o arquivo: {e}")

        # Fechar conexão com o banco de dados
        db.close()