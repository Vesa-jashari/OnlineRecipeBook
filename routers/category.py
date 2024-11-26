from streamlit import status
from unicodedata import category

from models.category import CategoryBase,Category
from database import get_db_connection
from fastapi import APIRouter, HTTPExeception

router=APIRouter()

@router.get("/categories/", List[Category])
def get_categories():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("Select if, name from categories")
    categories=cursor.fetchall()
    conn.close()
    category_list=[{"id":cat[0],"name":cat[1]} for cat in categories]
    return category_list