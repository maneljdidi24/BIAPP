import pandas as pd
#xpps_maroc_ma&int
import pandas as pd
import numpy as np

def extract_kt(Start,End,cnx):
    text = f"""select 
    X301SD.lpli.lglgrf as ID_Line,
    X301SD.lpli.LGBRAR as Trans_Type,
    X301SD.lpli.LGRGNR as Invoice_N,
    X301SD.lpli.LGWACD as Currency,
    X301SD.kdst.kdNAME as Desc_STPB,
    cast (X301SD.lpli.LGKDNR as varchar (20)) as Sold_To_BP,
    cast (X301SD.lpli.LGNEWT as real) as Net_Line_Amount,
    cast (X301SD.lpli.LGLIMG as real) as Inv_Quantity,
    cast (X301SD.lpli.LGNEWT as real)/ cast (X301SD.lpli.LGLIMG as real) AS PRICE,
    cast ((substr(X301SD.lpli.LGRGDA,5,2)||'/'||substr(X301SD.lpli.LGRGDA,7,2)||'/'|| substr(X301SD.lpli.LGRGDA,1,4) ) as date) as Inv_Date,
    cast (X301SD.lpli.LGPREI as real) as Added_value,
    X301SD.lpli.LGTENR as item,
    X301SD.teil.TEBEZ1 as Item_Description,
    X301SD.lpli.LGLIES as shipment,
    cast ('COF KT' as varchar (10)) as Plant,
    cast ('Marocco' as varchar (20)) as Region,
    X301SD.lpli.lglanr as Type,
    CASE when((X301SD.lpli.LGBRAR ='RM' or X301SD.lpli.LGBRAR='RE')and X301SD.lpli.lglanr='PF')THEN 'FG' ELSE 'NFG' END as type_invoice,
    CAST (X301SD.lpli.lgstat as varchar (4))as Inv_Stat,
    X301SD.teil.TEPRGR as fam,
    X301SD.teil.TETEFA as sect,
    X301SD.lplp.LPSNBE as Part_Number,
    substr(trim(FP.FSTEXT),1,5 ) as Price_Unit,
    substr(trim(FQ.FSTEXT),1,5 ) as Qty_Unit,
    cast(( (cast ( X301SD.afp4.p4emtn as real)/cast (X301SD.afp4.p4baku as real))/1000) as real) as Metal_Rate,
    cast (p4emfk as real) as Metal_weight_sales,
    '113' as Inv_Company,
    '113' as sales_Company,
    'EUR' as Reporting_Currency_Euro	,	
    'USD' as Reporting_Currency_USD,
    1 as active ,
    1 as request,
    0 as confirmed
    ,X301SD.lpli.LGVENR as Ship_To_BP
    ,shp.kdNAME as Ship_To_Description
    
    FROM X301SD.lpli
    
    LEFT JOIN X301SD.teil ON X301SD.lpli.lgfirm=X301SD.teil.tefirm AND X301SD.lpli.lgtenr=X301SD.teil.tetenr
    LEFT JOIN X301SD.lplp ON X301SD.lpli.lgfirm=X301SD.lplp.lpfirm AND X301SD.lpli.lgkdnr = X301SD.lplp.lpkdnr
    AND X301SD.lpli.lgvenr=X301SD.lplp.lpvenr AND X301SD.lpli.lgtenr=X301SD.lplp.lptenr
    LEFT JOIN X301SD.FSTX FQ ON FQ.FSFIRM =X301SD.lpli.LGFIRM AND X301SD.teil.TEMEIN=right(TRIM(FQ.FSSCHL),1)
    AND FQ.FSFLNA='T2TXBZ'AND FQ.FSSCHL LIKE'02%'AND FQ.FSSPCD='F'
    LEFT JOIN X301SD.FSTX FP ON FP.FSFIRM =X301SD.lpli.LGFIRM AND X301SD.teil.temepr=right(TRIM(FP.FSSCHL),1)
    AND FP.FSFLNA='T2TXBZ'AND FP.FSSCHL LIKE'02%'AND FP.FSSPCD='F'    
    LEFT JOIN X301SD.afp4 on X301SD.lpli.lglgrf=X301SD.afp4.p4lgrf and P4KUDA > 20221231 and p4firm =1
    LEFT JOIN X301SD.kdst ON X301SD.lpli.lgfirm=X301SD.kdst.kdfirm AND X301SD.lpli.lgkdnr=X301SD.kdst.kdkdnr 
    and X301SD.kdst.kdvenr=1
    inner JOIN X301SD.kdst shp ON 
    X301SD.lpli.lgfirm= shp.kdfirm 
    AND X301SD.lpli.lgkdnr =shp.kdkdnr     
    AND X301SD.lpli.LGVENR= shp.kdvenr

    WHERE 
    X301SD.lpli.LGRGDA BETWEEN '{Start}' AND '{End}'
    and X301SD.lpli.lgfirm=1
    """
    return  pd.read_sql(text, cnx)

