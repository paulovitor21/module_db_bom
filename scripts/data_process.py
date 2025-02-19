import os
import logging
import pandas as pd
import win32com.client
from scripts.db_connection import SessionLocal, engine
from scripts.models import Base
from scripts.data_transformation import clean_data
from scripts.db_operations import save_to_db
from scripts.convert_xlsb_xlsx import convert_xlsb_to_xlsx

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_date(xlsb_file):
    excel = win32com.client.Dispatch("Excel.Application")
    wb = excel.Workbooks.Open(xlsb_file, ReadOnly=True)
    data_salvamento = wb.BuiltinDocumentProperties("Last Save Time").Value
    wb.Close()
    excel.Quit()
    return data_salvamento.strftime('%Y-%m-%d %H:%M:%S')
    
def process_file(xlsb_file, converted_dir="converted_files"):
    # Create tables in the database
    Base.metadata.create_all(bind=engine)

    # Create session
    db = SessionLocal()

    xlsx_file = None

    try:
        # Convert the .xlsb file to .xlsx
        xlsx_file = convert_xlsb_to_xlsx(xlsb_file, converted_dir)

        # Load the data
        with pd.ExcelFile(xlsx_file) as xls:
            df_bom = xls.parse(dtype=str)

        # Extract file date
        plan_date = get_file_date(xlsb_file)
        
        # Clean the data
        df_bom = clean_data(df_bom)

        # Save to database
        save_to_db(df_bom, db, plan_date)
    except Exception as e:
        logging.error(f"An error occurred during the process execution: {e}")
        logging.exception("Error details: ")
    finally:
        # Delete the converted file to avoid accumulation
        if xlsx_file and os.path.exists(xlsx_file):
            try:
                #os.remove(xlsx_file)
                logging.info(f"Temporary file removed: {xlsx_file}")
            except Exception as e:
                logging.error(f"Could not delete the file: {e}")

        # Close database connection
        db.close()