import os
import pandas as pd
import logging

def convert_xlsb_to_xlsx(xlsb_file, output_dir):
    """
    Converte um arquivo .xlsb para .xlsx e salva em uma pasta especificada.

    :param xlsb_file: Caminho para o arquivo .xlsb de entrada.
    :param output_dir: Caminho da pasta onde o arquivo convertido será salvo.
    :return: Caminho completo do arquivo .xlsx convertido.
    """
    try:
        # Garantir que o diretório de saída exista
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Nome do arquivo convertido
        xlsx_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xlsb_file))[0] + ".xlsx")

        # Ler o arquivo .xlsb usando pandas e pyxlsb
        data = pd.read_excel(xlsb_file, engine='pyxlsb')

        # Salvar o DataFrame como .xlsx
        data.to_excel(xlsx_file, index=False)
        logging.info(f"Arquivo convertido com sucesso: {xlsx_file}")
        return xlsx_file
    except Exception as e:
        logging.error(f"Erro ao converter arquivo: {e}")
        raise