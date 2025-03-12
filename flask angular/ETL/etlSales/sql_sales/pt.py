
import pandas as pd
import numpy as np


def extract_PT_TEST_1(ic,sc,Start,End,cnx):#sales invoice
    text= f"""select

    (
    cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shpm as char))+'-'+
    rtrim(cast(ttdsls340{sc}.t_shpo as char))+'-'+  
	isnull(rtrim(ltrim(ttcmpr110{sc}.t_matr))
			,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,ttdsls340{sc}.t_shpo
                                    order by      tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm,ttdsls340{sc}.t_shpo )as varchar(3))
			)
	) as id_line,



    tcisli310{ic}.t_tran    as Trans_Type,
    tcisli310{ic}.t_idoc    as Invoice_N,  
    tcisli305{ic}.t_ccur    as Currency,
    tcisli310{ic}.t_ofbp    as Sold_To_BP,
    ttccom100100.t_nama     as Desc_STPB,
    tcisli310{ic}.t_dqua    as Inv_Quantity,
    tcisli310{ic}.t_cuns    as Qty_Unit ,
    tcisli310{ic}.t_pric    as Price ,
    tcisli310{ic}.t_cups    as Price_Unit ,
    tcisli310{ic}.t_orno    as Sales_O_S_N,
    tcisli310{ic}.t_item    as Item ,
    ttcibd001100.t_dsca     as Item_Description,
    tcisli310{ic}.t_amti    as Net_Line_Amount,
    tcisli305{ic}.t_idat    as Inv_Date,
    tcisli310{ic}.t_stbp    as  Ship_To_BP,
    ''                         as  Ship_To_Description,
    ttcmpr100{sc}.t_mtex       as  Mterial_Exchange,
    ttcmpr110{sc}.t_qmct       as  Metal_weight_sales,
    ttdsls301{sc}.t_pric       as  Added_value,
    ttcmpr110{sc}.t_acpr       as  Metal_Rate,
    ttdsls301{sc}.t_cono       as Contract_N,
    ttdsls340{sc}.t_dlno       as shipment,
    ttdsls340{sc}.t_shpo       as shipment_line,
    ttcibd004{sc}.t_aitc       as part_number,
    tcisli310{ic}.t_amth_1  as Net_Line_Amount_HC,
    'EUR'                      as HOME_CURRENCY,
    tcisli310{ic}.t_amth_2 as Reporting_Amount_Euro,
    'EUR'                     as Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3 as Reporting_Amount_USD,
    'USD'                     as Reporting_Currency_USD,
    ttcmpr110{sc}.t_matr      as Material_Type,
    tcisli310{ic}.t_sfcp   as Inv_Company,
    tcisli310{ic}.t_srcp   as Sales_Company,
    
    (CASE   when (tcisli310{ic}.t_srcp = 122 AND tcisli310{ic}.t_sfcp = 122)  then 'COF PT' 
            when (tcisli310{ic}.t_srcp = 122 AND tcisli310{ic}.t_sfcp = 127)  then 'COF HG'
            when (tcisli310{ic}.t_srcp = 125 AND tcisli310{ic}.t_sfcp = 122)  then 'COF GR'
            
        END)     as plant,
   
    (case when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) as TYPE_INVOICE,
    ''         as warehouse,
    1          as request  ,
    0          as confirmed,
    1          as active,
    'Portugal' as region

    FROM
    tcisli305{ic},
    tcisli310{ic} left join ttcibd004{sc}
                    on tcisli310{ic}.t_item=ttcibd004{sc}.t_item and ttcibd004{sc}.t_bpid=tcisli310{ic}.t_stbp
    
    ,
    ttccom100100 ,
    ttcibd001100,
    ttdsls340{sc} left join ttcmpr100{sc}
    left join ttcmpr110{sc} on ttcmpr110{sc}.t_bobj=ttcmpr100{sc}.t_bobj and ttcmpr100{sc}.t_borf=ttcmpr110{sc}.t_borf
    on ttcmpr100{sc}.t_borf=concat( ttdsls340{sc}.t_spon ,'/',ttdsls340{sc}.t_wpon,'/',ttdsls340{sc}.t_wsqn,'/',ttdsls340{sc}.t_seqn,'/',ttdsls340{sc}.t_invl) and
    ttcmpr100{sc}.t_bobj=concat( ttdsls340{sc}.t_schn,'/',ttdsls340{sc}.t_sctp ,'/',ttdsls340{sc}.t_revn) ,
    ttdsls301{sc},
    ttdsls311{sc},
   
    ttdsls321{sc}
    
    WHERE
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
    and tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp
    and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc
    and ttcibd001100.t_item=tcisli310{ic}.t_item
    and tcisli310{ic}.t_ofbp= ttccom100100.t_bpid
    and tcisli310{ic}.t_idoc=ttdsls340{sc}.t_invn
    
    and tcisli310{ic}.t_tran=ttdsls340{sc}.t_ttyp
    and tcisli310{ic}.t_tran=tcisli305{ic}.t_tran 

    and ttdsls340{sc}.t_schn=tcisli310{ic}.t_orno
    and tcisli310{ic}.t_shln=ttdsls340{sc}.t_shpo
    and ttdsls340{sc}.t_dlno=tcisli310{ic}.t_shpm
    and ttdsls321{sc}.t_worn=ttdsls340{sc}.t_schn
    and ttdsls321{sc}.t_sctp=2 and ttdsls321{sc}.t_wsqn=ttdsls340{sc}.t_wsqn 
    and ttdsls311{sc}.t_schn=ttdsls340{sc}.t_schn and ttdsls311{sc}.t_revn=ttdsls321{sc}.t_revn 
    and ttdsls311{sc}.t_sctp=2
    and ttdsls311{sc}.t_cono=ttdsls301{sc}.t_cono and ttdsls301{sc}.t_pono=ttdsls311{sc}.t_pono
    
    
    and tcisli310{ic}.t_sfcp =tcisli305{ic}.t_sfcp
	
    and tcisli305{ic}.t_stat=80 
    
    """

    return  pd.read_sql(text, cnx)


