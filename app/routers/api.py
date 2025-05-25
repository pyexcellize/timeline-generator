from fastapi import APIRouter, HTTPException
from pandas import DataFrame
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from app.services.excel import Excel

router = APIRouter()


@router.get("/rows/{row_pk}/timeline")
async def get_row_timeline(row_pk: str):
    """Get timeline for a specific row using real data from Excel files"""

    # Validate row_pk
    if not row_pk:
        raise HTTPException(status_code=400, detail="Row ID is required")

    try:
        # Get data from Excel service
        rows = Excel.get_rows_by_row_pk(row_pk)

        grouped_rows = {}
        for row in rows:
            date_key = row.get("00_parsed_date")
            file_name = row.get("00_file_name")
            sheet_name = row.get("00_sheet_name")

            if date_key not in grouped_rows:
                grouped_rows[date_key] = {}
            if file_name not in grouped_rows[date_key]:
                grouped_rows[date_key][file_name] = {}
            if sheet_name not in grouped_rows[date_key][file_name]:
                grouped_rows[date_key][file_name][sheet_name] = []

            grouped_rows[date_key][file_name][sheet_name].append(row)

        return {
            "matches": grouped_rows
        }

    except Exception as e:
        # Log the error in production
        print(f"Error fetching timeline for row {row_pk}: {str(e)}")
        raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/rows/auto_complete")
async def get_all_rowes():
    """Get list of all available rowes"""
    try:
        return [
            {"row_pk": "ROW-001", "status": "Active", "created": "2024-04-01"},
            {"row_pk": "ROW-002", "status": "Testing", "created": "2024-04-15"},
            {"row_pk": "ROW-003", "status": "Planning", "created": "2024-05-01"}
        ]
    except Exception as e:
        print(f"Error fetching rowes: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
