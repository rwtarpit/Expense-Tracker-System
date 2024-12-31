import mysql.connector
from contextlib import contextmanager
from logger_setup import setup_logger

logger=setup_logger('db_helper')

@contextmanager
def db_cursor(commit=False):
    connection = mysql.connector.connect(
    host="localhost",       # Replace with your MySQL server address
    user="root",            # Your MySQL username
    password="root",        # Your MySQL password
    database="expense_manager"       # Name of your database
    )
    # Check connection
    if connection.is_connected():
        print("Connected to MySQL database")
    else:
        print("connection unsuccessful")
    cursor=connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()
    
def get_monthlydata():
    logger.info(f"get_monthlydata() called")
    with db_cursor() as cursor:
        cursor.execute("SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) AS total_expense FROM expenses GROUP BY month ORDER BY month DESC;")
        expenses=cursor.fetchall()
        return expenses
            
            
def data_by_date(expense_date):
    logger.info(f"data_by_date called with {expense_date}")
    with db_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date= %s",(expense_date,))
        expenses=cursor.fetchall()
        return expenses
    
def enterdata( expense_date, amount, category, notes):
    logger.info(f"enterdata called with {(expense_date,amount, category, notes)}")
    with db_cursor(commit=True) as cursor:
        cursor.execute("insert into expenses (expense_date, amount, category, notes) values(%s,%s,%s,%s)",
                      ( expense_date, amount, category, notes) )

def delete_data(expense_date):
    logger.info(f"delete_data called with {expense_date}")
    with db_cursor(commit=True) as cursor:
        cursor.execute("delete from expenses where expense_date= %s ",(expense_date,))
        
def data_btw_date(start_date,end_date):
    logger.info(f"data_btw_date called with {(start_date,end_date)}")
    with db_cursor() as cursor:
        cursor.execute(" select category, sum(amount) as TOTAL from expenses where expense_date between %s and %s group by category",(start_date,end_date))
        data=cursor.fetchall()
        return data



         




        
        
        

        
        
    







    
    





