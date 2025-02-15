from sqlalchemy.orm import Session
from scripts.models import BomRecord
import logging

def save_to_db(df_bom, db: Session, plan_date):
    """
    Salva os registros no banco de dados usando ORM.
    Processa todos os registros de um arquivo, mas apenas insere os registros
    caso a data do arquivo não esteja presente no banco.

    Args:
        df_bom (DataFrame): DataFrame com os dados a serem inseridos.
        db (Session): Sessão do banco de dados.
        file_date (str): Data do arquivo a ser processado.

    Returns:
        bool: True se novos registros foram inseridos, False caso contrário.
    """
    # Converter todas as colunas para string
    df_bom = df_bom.astype(str)

        # Substituir valores nulos por strings vazias
    df_bom = df_bom.fillna('')
    # Verificar se já existem registros no banco para a mesma data do arquivo
    existing_records = db.query(BomRecord).filter_by(plan_date=plan_date).first()
    if existing_records:
        logging.info(f"[Ignorado] Registros para a data {plan_date} já existem no banco. Nenhum registro foi inserido.")
        return False  # Nenhum dado foi inserido

    # Inserir os registros, pois não existem registros para a data do arquivo
    inserted_count = 0
    for _, row in df_bom.iterrows():
        record = BomRecord(
            plan_date=plan_date,  # Valor da data do plano (passado como argumento)
            org=row['org.'],  # Certifique-se de que 'org.' é o nome correto no DataFrame
            top_item=row['top item'],
            top_desc=row['top desc'],  # Adicionado
            level=row['level'],  # Adicionado
            parent_item=row['parent item'],  # Adicionado
            parent_uit=row['parent uit'],  # Adicionado
            child_item=row['child item'],
            child_desc=row['child desc'],
            child_spec=row['child spec'],  # Adicionado
            child_uit=row['child uit'],
            child_rev=row['child rev'],  # Adicionado
            supply_type=row['supply type'],  # Adicionado
            child_c_osp=row['child c-osp'],  # Adicionado
            make_buy=row['make/buy'],  # Adicionado
            desig_no=row['desig no.'],  # Adicionado
            eco_no=row['eco no.'],  # Adicionado
            quantity=row['quantity'],  # Adicionado
            extended_quantity=row['extended quantity'],  # Adicionado
            start_date=row['start date'],  # Adicionado
            end_date=row['end date'],  # Adicionado
            comments=row['comments'],  # Adicionado
            subs_item_1=row['subs item 1'],
            subs_item_2=row['subs item 2'],  # Adicionado
            subs_item_3=row['subs item 3'],  # Adicionado
            subs_item_4=row['subs item 4'],  # Adicionado
            subs_item_5=row['subs item 5'],  # Adicionado
            subs_item_6=row['subs item 6'],  # Adicionado
            subs_item_7=row['subs item 7'],  # Adicionado
            subs_item_8=row['subs item 8'],  # Adicionado
            subs_item_9=row['subs item 9'],  # Adicionado
            qpa=row['qpa'],
            class_code=row['class code'],  # Adicionado
            class_name=row['class name'],  # Adicionado
            uom=row['uom'],  # Adicionado
            svc_code=row['svc code'],  # Adicionado
            svc_location=row['svc location'],  # Adicionado
            code=row['code'],  # Adicionado
            code2=row['code2'],  # Adicionado
            local=row['local'],
            assy=row['assy'],
            supplier=row['supplier'],
            line=row['line'],  # Adicionado
            planner=row['planner'],
            purchaser=row['purchaser'],
            supplier_name=row['supplier name'],
            model_mrp=row['model mrp'],
        )
        db.add(record)
        inserted_count += 1

    # Commit no banco
    db.commit()

    # Exibir mensagem de sucesso apenas se registros forem inseridos
    logging.info(f"[Inserido] Total de registros inseridos para a data {plan_date}: {inserted_count}.")
    logging.info("Dados salvos com sucesso!")
    return True