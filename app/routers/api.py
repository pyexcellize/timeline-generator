from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from app.services.excel import Excel

router = APIRouter()


@router.get("/rows/{row_id}/timeline")
async def get_row_timeline(row_id: str):
    """Get timeline for a specific row using real data from Excel files"""

    # Validate row_id
    if not row_id:
        raise HTTPException(status_code=400, detail="Row ID is required")

    try:
        # Get data from Excel service
        row_rows = Excel.get_rows_by_row_id(row_id)
        
        # Return early if no data found
        if not row_rows:
            return {
                "row_id": row_id,
                "events": []
            }
        
        # Process the data into timeline events
        events = []
        for row in row_rows:
            # Extract data
            file_name = row["file_name"]
            sheet_name = row["sheet_name"]
            row_data = row["data"]
            
            # Try to get date from "DATE_COLUMN_0" or "DATE_COLUMN_1" columns
            event_date = None
            if "DATE_COLUMN_0" in row_data:
                event_date = str(row_data["DATE_COLUMN_0"])
            elif "DATE_COLUMN_1" in row_data:
                event_date = str(row_data["DATE_COLUMN_1"])
                
            # Format the date if it's numeric (YYYYMMDD format)
            if event_date and event_date.isdigit() and len(event_date) == 8:
                year = event_date[:4]
                month = event_date[4:6]
                day = event_date[6:]
                event_date = f"{year}-{month}-{day}"
            
            # Create description from available data
            description = f"Data from {file_name} ({sheet_name})"
            
            # Create table data from row values (excluding row ID and date columns)
            table_data = []
            for key, value in row_data.items():
                if key != "PRIMARY_KEY" and key not in ["DATE_COLUMN_0", "DATE_COLUMN_1"]:
                    table_data.append(f"{key}: {value}")
            
            # Create event object
            event = {
                "date": event_date or "Unknown date",
                "row_id": row_id,
                "description": description,
                "source": {
                    "file": file_name,
                    "sheet": sheet_name
                },
                "table_data": table_data
            }
            
            events.append(event)
        
        # Sort events by date if available (most recent first)
        events.sort(
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d") 
            if x["date"] != "Unknown date" and len(x["date"]) == 10 
            else datetime.min,
            reverse=True
        )
        
        return {
            "row_id": row_id,
            "events": events
        }

    except Exception as e:
        # Log the error in production
        print(f"Error fetching timeline for row {row_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/rows/rowes")
async def get_all_rowes():
    """Get list of all available rowes"""
    try:
        return [
            {"row_id": "ROW-001", "status": "Active", "created": "2024-04-01"},
            {"row_id": "ROW-002", "status": "Testing", "created": "2024-04-15"},
            {"row_id": "ROW-003", "status": "Planning", "created": "2024-05-01"}
        ]
    except Exception as e:
        print(f"Error fetching rowes: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/row/{row_id}/data", response_model=Dict)
async def get_row_data(row_id: str):
    """
    Fetch all rows with a specific row ID from all Excel files in the data directory.
    
    Args:
        row_id: The row ID to search for in the "PRIMARY_KEY" column
        
    Returns:
        All matching rows with file and sheet metadata
    """
    if not row_id:
        raise HTTPException(status_code=400, detail="Row ID is required")
        
    try:
        # Get data from Excel service
        results = Excel.get_rows_by_row_id(row_id)
        
        if not results:
            return {
                "row_id": row_id,
                "count": 0,
                "data": []
            }
            
        return {
            "row_id": row_id,
            "count": len(results),
            "data": results
        }
        
    except Exception as e:
        # Log the error
        print(f"Error fetching row data for {row_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