def extract_PT_TEST_2(ic,sc,Start,End,cnx):#sales schede
    text= f"""select

    (
    cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(ttdsls406{sc}.t_shpm as char))+'-'+
    rtrim(cast(ttdsls406{sc}.t_shln as char))+'-'+  
	isnull(rtrim(ltrim(ttcmpr110{sc}.t_matr ))
		,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln
                                 order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln )as varchar(3))
			)
	) as id_line,
    
    tcisli310{ic}.t_tran  as  Trans_Type,
    tcisli310{ic}.t_idoc  as  Invoice_N,
    tcisli305{ic}.t_ccur  as  Currency,
    tcisli310{ic}.t_ofbp  as  Sold_To_BP,
    ttccom100100.t_nama      as  Desc_STPB,
    tcisli310{ic}.t_dqua  as  Inv_Quantity,
    tcisli310{ic}.t_cuns  as  Qty_Unit ,
    tcisli310{ic}.t_pric  as  Price,
    tcisli310{ic}.t_cups  as  Price_Unit ,
    tcisli310{ic}.t_orno  as  Sales_O_S_N,
    tcisli310{ic}.t_item  as  Item ,
    ttcibd001100.t_dsca      as  Item_Description,
    tcisli310{ic}.t_amti  as  Net_Line_Amount,
    tcisli305{ic}.t_idat  as  Inv_Date ,

    
    tcisli310{ic}.t_stbp  as  Ship_To_BP,
    ''                       as  Ship_To_Description,
    ttcmpr100{sc}.t_mtex     as  Mterial_Exchange,
    ttcmpr110{sc}.t_qmct     as  Metal_weight_sales,
    ttdsls301{sc}.t_pric     as  Added_value,
    ttcmpr110{sc}.t_acpr     as  Metal_Rate,

    ttdsls301{sc}.t_cono     as  Contract_N,
    ttdsls406{sc}.t_shpm     as  shipment,
    ttdsls406{sc}.t_shln     as  shipment_line,
    ttcibd004{sc}.t_aitc     as  part_number,
   
    
    (CASE   when (tcisli310{ic}.t_srcp = 122 AND tcisli310{ic}.t_sfcp = 122)  then 'COF PT' 
            when (tcisli310{ic}.t_srcp = 122 AND tcisli310{ic}.t_sfcp = 127)  then 'COF HG'
            when (tcisli310{ic}.t_srcp = 125 AND tcisli310{ic}.t_sfcp = 122)  then 'COF GR'
            
        END)     as plant,
    
    
    'Portugal' as region,

    tcisli310{ic}.t_amth_1  as  Net_Line_Amount_HC    ,'EUR'  as  HOME_CURRENCY,
    tcisli310{ic}.t_amth_2  as  Reporting_Amount_Euro ,'EUR'  as  Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3  as  Reporting_Amount_USD  ,'USD'  as  Reporting_Currency_USD,
    ttcmpr110{sc}.t_matr       as  Material_Type,
    tcisli310{ic}.t_sfcp    as  Inv_Company,
    tcisli310{ic}.t_srcp    as  Sales_Company,
    '' as  warehouse
    ,2 as request
    ,1 as active
    ,0 as confirmed
    ,(case  when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) as TYPE_INVOICE

    FROM
    tcisli305{ic},
    tcisli310{ic}
    left join ttcibd004{sc} on Replace(tcisli310{ic}.t_item,' ','')=Replace(ttcibd004{sc}.t_item,' ','') and Replace(ttcibd004{sc}.t_bpid,' ','')=Replace(tcisli310{ic}.t_stbp,' ','') ,
    ttccom100100 ,
    ttcibd001100,
    ttdsls406{sc} left join ttcmpr100{sc} left join ttcmpr110{sc} on
    ttcmpr110{sc}.t_bobj=ttcmpr100{sc}.t_bobj and
    ttcmpr100{sc}.t_borf=ttcmpr110{sc}.t_borf
    on ttcmpr100{sc}.t_bobj= ttdsls406{sc}.t_orno and ttcmpr100{sc}.t_borf=concat(  ttdsls406{sc}.t_pono ,'/', ttdsls406{sc}.t_sqnb,'/', ttdsls406{sc}.t_dsqn,'/', ttdsls406{sc}.t_invl),
    ttdsls401{sc} left join ttdsls301{sc} on ttdsls301{sc}.t_cono=ttdsls401{sc}.t_cono and ttdsls401{sc}.t_cpon=ttdsls301{sc}.t_pono

    WHERE
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) and
    tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and
    tcisli305{ic}.t_stat=80 and
    ttcibd001100.t_item=tcisli310{ic}.t_item and
    tcisli310{ic}.t_ofbp= ttccom100100.t_bpid and
    tcisli310{ic}.t_idoc= ttdsls406{sc}.t_invn and

    tcisli310{ic}.t_tran= ttdsls406{sc}.t_ttyp and
    tcisli310{ic}.t_tran=tcisli305{ic}.t_tran and
    
    ttdsls406{sc}.t_orno= tcisli310{ic}.t_orno and
    ttdsls406{sc}.t_pono= tcisli310{ic}.t_pono and
    tcisli310{ic}.t_shln= ttdsls406{sc}.t_shln and
    tcisli310{ic}.t_shpm= ttdsls406{sc}.t_shpm and
    ttdsls401{sc}.t_pono= ttdsls406{sc}.t_pono and 
    ttdsls401{sc}.t_ofbp= tcisli310{ic}.t_ofbp and 
    ttdsls401{sc}.t_item= tcisli310{ic}.t_item and 
    ttdsls401{sc}.t_sqnb= ttdsls406{sc}.t_sqnb and 
    ttdsls401{sc}.t_orno= ttdsls406{sc}.t_orno and
    
    tcisli310{ic}.t_sfcp =tcisli305{ic}.t_sfcp
	

    """
    #print(text)
    return  pd.read_sql(text, cnx)


