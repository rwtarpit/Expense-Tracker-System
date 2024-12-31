from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    notes: str
    
class DateRange(BaseModel):
    start_date: date
    end_date: date



app=FastAPI()
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date : date):
    expense= db_helper.data_by_date(expense_date)
    return expense

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date : date, expenses : List[Expense]):
    db_helper.delete_data(expense_date)
    for expense in expenses:
        db_helper.enterdata( expense_date, expense.amount, expense.category, expense.notes)
    return { "message": "expenses updated successfully"}

@app.post("/analytics/category")
def get_analytics(date_range : DateRange):
    data=db_helper.data_btw_date(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException("status code : 500, detail : failed to retrieve expense summary from database")
    total=sum([item['TOTAL'] for item in data])
    breakdown={}
    for item in data:
        percentage=round((item['TOTAL']/total)*100 if total!=0 else 0,2)
        breakdown[item['category']]={"total":item['TOTAL'], "percent":percentage}
        
    return breakdown

@app.post("/analytics/monthly")
def complete_data():
    data=db_helper.get_monthlydata()
    return data


    
    
