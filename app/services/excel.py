import os
import pandas as pd
from typing import List, Dict, Any, Union

class Excel:
    DATA_DIRECTORY = "data/"  # Root data directory for Excel files
    
    @staticmethod
    def get_excel_file_path(file_name: str) -> str:
        """
        Returns the full path to the Excel file.
        """
        return f"app/excel/{file_name}"

    @staticmethod
    def get_excel_file_name(file_name: str) -> str:
        """
        Returns the name of the Excel file.
        """
        return file_name
        
    @staticmethod
    def find_all_excel_files() -> List[str]:
        """
        Returns a list of all Excel files in the data directory.
        """
        excel_files = []
        # Check if the data directory exists
        if not os.path.exists(Excel.DATA_DIRECTORY):
            return excel_files
            
        # Walk through the directory and find all Excel files
        for root, _, files in os.walk(Excel.DATA_DIRECTORY):
            for file in files:
                if file.endswith(('.xlsx', '.xls')):
                    excel_files.append(os.path.join(root, file))
                    
        return excel_files
    
    @staticmethod
    def get_rows_by_row_id(row_id: str) -> List[Dict[str, Any]]:
        """
        Searches all Excel files in the data directory for rows with the specified row ID.
        
        Args:
            row_id: The row ID to search for in the "PRIMARY_KEY" column.
            
        Returns:
            A list of dictionaries containing the matching rows with file and sheet metadata.
        """
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
                        
                        # Check if the "PRIMARY_KEY" column exists in this sheet
                        if "PRIMARY_KEY" in df.columns:
                            # Filter rows where "PRIMARY_KEY" matches the row_id
                            matching_rows = df[df["PRIMARY_KEY"] == row_id]
                            
                            # If there are matching rows, add them to results
                            if not matching_rows.empty:
                                for _, row in matching_rows.iterrows():
                                    # Convert row to dictionary and add metadata
                                    row_dict = row.to_dict()
                                    result = {
                                        "file_name": file_name,
                                        "sheet_name": sheet_name,
                                        "data": row_dict
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
