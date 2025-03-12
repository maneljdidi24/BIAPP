
from ETL.etlSales.sql_sales import exception, mexic,tn_med,Chine,check,pt
import sqlalchemy
from sqlalchemy import create_engine

def insertIntoTable_tn_med_prod(ic,sc,Start,End,cnxnS,cnxnT,tables):
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    
    c1=check.check_data_1(ic,sc,Start,End,cnxnS)
    #print(c['x'][0])
    c2=check.check_data_2(ic,sc,Start,End,cnxnS)
    
    df1=tn_med.extract_tn_md_prod_1(ic,Start,End,cnxnS)
    
    t=0
    
    #print(len(df))
    if len(df1)==c1['X'][0] :
        print("check Query 1 ok") 
        df2=tn_med.extract_tn_md_prod_2(ic,Start,End,cnxnS) 
          
        if len(df2)>=c2['Y'][0] :
            print("check Query 2 ok") 
            t=1
        else :
            print("check Query2 Error") 
    else :
        print("check Query 1 Error")  

    if t==1 :
        print("1: First Query")
        #df1.to_sql(tables, engine, if_exists='append', index=False)
        #print("Query 1 done successufully with "+str(len(df1))+" lines inserted")
        
        df1.to_sql(tables, engine, if_exists='append', index=False)

        print("2: Second Query")
        df2.to_sql(tables, engine, if_exists='append', index=False)
        print("Query 2 done successufully with "+str(len(df2))+" lines inserted")
        
    #print(str(len(df1) + len(df2) ) + " lines inserted Into Table "+"***"+tables+"***")

    cnxnT.close()     
    cnxnS.close()



# return  pd.read_sql(text, cnx)

def insert_into_tn_exception(ic,Start,End,cnxnS,cnxnT,tables):
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1=exception.extract_tn_exception(ic,Start,End,cnxnS) 
    
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1))+" lines inserted")
    
    cnxnT.close()     
    cnxnS.close()


def insertIntoTable_mexic(ic,sc,Start,End,cnxnS,cnxnT,tables): 
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    c1=check.check_data_1(ic,sc,Start,End,cnxnS)
    c2=check.check_data_2(ic,sc,Start,End,cnxnS)
    
    df1=mexic.extract_mx_1(ic,sc,Start,End,cnxnS) 
    t=0
    
    if len(df1)>=c1['X'][0] :
        print("check Query 1 ok") 
        df2=mexic.extract_mx_2(ic,sc,Start,End,cnxnS)

        if len(df2)>=c2['Y'][0] :
            print("check Query 2 ok") 
            t=1
        else :
            print("check Query2 Error") 
    else :
        print("check Query 1 Error")  

    if t==1 :
        print("1: First Query")
        df1.to_sql(tables, engine, if_exists='append', index=False)
        print("Query 1 done successufully with "+str(len(df1))+" lines inserted")

        print("2: Second Query")
        df2.to_sql(tables, engine, if_exists='append', index=False)
        print("Query 2 done successufully with "+str(len(df2))+" lines inserted")

  
    
    cnxnT.close()     
    cnxnS.close()

def insert_into_mx_exception(ic,sc,Start,End,cnxnS,cnxnT,tables):
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1=exception.extract_mx_exception(ic,sc,Start,End,cnxnS) 
    
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1))+" lines inserted")
    
    cnxnT.close()     
    cnxnS.close()


