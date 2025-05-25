import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Union

from pandas import DataFrame

from app.config.config import Config


class Excel:
    # Class-level cache for Excel files
    _excel_cache = {}
    
    @classmethod
    def initialize_cache(cls):
        """Initialize the Excel file cache"""
        cls._excel_cache = {}
        excel_files = cls.find_all_excel_files()
        for file_path in excel_files:
            try:
                # Load the Excel file and store it in cache
                excel_file = pd.ExcelFile(file_path)
                file_name = os.path.basename(file_path)
                
                # Cache both the ExcelFile object and pre-loaded DataFrames for each sheet
                cls._excel_cache[file_path] = {
                    'excel_file': excel_file,
                    'file_name': file_name,
                    'sheets': {}
                }
                
                # Pre-load all sheets
                for sheet_name in excel_file.sheet_names:
                    try:
                        sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
                        cls._excel_cache[file_path]['sheets'][sheet_name] = sheet_df
                    except Exception as e:
                        print(f"Error pre-loading sheet {sheet_name} in file {file_path}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error loading file {file_path} into cache: {str(e)}")
                continue
                
        print(f"Excel cache initialized with {len(cls._excel_cache)} files")
    
    @classmethod
    def refresh_cache(cls):
        """Refresh the Excel file cache"""
        cls.initialize_cache()
    
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

    @classmethod
    def get_rows_by_row_pk(cls, row_pk: str) -> Any:
        output = []
        
        # Initialize cache if empty
        if not cls._excel_cache:
            cls.initialize_cache()

        # Use the cached Excel files instead of opening them again
        for file_path, cached_data in cls._excel_cache.items():
            file_name = cached_data['file_name']
            
            # Process each cached sheet
            for sheet_name, sheet_df in cached_data['sheets'].items():
                try:
                    found_date_key = None
                    for date_key in Config.DATE_COLUMNS:
                        if date_key in sheet_df.columns:
                            found_date_key = date_key
                            break
                    
                    # Check if row_pk exists in index
                    if row_pk in sheet_df.index:
                        matches_in_sheet_df = sheet_df.loc[row_pk]
                        
                        # Handle both Series (single row) and DataFrame (multiple rows)
                        if isinstance(matches_in_sheet_df, pd.Series):
                            row = matches_in_sheet_df
                            # Parse date if date column exists
                            parsed_date = 'None'
                            if found_date_key and found_date_key in row:
                                try:
                                    date_value = str(row[found_date_key])
                                    # Clean the date string (removing any non-numeric characters)
                                    date_value = ''.join(filter(str.isdigit, date_value))

                                    # Parse date in YYYYMMDD format
                                    if len(date_value) == 8:
                                        date_obj = datetime.strptime(date_value, Config.DATE_FORMAT)
                                        parsed_date = date_obj.strftime('%Y-%m-%d')
                                except Exception as date_error:
                                    print(f"Error parsing date {row[found_date_key]}: {str(date_error)}")
                                    parsed_date = 'Error parsing date'

                            output.append({
                                **{
                                    '00_parsed_date': parsed_date,
                                    '00_file_name': file_name,
                                    '00_sheet_name': sheet_name,
                                },
                                **row.astype(str).to_dict(),
                            })
                        else:
                            # Handle DataFrame (multiple rows)
                            for _, row in matches_in_sheet_df.iterrows():
                                # Parse date if date column exists
                                parsed_date = 'None'
                                if found_date_key and found_date_key in row:
                                    try:
                                        date_value = str(row[found_date_key])
                                        # Clean the date string (removing any non-numeric characters)
                                        date_value = ''.join(filter(str.isdigit, date_value))

                                        # Parse date in YYYYMMDD format
                                        if len(date_value) == 8:
                                            date_obj = datetime.strptime(date_value, Config.DATE_FORMAT)
                                            parsed_date = date_obj.strftime('%Y-%m-%d')
                                    except Exception as date_error:
                                        print(f"Error parsing date {row[found_date_key]}: {str(date_error)}")
                                        parsed_date = 'Error parsing date'

                                output.append({
                                    **{
                                        '00_parsed_date': parsed_date,
                                        '00_file_name': file_name,
                                        '00_sheet_name': sheet_name,
                                    },
                                    **row.astype(str).to_dict(),
                                })

                except Exception as e:
                    # Log error but continue processing other sheets
                    print(f"Error processing sheet {sheet_name} in file {file_path}: {str(e)}")
                    continue

        return output

# Initialize the Excel cache when the module is loaded
Excel.initialize_cache()