def Manual_Sales_Invoice_PT(ic,Start,End,cnx):#
    text= f"""select
    (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
    cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'
	+cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc
                             order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc )as varchar(3))
	) as id_line,

    tcisli310{ic}.t_tran   as  Trans_Type,
    tcisli310{ic}.t_idoc   as  Invoice_N,
    tcisli305{ic}.t_ccur   as  Currency,
    tcisli310{ic}.t_ofbp   as  Sold_To_BP,
    tcisli310{ic}.t_dqua   as  Inv_Quantity,
    tcisli310{ic}.t_cuns   as  Qty_Unit,
    tcisli310{ic}.t_pric   as  Price,
    tcisli310{ic}.t_cups   as  Price_Unit,
    tcisli310{ic}.t_orno   as  Sales_O_S_N,
    tcisli310{ic}.t_item   as  Item,
    tcisli310{ic}.t_amti   as  Net_Line_Amount,
    tcisli305{ic}.t_idat   as  Inv_Date,
    tcisli310{ic}.t_stbp   as  Ship_To_BP,
    tcisli310{ic}.t_amth_1 as  Net_Line_Amount_HC    ,'TND'  as  HOME_CURRENCY,
    tcisli310{ic}.t_amth_2 as  Reporting_Amount_Euro ,'EUR'  as  Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3 as  Reporting_Amount_USD  ,'USD'  as  Reporting_Currency_USD,
    tcisli310{ic}.t_sfcp   as  Inv_Company,
    tcisli310{ic}.t_srcp   as  Sales_Company,
    tcisli310{ic}.t_shln   as  shipment_line,
    tcisli310{ic}.t_shpm   as  shipment,
    ''as warehouse,
    3 AS REQUEST,
    1 as Active,
    0 as confirmed,
    'Portugal' as region,
    
    (CASE WHEN tcisli310{ic}.t_srcp = 122 THEN 'M-122' 
          WHEN tcisli310{ic}.t_srcp = 127 THEN 'M-127'  END) as plant,
    
    (CASE WHEN tcisli310{ic}.t_cups in('km','KM','Km','kM') THEN 'FG' ELSE 'NFG' END) as TYPE_INVOICE

    FROM
    tcisli310{ic},
    tcisli305{ic}
    
    WHERE
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', {ic}) and CONVERT(DATETIME, '{End}', {ic})
    and tcisli310{ic}.t_orno not in (select ttdsls406{ic}.t_orno from ttdsls406{ic})
    and tcisli310{ic}.t_orno not in (select ttdsls406127.t_orno from ttdsls406127)
    and tcisli310{ic}.t_orno not in (select ttdsls406125.t_orno from ttdsls406125)

    and tcisli310{ic}.t_orno not in (select ttdsls340{ic}.t_schn from ttdsls340{ic})
    and tcisli310{ic}.t_orno not in (select ttdsls340127.t_schn from ttdsls340127)
    and tcisli310{ic}.t_orno not in (select ttdsls340125.t_schn from ttdsls340125)

    and tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
    tcisli305{ic}.t_stat=80
    """
    return pd.read_sql(text,cnx)
  


#
#

def extract_PT_localhost(tables,Start,End,cnx):
    text= f"""  
    SELECT * FROM {tables} 
    WHERE inv_date BETWEEN CONVERT(DATETIME, '{Start}', 102) AND CONVERT(DATETIME, '{End}', 102) 
    """
    return pd.read_sql(text,cnx)