def insertIntoTable_Chine(ic,sc,Start,End,cnxnS,cnxnT,tables): 
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    
    c1=check.check_data_1(ic,sc,Start,End,cnxnS)
    c2=check.check_data_2(ic,sc,Start,End,cnxnS)
    
    df1=Chine.extract_Chine_1(ic,sc,Start,End,cnxnS)
    t=0
    if len(c1)>0 or len(c2)>0 :
        if len(df1)==c1['X'][0] :
            print("check Query 1 ok") 
            df2=Chine.extract_Chine_2(ic,sc,Start,End,cnxnS) 
            
            if len(df2)>=c2['Y'][0] :
                print("check Query 2 ok") 
                t=1
            else :
                print("check Query2 Error") 
        else :
            print("check Query 1 Error")  

        if t==1 :
            print("1: First Query")
            print(df1)
            print(engine)
            print(tables)
           
            df1.to_sql(tables, engine, if_exists='append', index=False)
            print("Query 1 done successufully with "+str(len(df1))+" lines inserted")
            
            print("2: Second Query")
            df2.to_sql(tables, engine, if_exists='append', index=False)
            print("Query 2 done successufully with "+str(len(df2))+" lines inserted")

            
        print(str(len(df1) + len(df2) ) + " lines inserted Into Table "+"***"+tables+"***")
    
    else :
        print("No data from : "+Start+" to "+End)


    cnxnT.close()     
    cnxnS.close()

def insert_into_CHINE_exception(ic,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1=exception.extract_CHINE_exception(ic,Start,End,cnxnS) 
    
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1))+" lines inserted")
    
    cnxnT.close()     
    cnxnS.close()


def insertIntoTable_PT(ic,sc,Start,End,cnxnS,cnxnT,tables):

    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1=Pt.extract_PT(Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    
    print(str(len(df1))+" lines inserted")
    
    df2=Pt.extract_PT_TEST_2(ic,sc,Start,End,cnxnS)
    df2.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df2))+" lines inserted")

    cnxnT.close()     
    cnxnS.close()

def insertIntoTable_PT_exception(ic,sc,Start,End,cnxnS,cnxnT,tables):
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1=exception.extract_pt_exception(ic,sc,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    
    print(str(len(df1))+" lines inserted")
    
    cnxnT.close()     
    cnxnS.close()

###***********************Manual*************************************

def insertManuel_sales_invoices_tunis(plant,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    print("3: Manuel sales invoices")
    df1=tn_med.Manual_Sales_Invoice(plant,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1)) + " lines inserted Into Table "+"***"+tables+"***")
    cnxnT.close()     
    cnxnS.close()

def insertManuel_sales_invoices_PT(plant,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    print("3: Manuel sales invoices")
    df1=Pt.Manual_Sales_Invoice_PT(plant,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1)) + " lines inserted Into Table "+"***"+tables+"***")
    cnxnT.close()     
    cnxnS.close()


def insertManuel_sales_invoices_Mexico(plant,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    print("3: Manuel sales invoices")
    df1=mexic.Manual_Sales_Envoice_mexico(plant,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1)) + " lines inserted Into Table "+"***"+tables+"***")
    cnxnT.close()     
    cnxnS.close()

def insertManuel_sales_invoices_Mexico_sp(plant,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    print("3: Manuel sales invoices")
    df1=mexic.Manual_Sales_Envoice_mexico_sp(plant,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1)) + " lines inserted Into Table "+"***"+tables+"***")
    cnxnT.close()     
    cnxnS.close()


