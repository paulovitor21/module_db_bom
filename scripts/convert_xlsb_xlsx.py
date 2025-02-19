import os
import pandas as pd
import logging

def convert_xlsb_to_xlsx(xlsb_file, output_dir):
    """
    Converts an .xlsb file to .xlsx and saves it in a specified folder.

    :param xlsb_file: Path to the input .xlsb file.
    :param output_dir: Path to the folder where the converted file will be saved.
    :return: Full path of the converted .xlsx file.
    """
    try:
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Name of the converted file
        xlsx_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xlsb_file))[0] + ".xlsx")

        # Read the .xlsb file using pandas and pyxlsb
        data = pd.read_excel(xlsb_file, engine='pyxlsb')

        # Save the DataFrame as .xlsx
        data.to_excel(xlsx_file, index=False)
        logging.info(f"File successfully converted: {xlsx_file}")
        return xlsx_file
    except Exception as e:
        logging.error(f"Error converting file: {e}")
        raise