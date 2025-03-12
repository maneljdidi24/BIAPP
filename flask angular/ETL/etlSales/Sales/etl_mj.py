import time
from ETL.etlSales.Sales import  extractionLn, extractionXpps, truncate
from dao import dao
import warnings
warnings.filterwarnings("ignore")
# ***********************************    EXTRACT_DATA

def F_Extract(r,d1,d2):
   
    region=r
    date1=d1
    date2=d2

    match (region):
        case "COF MX"           :#610
            s=time.time() 
            print("1-start... ")
            print("You are directed to Ln") 
            #cnxnT = dao.getTargetConnection()       
            cnxnT = dao.getAZURE_Connection2("sales")
            cnxnS = dao.getSourceConnectionLn_Mexico()
            tabl = "Global_Sales_Mexico" 
            start = date1
            end = date2
            
            ic = 610
            #step1
            sc = 630
          
            print("step1: 630 from "+start+" to "+end)
            extractionLn.insertIntoTable_mexic(ic,sc,start,end,cnxnS,cnxnT,tabl)    
            #step2
            sc=640
            cnxnT = dao.getAZURE_Connection2("sales")
            cnxnS = dao.getSourceConnectionLn_Mexico()
            print("step2: 640 from "+start+" to "+end)
            extractionLn.insertIntoTable_mexic(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #manual  
            print("MANUAL SALES INVOICE COF MX")
            cnxnT = dao.getAZURE_Connection2("sales")          
            cnxnS = dao.getSourceConnectionLn_Mexico()
            
            invC = 610
            extractionLn.insertManuel_sales_invoices_Mexico(invC,start,end,cnxnS,cnxnT,tabl)
           
            #Exception
            print("Exception SALES INVOICE COF MX")
            ic=610
            tabl = "Global_Sales_mexico" #liste de choix

            sc=630
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Mexico()
            extractionLn.insert_into_mx_exception(ic,sc,start,end,cnxnS,cnxnT,tabl)
            
            sc=640
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Mexico()           
            extractionLn.insert_into_mx_exception(ic,sc,start,end,cnxnS,cnxnT,tabl)
            
            
            e=time.time()
            elapsed=(e-s)
            print(f'insert done : {elapsed:}s')
  
        case "COF SP"           :#660
            print("COF SP : 660")
            print("You are directed to Ln")
            #cnxnT = dao.getAZURE_Connection2("sales")
            cnxnT = dao.getTargetConnection()
            tabl = "Global_Sales_Mexico" 
            ic=660
            sc=660
            start = date1
            end = date2
            
            cnxnS = dao.getSourceConnectionLn_Mexico()
            completed=10
            print("step1: 660")
            extractionLn.insertIntoTable_mexic(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #manual  
            print("MANUAL SALES INVOICE COF MX")
            #cnxnT = dao.getAZURE_Connection2("sales")
            cnxnT = dao.getTargetConnection()        
            cnxnS = dao.getSourceConnectionLn_Mexico()
            extractionLn.insertManuel_sales_invoices_Mexico(ic,start,end,cnxnS,cnxnT,tabl)
           
            #Exception
            print("Exception SALES INVOICE COF MX")
            #cnxnT = dao.getAZURE_Connection2("sales")
            cnxnT = dao.getTargetConnection()         
            cnxnS = dao.getSourceConnectionLn_Mexico()
            extractionLn.insert_into_mx_exception(ic,sc,start,end,cnxnS,cnxnT,tabl)





        case "COF TN"           :#102
            print("3- "+region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            tabl = "Global_Sales_Tunis" #liste de choix
            ic = 102
            sc=102    
            start = date1
            end =   date2
            s=time.time()      
            extractionLn.insertIntoTable_tn_med_prod(ic,sc,start,end,cnxnS,cnxnT,tabl)
            e=time.time()
            elapsed=(e-s)
            print(f'insert done : {elapsed:}s')

            #Manual
            print("MANUAL SALES INVOICE COF TN")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insertManuel_sales_invoices_tunis(ic,start,end,cnxnS,cnxnT,tabl)
            
            
            #exception
            print("Exception SALES INVOICE COF TN")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insert_into_tn_exception(ic,start,end,cnxnS,cnxnT,tabl)         
            


             
        case "COF MED"          :#104
                 
            print("4- "+region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            tabl = "Global_Sales_Tunis" #liste de choix
            ic = 104
            sc=104    
            start = date1
            end =   date2
            s=time.time()    
            extractionLn.insertIntoTable_tn_med_prod(ic,sc,start,end,cnxnS,cnxnT,tabl)
            
            #Manual
            print("MANUAL SALES INVOICE COF MED")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insertManuel_sales_invoices_tunis(ic,start,end,cnxnS,cnxnT,tabl)
            
            
            #exception
            print("Exception SALES INVOICE COF MED")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insert_into_tn_exception(ic,start,end,cnxnS,cnxnT,tabl)   

 

        case "COF SARL"         :#105
            st1=time.time()      
            print("3- "+region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            tabl = "Global_Sales_Tunis"
            ic = 105
            sc = 105
            start = date1
            end =   date2
            extractionLn.insertIntoTable_tn_med_prod(ic,sc,start,end,cnxnS,cnxnT,tabl)
            
            #Manual
            print("MANUAL SALES INVOICE COF SARL")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insertManuel_sales_invoices_tunis(ic,start,end,cnxnS,cnxnT,tabl)
            
            #exception
            print("Exception SALES INVOICE COF SARL")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_tn_med_prod()
            extractionLn.insert_into_tn_exception(ic,start,end,cnxnS,cnxnT,tabl)      


        case "COF MA & INT"     :
            print(region)
            print("You are directed to Xpps")
            #cnxnT = dao.getTargetConnection()
            cnxnT = dao.getAZURE_Connection2("sales")         
            cnxnS = dao.getSOURCEConnectionXPPS_ma_int() 
            tabl1="Global_Sales_Maroc"
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            ic="112,114"
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_ma_int(start,end,cnxnS,cnxnT,tabl1) 

        case "COF KT"           :
            print(region)
            print("You are directed to Xpps")
            completed =10 
            #cnxnT = dao.getTargetConnection()
            cnxnT = dao.getAZURE_Connection2("sales")
            cnxnS = dao.getSOURCEConnectionXPPS_kt()
            completed +=10
            tabl1="Global_Sales_Maroc"
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            ic="113"
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_kt(start,end,cnxnS,cnxnT,tabl1)   
                   

        case "COF EE"           :# 132 133 134  135
            print(region)
            print("You are directed to Xpps :")
            cnxnT = dao.getAZURE_Connection2("sales")
            #cnxnT = dao.getTargetConnection()
            cnxnS = dao.getSOURCEConnectionXPPS_EE()
            completed =10
            #si test connexion ok
            tabl1="Global_Sales_EE"
            Firm=1
            ic=132
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            print(region)
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_EE(Firm,start,end,cnxnS,cnxnT,tabl1) 
        case "COF PL"           :# 132 133 134  135
            print(region)
            print("You are directed to Xpps :")
            cnxnT = dao.getAZURE_Connection2("sales")
            #cnxnT = dao.getTargetConnection()
            cnxnS = dao.getSOURCEConnectionXPPS_EE()
            completed =10
            #si test connexion ok
            tabl1="Global_Sales_EE"
            Firm=2
            ic=133
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            print(region)
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_EE(Firm,start,end,cnxnS,cnxnT,tabl1) 
        case "COF MK"           :# 132 133 134  135
            print(region)
            print("You are directed to Xpps :")
            cnxnT = dao.getAZURE_Connection2("sales")
            #cnxnT = dao.getTargetConnection()
            cnxnS = dao.getSOURCEConnectionXPPS_EE()
            completed =10
            #si test connexion ok
            tabl1="Global_Sales_EE"
            Firm=3
            ic=135
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            print(region)
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_EE(Firm,start,end,cnxnS,cnxnT,tabl1) 
        case "COF SRB"          :# 132 133 134  135
            print(region)
            print("You are directed to Xpps :")
            cnxnT = dao.getAZURE_Connection2("sales")
            #cnxnT = dao.getTargetConnection()
            cnxnS = dao.getSOURCEConnectionXPPS_EE()
            completed =10
            #si test connexion ok
            tabl1="Global_Sales_EE"
            Firm=4
            ic=134
            v1=date1
            v2=date2
            date1_xpps=str(v1[0])+str(v1[1])+str(v1[2])+str(v1[3])+str(v1[5])+str(v1[6])+str(v1[8])+str(v1[9])
            date2_xpps=str(v2[0])+str(v2[1])+str(v2[2])+str(v2[3])+str(v2[5])+str(v2[6])+str(v2[8])+str(v2[9])
            start = date1_xpps
            end = date2_xpps
            print(region)
            #truncate.truncateTable_xpps(cnxnT,tabl1,ic,start,end)
            extractionXpps.insertIntoTable_EE(Firm,start,end,cnxnS,cnxnT,tabl1) 
        case "COF GR"           :#125
    
            print(region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnection_LN_DB_Portugal()
            tabl = "Global_Sales_Portugal" #liste de choix
            ic = 122
            sc = 125
            start = date1
            end =   date2  
            extractionLn.insertIntoTable_PT(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #Manual
            #Exception
            print("Exception : COF GR")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnection_LN_DB_Portugal()
            extractionLn.insertIntoTable_PT_exception(ic,sc,start,end,cnxnS,cnxnT,tabl)




           
        case "COF HG"           :#127
            #print(region+"From"+ start +"To"+end)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnection_LN_DB_Portugal()
            tabl = "Global_Sales_Portugal" #liste de choix
            ic = 127
            sc = 122
            start = date1
            end =   date2  
            extractionLn.insertIntoTable_PT(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #Manual
            #Exception
            print("Exception : COF HG")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnection_LN_DB_Portugal()
            eextractionLn.insertIntoTable_PT_exception(ic,sc,start,end,cnxnS,cnxnT,tabl)
            


        case "COF TT"           :#153
            print(region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            tabl = "Global_Sales_Chine" #liste de choix
            ic= 153
            sc = 153
            start = date1
            end =   date2
            extractionLn.insertIntoTable_Chine(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #Manual
            print("MANUAL SALES INVOICE COF TT")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            extractionLn.insertManuel_sales_invoices_Chine(ic,start,end,cnxnS,cnxnT,tabl)

            #Exception
            print("Exception SALES INVOICE COF TT")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            extractionLn.insert_into_CHINE_exception(ic,start,end,cnxnS,cnxnT,tabl)
           


        case "COF TJ"           :#502

            print(region)         
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            tabl = "Global_Sales_Chine" #liste de choix
            ic=502
            sc =502
            start = date1
            end =   date2    
            extractionLn.insertIntoTable_Chine(ic,sc,start,end,cnxnS,cnxnT,tabl)

            #Manual
            print("MANUAL SALES INVOICE COF TJ")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            extractionLn.insertManuel_sales_invoices_Chine(ic,start,end,cnxnS,cnxnT,tabl)
    
            #Exception
            print("Exception SALES INVOICE COF Tj")
            cnxnT = dao.getAZURE_Connection2("sales")           
            cnxnS = dao.getSourceConnectionLn_Chine()
            extractionLn.insert_into_CHINE_exception(ic,start,end,cnxnS,cnxnT,tabl)

        case "Load COF PT"      :
            print("region")
            cnxnS = dao.getTargetConnection()
            print("1")
            cnxnT = dao.getAZURE_Connection2("sales")
            tabl = "Global_Sales_portugal" #liste de choix
            start = date1
            end =   date2    
            extractionLn.insertIntoTable_portugal(start,end,cnxnS,cnxnT,tabl)     


# ***********************************    TRANSFORM_DATA

def RunState (cnx)   :
    sql=f"""Select top 1 run_status as X 
            From msdb.dbo.sysjobs j 
            INNER JOIN msdb.dbo.sysjobsteps s ON j.job_id = s.job_id
            INNER JOIN msdb.dbo.sysjobhistory h ON s.job_id = h.job_id AND s.step_id = h.step_id AND h.step_id <> 0
            WHERE j.enabled = 1  and j.name = 'BI_TransformData'
            ORDER BY  msdb.dbo.agent_datetime(run_date, run_time) DESC 
        """
    return pd.read_sql(sql, cnx)



#***************************

def F_Transform():
    print("hello")
    conn = dao.getAZURE_Connection2("sales")
    curs = conn.cursor()  
    s = """SET NOCOUNT ON; exec msdb.dbo.sp_start_job N'BI_TransformData' """
    curs.execute(s)
    print("sp: BI_TransformData... ")
    time.sleep(300)  
   
    C1 = RunState(conn)
    if C1['X'][0] == 1:
        print("Done successfully")
    elif C1['X'][0] == 0:
        print("Execution Error")


# ***********************************    LOAD_DATA
    
from sqlalchemy import text

def F_Load(r, d1, d2):
    print("hello")
    engine = dao.getAZURE_Connection2("sales")  # Vérifiez que c'est bien un SQLAlchemy engine

    with engine.connect() as conn:
        s = text("SET NOCOUNT ON; exec msdb.dbo.sp_start_job N'BI_Load_fact_sales'")
        conn.execute(s)
        print("sp: BI_Load_fact_sales... ")
        time.sleep(3)

        C1 = RunState(conn)  # Assurez-vous que RunState fonctionne avec SQLAlchemy
        if C1['X'][0] == 1:
            print("Done successfully")
        elif C1['X'][0] == 0:
            print("Execution Error")

   
    
    


   
            
            
    
