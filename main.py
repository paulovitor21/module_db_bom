import os
import logging
from scripts.data_process import process_file
from typing import NoReturn

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main() -> NoReturn:
    """
    Main function to process the .xlsb file.
    """
    try:
        # Path to the source .xlsb file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xlsb_file = os.path.join(script_dir, "1213_Bom_Master.xlsb")
        # Process the file
        process_file(xlsb_file)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        logging.exception("Error details: ")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        logging.exception("Error details: ")
    except Exception as e:
        logging.error(f"An error occurred during the process execution: {e}")
        logging.exception("Error details: ")

if __name__ == "__main__":
    main()