import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Union

from pandas import DataFrame

from app.config.config import Config


class Excel:
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
    def get_rows_by_row_pk(row_pk: str) -> Any:
        output = []

        for file_path in Excel.find_all_excel_files():
            try:
                # Get the Excel file with all sheets
                excel_file = pd.ExcelFile(file_path)

                # Extract the file name from the path
                file_name = os.path.basename(file_path)

                # Process each sheet in the Excel file
                for sheet_name in excel_file.sheet_names:
                    try:
                        # Read the sheet into a DataFrame
                        sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name)

                        # Find which primary key is in the dataframe
                        found_primary_key = None
                        for pk in Config.PRIMARY_KEYS:
                            if pk in sheet_df.columns:
                                found_primary_key = pk
                                break

                        found_date_key = None
                        for date_key in Config.DATE_COLUMNS:
                            if date_key in sheet_df.columns:
                                found_date_key = date_key
                                break

                        # If a primary key is found, search for the row_pk
                        if found_primary_key:
                            matches_in_sheet = []
                            matches_in_sheet_df = sheet_df[sheet_df[found_primary_key] == row_pk]

                            # If there are matching rows, add them to results
                            if not matches_in_sheet_df.empty:
                                for _, row in matches_in_sheet_df.iterrows():
                                    matches_in_sheet.append({
                                        'metadata': {
                                            'parsed_date': 'None'
                                        },
                                        'row': row.astype(str).to_dict(),
                                    })

                                output.append({
                                    'matches': matches_in_sheet,
                                    'file_name': file_name,
                                    'sheet_name': sheet_name,
                                })

                    except Exception as e:
                        # Log error but continue processing other sheets
                        print(f"Error processing sheet {sheet_name} in file {file_path}: {str(e)}")
                        continue

            except Exception as e:
                # Log error but continue processing other files
                print(f"Error processing file {file_path}: {str(e)}")
                continue

        return output
