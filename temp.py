import os import logging from botcity.core import DesktopBot from botcity.web import WebBot, By from botcity.maestro import * from login_lge import login from utils.driver_manager import choosing_browser from module_db_bom.data_process import process_file from modules.check_email import download_email_attachments_by_title

Disable errors if we are not connected

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main(): webbot = WebBot()

# Connect to BotCity Maestro
maestro = BotMaestroSDK.from_sys_args("https://developers.botcity.dev/", "lg", "LG_AC8AFU4RY3KU8GJ6BRM7")
execution = maestro.get_execution()

print(f"Task ID is: {execution.task_id}")
print(f"Task Parameters are: {execution.parameters}")

# Configure the web browser
webbot.browser, webbot.driver_path = choosing_browser('chrome')

# Retrieve credentials from Maestro
username_credential = maestro.get_credential(label="dx_robot_login", key="login")
password_credential = maestro.get_credential(label="dx_robot_login", key="password")
employee_number = maestro.get_credential(label="dx_robot_login", key="employee_number")
personal_id_code = maestro.get_credential(label="dx_robot_login", key="personal_id_code")

# Perform login
login.login(webbot, username_credential, password_credential, employee_number, personal_id_code)
webbot.wait(5000)

# Search for email attachments
search_queries = ["BOM Master"]
download_email_attachments_by_title(webbot, employee_number, search_queries)
webbot.wait(5000)

# Process BOM database
try:
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arquivos_destino")
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".xlsb")]
    if files:
        xlsb_file = max(files, key=os.path.getctime)  # Get the most recently modified file
    else:
        logging.info("No .xlsb files found in the destination folder.")
        return

    logging.info(f"Processing file: {xlsb_file}")
    process_file(xlsb_file)

except Exception as e:
    logging.error(f"An error occurred during process execution: {e}")
    logging.exception("Error details: ")

# Finalize the task in Maestro
maestro.finish_task(
    task_id=execution.task_id,
    status=AutomationTaskFinishStatus.SUCCESS,
    message="Task successfully completed."
)

def not_found(label): print(f"Element not found: {label}")

try: maestro = BotMaestroSDK.from_sys_args() execution = maestro.get_execution() main() except Exception as e: if maestro and execution: maestro.error( task_id=execution.task_id, exception=e ) maestro.finish_task( task_id=execution.task_id, status=AutomationTaskFinishStatus.FAILED, message=f"An exception occurred: {e}" ) finally: os.system("taskkill /f /im chromedriver.exe") os.system("taskkill /f /im chrome.exe")

