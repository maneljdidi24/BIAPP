def truncateTable(Ic,sc,Start,End,cnx,tables):
    sqlQuery = f"delete from  {tables} where inv_date  between '{Start}' and  '{End}' and inv_company= {ic} and sales_company='{sc}'"
    cursor = cnxn.cursor()
    cursor.execute(sqlQuery)
    cnxn.commit()
    print("Truncate Table "+ "***"+ tables +"***")