def extract_ma_int(Start,End,cnx):

    text = f""" select 
    X301SD.lpli.lglgrf as ID_Line,
    X301SD.lpli.LGBRAR as Trans_Type,
    X301SD.lpli.LGRGNR as Invoice_N,
    X301SD.lpli.LGWACD as Currency,
    X301SD.kdst.kdNAME as Desc_STPB,
    X301SD.lpli.LGKDNR as Sold_To_BP,
    cast (X301SD.lpli.LGNEWT as real) as Net_Line_Amount,
    cast (X301SD.lpli.LGLIMG as real) as Inv_Quantity,
    cast (X301SD.lpli.LGNEWT as real)/cast (X301SD.lpli.LGLIMG as real) as Price,
    cast ((substr(X301SD.lpli.LGRGDA,5,2)||'/'||substr(X301SD.lpli.LGRGDA,7,2)||'/'|| substr(X301SD.lpli.LGRGDA,1,4) ) as date) as Inv_Date,
    cast ( X301SD.lpli.LGPREI as real) as Added_value,
    X301SD.lpli.LGTENR as item,
    X301SD.teil.TEBEZ1 as Item_Description,
    X301SD.lpli.LGLIES as shipment,
    CASE when (X301SD.lpli.lgfirm = '1') 
         THEN cast ('COF MA' as varchar (10)) 
         ELSE cast ('COF INT' as varchar (10)) 
         END as Plant,
    CASE when (X301SD.lpli.lgfirm = '1') 
         THEN '112' 
         ELSE '114' 
         END as Inv_Company,
    CASE when (X301SD.lpli.lgfirm = '1') 
         THEN '112' 
         ELSE '114' 
         END as sales_Company,
   
    X301SD.lpli.lglanr as Type,
    
    CASE when (X301SD.lpli.lgfirm ='1') then 
        (CASE when (X301SD.lpli.LGBRAR= 'RM' or X301SD.lpli.LGBRAR='RE')THEN 'FG' ELSE 'NFG' END)  
    when (X301SD.lpli.lgfirm ='2') then 
        CASE when ((X301SD.lpli.LGBRAR= 'RM' or X301SD.lpli.LGBRAR='RE') and (X301SD.lpli.lglanr='CI' or X301SD.lpli.lglanr='YI'))THEN 'FG' ELSE 'NFG' END 
    END AS TYPE_INVOICE,  

    CAST (X301SD.lpli.lgstat as varchar (4))as Inv_Stat,
    X301SD.teil.TEPRGR as fam,
    X301SD.teil.TETEFA as sect,
    X301SD.lplp.LPSNBE as Part_Number,
    substr(trim(FP.FSTEXT),1,5 ) as Price_Unit,
    substr(trim(FQ.FSTEXT),1,5 ) as Qty_Unit,
    cast(( (cast ( X301SD.afp4.p4emtn as real)/cast (X301SD.afp4.p4baku as real))/1000) as real) as Metal_Rate,
    cast (p4emfk as real) as Metal_weight_sales,
    'EUR' as Reporting_Currency_Euro	,	
    'USD' as Reporting_Currency_USD,
    1 as active ,
    1 as request,
    0 as confirmed,
    
    X301SD.lpli.LGVENR as Ship_To_BP, shp.kdNAME as Ship_To_Description
   
    FROM X301SD.lpli 
    
    LEFT JOIN X301SD.teil ON X301SD.lpli.lgfirm=X301SD.teil.tefirm AND X301SD.lpli.lgtenr=X301SD.teil.tetenr
    
    LEFT JOIN X301SD.lplp ON X301SD.lpli.lgfirm=X301SD.lplp.lpfirm AND X301SD.lpli.lgkdnr = X301SD.lplp.lpkdnr
    AND X301SD.lpli.lgvenr=X301SD.lplp.lpvenr AND X301SD.lpli.lgtenr=X301SD.lplp.lptenr
    
    LEFT JOIN X301SD.FSTX FQ ON FQ.FSFIRM =X301SD.lpli.LGFIRM AND X301SD.teil.TEMEIN=right(TRIM(FQ.FSSCHL),1)
    AND FQ.FSFLNA='T2TXBZ'AND FQ.FSSCHL LIKE'02%'AND FQ.FSSPCD='F'
    
    LEFT JOIN X301SD.FSTX FP ON FP.FSFIRM =X301SD.lpli.LGFIRM AND X301SD.teil.temepr=right(TRIM(FP.FSSCHL),1)
    AND FP.FSFLNA='T2TXBZ'AND FP.FSSCHL LIKE'02%'AND FP.FSSPCD='F'    
    
    LEFT JOIN X301SD.afp4 on X301SD.lpli.lglgrf=X301SD.afp4.p4lgrf and P4KUDA > 20221200 and p4firm =2

    LEFT JOIN X301SD.kdst ON X301SD.lpli.lgfirm=X301SD.kdst.kdfirm AND X301SD.lpli.lgkdnr=X301SD.kdst.kdkdnr 
    and X301SD.kdst.kdvenr=1

    LEFT JOIN X301SD.kdst shp ON X301SD.lpli.lgfirm= shp.kdfirm AND X301SD.lpli.lgkdnr =shp.kdkdnr     
    and shp.kdvenr=X301SD.lpli.LGVENR
    
    WHERE X301SD.lpli.LGRGDA BETWEEN '{Start}' AND '{End}'
    
    """
    #print (text)
    return  pd.read_sql(text, cnx)


