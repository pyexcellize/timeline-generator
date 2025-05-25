import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Union

from app.config.config import Config


class Excel:

    @staticmethod
    def get_excel_file_path(file_name: str) -> str:
        return f"app/excel/{file_name}"

    @staticmethod
    def get_excel_file_name(file_name: str) -> str:
        return file_name

    @staticmethod
    def find_all_excel_files() -> List[str]:
        excel_files = []
        # Check if the data directory exists
        if not os.path.exists(Config.DATA_DIRECTORY):
            return excel_files

        # Walk through the directory and find all Excel files
        for root, _, files in os.walk(Config.DATA_DIRECTORY):
            for file in files:
                if file.endswith(('.xlsx', '.xls')):
                    excel_files.append(os.path.join(root, file))

        return excel_files

    @staticmethod
    def get_rows_by_row_id(row_id: str) -> List[Dict[str, Any]]:
        results = []
        excel_files = Excel.find_all_excel_files()

        for file_path in excel_files:
            try:
                # Get the Excel file with all sheets
                excel_file = pd.ExcelFile(file_path)

                # Extract the file name from the path
                file_name = os.path.basename(file_path)

                # Process each sheet in the Excel file
                for sheet_name in excel_file.sheet_names:
                    try:
                        # Read the sheet into a DataFrame
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)

                        # Find which primary key is in the dataframe
                        found_primary_key = None
                        for pk in Config.PRIMARY_KEYS:
                            if pk in df.columns:
                                found_primary_key = pk
                                break

                        # If a primary key is found, search for the row_id
                        if found_primary_key:
                            matching_rows = df[df[found_primary_key] == row_id]

                            # If there are matching rows, add them to results
                            if not matching_rows.empty:
                                for _, row in matching_rows.iterrows():
                                    # Convert row to dictionary
                                    row_dict = row.to_dict()
                                    
                                    # Extract dates from date columns if defined in Config
                                    extracted_dates = {}
                                    if hasattr(Config, 'DATE_COLUMNS') and Config.DATE_COLUMNS:
                                        for date_col in Config.DATE_COLUMNS:
                                            if date_col in row_dict:
                                                date_value = row_dict[date_col]
                                                extracted_dates[date_col] = date_value

                                    # Add metadata and extracted dates to result
                                    result = {
                                        "file_name": file_name,
                                        "sheet_name": sheet_name,
                                        "data": row_dict,
                                        "extracted_dates": extracted_dates
                                    }
                                    results.append(result)
                    except Exception as e:
                        # Log error but continue processing other sheets
                        print(f"Error processing sheet {sheet_name} in file {file_path}: {str(e)}")
                        continue

            except Exception as e:
                # Log error but continue processing other files
                print(f"Error processing file {file_path}: {str(e)}")
                continue

        return results