def insertManuel_sales_invoices_Chine(plant,Start,End,cnxnS,cnxnT,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    print("3: Manuel sales invoices")
    df1=Chine.Manual_Sales_Envoice_Chine(plant,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    print(str(len(df1)) + " lines inserted Into Table "+"***"+tables+"***")
    cnxnT.close()     
    cnxnS.close()

###***********************LOAD*************************************

def loadAzure(invC,Start,End,tables,r):

    print("Starting data loading process...")

    
    # Establish a connection to the source database
    source_connection_string = urllib.parse.quote_plus(f'DRIVER={{SQL Server}};Server=CORPTN-LAP-879;Database=SALES')
    source_engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={source_connection_string}', fast_executemany=True)
    print("Connected to source database.")
    
    # Read data from the source table
    source_query ="SELECT  * FROM "+tables+" where inv_company in (" + invC + ")  and  inv_date between CONVERT(DATETIME,'" + Start + "', 102) and CONVERT(DATETIME, '" + End + "', 102) and request in ("+r+") "
    print(source_query)                
    df = pd.read_sql(source_query, source_engine)

    
    #Establish a connection to the destination database
    #destination_connection_string= urllib.parse.quote_plus(f'DRIVER={{SQL Server}};Server=172.25.8.52;Trusted_connection=yes;Database=Sales;UID=sa;PWD=Bi%s@++**%%2544')                                       
    destination_connection_string= urllib.parse.quote_plus(f'DRIVER={{SQL Server}};Server=192.168.122.40;Trusted_connection=yes;Database=Sales;UID=sa;PWD=S@C0rp2022DwH')                                       
                                    
    destination_engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={destination_connection_string}', fast_executemany=True, use_setinputsizes=False)
    print("Connected to destination database.")

    """destination_connection_string = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};Server=192.168.122.40\\SQLEXPRESS,1433;Database=Sales;UID=sa;PWD=S@C0rp2022DwH')
    destination_engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={destination_connection_string}', fast_executemany=True)
    print("Connected to destination database.")"""


    # Write data to the destination table
    destination_table = tables
    df.to_sql(destination_table, destination_engine, schema=None, if_exists='append', index=False, index_label=None, chunksize=100, dtype=None, method=None)
    print("Loaded data into destination table.")
    print("Data loading process completed.")
            
            
def insert_Widget_ln_year(ic,sc,Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.check_data_year_ln(ic,sc,Start,End,cnxn)
    return dfm1

def insert_Widget_ln_mth(ic,sc,Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.check_data_month_ln(ic,sc,Start,End,cnxn)
    return dfm1

def insert_Widget_ln_day(ic,sc,Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.check_data_day_ln(ic,sc,Start,End,cnxn)
    return dfm1

#xpps
def insert_Widget_xpps_year_ma_int(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_year_ma_int(Start,End,cnxn)
    return dfm1
                    
def insert_Widget_xpps_mth_ma_int(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_mth_ma_int(Start,End,cnxn)
    return dfm1  

def insert_Widget_xpps_day_ma_int(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_day_ma_int(Start,End,cnxn)
    return dfm1    



def insert_Widget_xpps_year_kt(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_year_kt(Start,End,cnxn)
    return dfm1

def insert_Widget_xpps_mth_kt(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_mth_kt(Start,End,cnxn)
    return dfm1

def insert_Widget_xpps_day_kt(Start,End,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_day_kt(Start,End,cnxn)
    return dfm1



def insert_Widget_xpps_year_ee(Start,End,f,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_year_EE(Start,End,f,cnxn)
    return dfm1

def insert_Widget_xpps_mth_ee(Start,End,f,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_mth_EE(Start,End,f,cnxn)
    return dfm1

def insert_Widget_xpps_day_ee(Start,End,f,cnxn):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm1=check.CKECK_xpps_day_EE(Start,End,f,cnxn)
    return dfm1



#******************
#
def insert_Widget_az_loc_year(ic,sc,Start,End,cnxn,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm2=check.check_data_year_azure_local(ic,sc,Start,End,cnxn,tables)
    return dfm2

def insert_Widget_az_loc_mth(ic,sc,Start,End,cnxn,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm2=check.check_data_month_azure_local(ic,sc,Start,End,cnxn,tables)
    return dfm2

def insert_Widget_az_loc_day(ic,sc,Start,End,cnxn,tables):
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxn)
    dfm2=check.check_data_day_azure_local(ic,sc,Start,End,cnxn,tables)
    return dfm2






def insertIntoTable_portugal(Start,End,cnxnS,cnxnT,tables):
    
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    df1= pt.extract_PT_localhost(tables,Start,End,cnxnS)
    df1.to_sql(tables, engine, if_exists='append', index=False)
    
    print(str(len(df1))+" lines inserted")
    
    cnxnT.close()     
    cnxnS.close()

#
#
