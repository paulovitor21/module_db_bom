from sqlalchemy.orm import Session
from scripts.models import BomRecord
import logging

def save_to_db(df_bom, db: Session, plan_date):
    """
    Save records to the database using ORM.
    Processes all records from a file, but only inserts records
    if the file date is not already present in the database.

    Args:
        df_bom (DataFrame): DataFrame with the data to be inserted.
        db (Session): Database session.
        plan_date (str): Date of the file to be processed.

    Returns:
        bool: True if new records were inserted, False otherwise.
    """
    # Convert all columns to string
    df_bom = df_bom.astype(str)

    # Replace null values with empty strings
    df_bom = df_bom.fillna('')
    # Check if records already exist in the database for the same file date
    existing_records = db.query(BomRecord).filter_by(plan_date=plan_date).first()
    if existing_records:
        logging.info(f"[Ignored] Records for the date {plan_date} already exist in the database. No records were inserted.")
        return False  # No data was inserted

    # Insert records, as no records exist for the file date
    inserted_count = 0
    for _, row in df_bom.iterrows():
        record = BomRecord(
            plan_date=plan_date,  # Plan date value (passed as argument)
            org=row['org.'],  # Ensure 'org.' is the correct name in the DataFrame
            top_item=row['top item'],
            top_desc=row['top desc'],  # Added
            level=row['level'],  # Added
            parent_item=row['parent item'],  # Added
            parent_uit=row['parent uit'],  # Added
            child_item=row['child item'],
            child_desc=row['child desc'],
            child_spec=row['child spec'],  # Added
            child_uit=row['child uit'],
            child_rev=row['child rev'],  # Added
            supply_type=row['supply type'],  # Added
            child_c_osp=row['child c-osp'],  # Added
            make_buy=row['make/buy'],  # Added
            desig_no=row['desig no.'],  # Added
            eco_no=row['eco no.'],  # Added
            quantity=row['quantity'],  # Added
            extended_quantity=row['extended quantity'],  # Added
            start_date=row['start date'],  # Added
            end_date=row['end date'],  # Added
            comments=row['comments'],  # Added
            subs_item_1=row['subs item 1'],
            subs_item_2=row['subs item 2'],  # Added
            subs_item_3=row['subs item 3'],  # Added
            subs_item_4=row['subs item 4'],  # Added
            subs_item_5=row['subs item 5'],  # Added
            subs_item_6=row['subs item 6'],  # Added
            subs_item_7=row['subs item 7'],  # Added
            subs_item_8=row['subs item 8'],  # Added
            subs_item_9=row['subs item 9'],  # Added
            qpa=row['qpa'],
            class_code=row['class code'],  # Added
            class_name=row['class name'],  # Added
            uom=row['uom'],  # Added
            svc_code=row['svc code'],  # Added
            svc_location=row['svc location'],  # Added
            code=row['code'],  # Added
            code2=row['code2'],  # Added
            local=row['local'],
            assy=row['assy'],
            supplier=row['supplier'],
            line=row['line'],  # Added
            planner=row['planner'],
            purchaser=row['purchaser'],
            supplier_name=row['supplier name'],
            model_mrp=row['model mrp'],
        )
        db.add(record)
        inserted_count += 1

    # Commit to the database
    db.commit()

    # Display success message only if records were inserted
    logging.info(f"[Inserted] Total records inserted for the date {plan_date}: {inserted_count}.")
    logging.info("Data saved successfully!")
    return True