

import pandas as pd
#import xlrd
from io import RawIOBase
from contextlib import contextmanager


def extract_mx_exception(ic,sc,Start,End,cnx): #sales shcedels
    text= f"""
    Select 
   (
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shpm as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shln as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{sc}.t_mati))
			,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln 
                                     order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln )as varchar(3))
			)
	) as id_line,

    tcisli310{ic}.t_tran  as  Trans_Type,
    tcisli310{ic}.t_idoc  as  Invoice_N,
    tcisli305{ic}.t_ccur  as  Currency,
    tcisli310{ic}.t_ofbp  as  Sold_To_BP,
    ttccom100{ic}.t_nama  as  Desc_STPB,
    tcisli310{ic}.t_dqua  as  Inv_Quantity,
    tcisli310{ic}.t_cuns  as  Qty_Unit,
    tcisli310{ic}.t_pric  as  Price ,
    tcisli310{ic}.t_cups  as  Price_Unit ,
    tcisli310{ic}.t_orno  as  Sales_O_S_N,
    tcisli310{ic}.t_item  as  Item,
    ttcibd001{ic}.t_dsca  as  Item_Description,
    tcisli310{ic}.t_amti  as  Net_Line_Amount,
    tcisli305{ic}.t_idat  as  Inv_Date,
    tcisli310{ic}.t_stbp  as  Ship_To_BP,
    ''  as  Ship_To_Description,
    ttdmpv102{sc}.t_mprs  as  Mterial_Exchange,
    ttdmpv102{sc}.t_matf  as  Metal_weight_sales,
    ttdsls301{sc}.t_pric  as  Added_value,
   
    ttdmpv102{sc}.t_apri  as  Metal_Rate,
    ttdsls301{sc}.t_cono  as  Contract_N,
    tcisli310{ic}.t_shpm  as  shipment,
    tcisli310{ic}.t_shln  as  shipment_line,
    ttcibd004{sc}.t_aitc  as  Part_Number,

    'North America' as region,
    tcisli310{ic}.t_amth_1  as  Net_Line_Amount_HC,
    'HNL'  as  Home_Currency,
    tcisli310{ic}.t_amth_2  as  Reporting_Amount_Euro,
    'EUR'  as  Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3  as  Reporting_Amount_USD,
    'USD'  as  Reporting_Currency_USD,
    ttdmpv102{sc}.t_mati  as  Material_Type,
    tcisli310{ic}.t_sfcp  as  Inv_Company,
    tcisli310{ic}.t_srcp  as  Sales_Company,
    case  when tcisli310{ic}.t_cups IN ('km','KM','Km') then 'FG' ELSE 'NFG' END as type_invoice,
    ttdsls401{sc}.t_cwar  as  warehouse,
    4 as request, 
    1 as active,
    0 as confirmed
    
    FROM
    tcisli305{ic}, ttdsls401{sc} 
    WITH (NOLOCK)
    left join ttdsls301{sc} on ttdsls301{sc}.t_cono=ttdsls401{sc}.t_cono and ttdsls401{sc}.t_cpon=ttdsls301{sc}.t_pono
    
    ,ttdsls406{sc} 
    left join ttdmpv102{sc} on ttdmpv102{sc}.t_orno=ttdsls406{sc}.t_orno and ttdmpv102{sc}.t_pono=ttdsls406{sc}.t_pono and ttdmpv102{sc}.t_sqnb=ttdsls406{sc}.t_sqnb
    
    ,tcisli310{ic} 
    left join ttcibd004{sc} on tcisli310{ic}.t_item=ttcibd004{sc}.t_item and ttcibd004{sc}.t_bpid=tcisli310{ic}.t_stbp
    
    left join ttcibd001{ic} on ltrim(rtrim(ttcibd001{ic}.t_item)) = ltrim(rtrim(tcisli310{ic}.t_item)) 
	left join ttccom100{ic} on tcisli310{ic}.t_ofbp = ttccom100{ic}.t_bpid
    
    WHERE

    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}',102) and
    ttdsls406{sc}.t_pono=tcisli310{ic}.t_pono and
    tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and
    tcisli310{ic}.t_idoc=ttdsls406{sc}.t_invn and 
    tcisli310{ic}.t_tran=ttdsls406{sc}.t_ttyp and
    ttdsls406{sc}.t_orno=tcisli310{ic}.t_orno and
    tcisli305{ic}.t_tran=ttdsls406{sc}.t_ttyp and 
    tcisli305{ic}.t_stat in (5,6) and

    tcisli310{ic}.t_pono=ttdsls401{sc}.t_pono  
    and  tcisli310{ic}.t_orno=ttdsls401{sc}.t_orno 
    and ttdsls401{sc}.t_sqnb=ttdsls406{sc}.t_sqnb 
	

	and ttdsls406{sc}.t_rcln = tcisli310{ic}.t_shln
	and ttdsls406{sc}.t_rcid=tcisli310{ic}.t_shpm

    and ttdsls406{sc}.t_shln<>tcisli310{ic}.t_shln 
    and tcisli310{ic}.t_shpm<>ttdsls406{sc}.t_shpm
    
    
    and tcisli305{ic}.t_stat in (5,6)
    
    """
    return  pd.read_sql(text, cnx)  

def extract_CHINE_exception(ic,Start,End,cnx): #sales order
    text= f"""
    Select
     (
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shpm as char))+'-'+
    rtrim(cast( tcisli310{ic}.t_shln as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{ic}.t_mati+'-'+  cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln
                                     order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln )as varchar(3))))
			,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln
                                     order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,tcisli310{ic}.t_shln )as varchar(3))
			)
	) as id_line,
	
    tcisli310{ic}.t_tran  as  Trans_Type,
    tcisli310{ic}.t_idoc  as  Invoice_N,
    tcisli305{ic}.t_ccur  as  Currency,
    tcisli310{ic}.t_ofbp  as  Sold_To_BP,
    ttccom100502.t_nama   as  Desc_STPB,
    tcisli310{ic}.t_dqua  as  Inv_Quantity,
    tcisli310{ic}.t_cuns  as  Qty_Unit,
    tcisli310{ic}.t_pric  as  Price ,
    tcisli310{ic}.t_cups  as  Price_Unit ,
    tcisli310{ic}.t_orno  as  Sales_O_S_N,
    ltrim(tcisli310{ic}.t_item)  as  Item,
    ttcibd001{ic}.t_dsca  as  Item_Description,
    tcisli310{ic}.t_amti  as  Net_Line_Amount,
    tcisli305{ic}.t_idat  as  Inv_Date,
    tcisli310{ic}.t_stbp  as  Ship_To_BP,
    ''                    as  Ship_To_Description,
    ttdmpv102{ic}.t_mprs  as  Mterial_Exchange,
    ttdmpv102{ic}.t_matf  as  Metal_weight_sales,
    ttdsls301{ic}.t_pric  as  Added_value,
    
    ttdmpv102{ic}.t_apri  as  Metal_Rate,
    ttdsls301{ic}.t_cono  as  Contract_N,
    tcisli310{ic}.t_shpm  as  shipment,
    tcisli310{ic}.t_shln  as  shipment_line,
    ttcibd004{ic}.t_aitc  as  Part_Number,
    case  tcisli310{ic}.t_sfcp when  153 then 'COF TT' when {ic} then 'COF TJ' END  as plant,
    
    tcisli310{ic}.t_amth_1  as  Net_Line_Amount_HC,
    'CNY'  as  Home_Currency,
    tcisli310{ic}.t_amth_2  as  Reporting_Amount_Euro,
    'EUR'  as  Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3  as  Reporting_Amount_USD,
    'USD'  as  Reporting_Currency_USD,
    ttdmpv102{ic}.t_mati  as  Material_Type,
    tcisli310{ic}.t_sfcp  as  Inv_Company,
    tcisli310{ic}.t_srcp  as  Sales_Company,
    case  when tcisli310{ic}.t_cups IN ('km','KM','Km') then 'FG' ELSE 'NFG' END as type_invoice,
    ttdsls401{ic}.t_cwar  as  warehouse,
    4 as request, 1 as active,0 as confirmed
    
    FROM
    tcisli305{ic}, ttdsls401{ic}
    WITH (NOLOCK)
    left join ttdsls301{ic} on ttdsls301{ic}.t_cono=ttdsls401{ic}.t_cono and ttdsls401{ic}.t_cpon=ttdsls301{ic}.t_pono,
    ttdsls406{ic} left join ttdmpv102{ic} on ttdmpv102{ic}.t_orno=ttdsls406{ic}.t_orno and ttdmpv102{ic}.t_pono=ttdsls406{ic}.t_pono and ttdmpv102{ic}.t_sqnb=ttdsls406{ic}.t_sqnb ,
    tcisli310{ic} left join ttcibd004{ic} on tcisli310{ic}.t_item=ttcibd004{ic}.t_item and ttcibd004{ic}.t_bpid=tcisli310{ic}.t_stbp,
    ttcibd001{ic},
    ttccom100502

    where

    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}',102) and
    ttdsls406{ic}.t_pono = tcisli310{ic}.t_pono and
    tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and
    tcisli305{ic}.t_stat= 6 and
    tcisli310{ic}.t_idoc=ttdsls406{ic}.t_invn and
    tcisli310{ic}.t_tran=ttdsls406{ic}.t_ttyp and
    ttdsls406{ic}.t_orno=tcisli310{ic}.t_orno and
    tcisli305{ic}.t_tran=ttdsls406{ic}.t_ttyp and
    ttcibd001{ic}.t_item=tcisli310{ic}.t_item and
    tcisli310{ic}.t_ofbp= ttccom100502.t_bpid and
    tcisli310{ic}.t_pono= ttdsls406{ic}.t_pono and
    tcisli310{ic}.t_pono=ttdsls401{ic}.t_pono and
    tcisli310{ic}.t_orno=ttdsls401{ic}.t_orno and
    ttdsls401{ic}.t_sqnb=ttdsls406{ic}.t_sqnb 
    --ttdsls406{ic}.t_shln=tcisli310{ic}.t_shln and
    --tcisli310{ic}.t_shpm=ttdsls406{ic}.t_shpm
	and ttdsls406{ic}.t_rcln = tcisli310{ic}.t_shln
	and ttdsls406{ic}.t_rcid = tcisli310{ic}.t_shpm
    and ttdsls406{ic}.t_rcid <>''  
    and ttdsls406{ic}.t_rcid is not null  
    """
    return  pd.read_sql(text, cnx)  

def extract_tn_exception(ic,Start,End,cnx): #sales order
    text= f"""
   select
    
    (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
    cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(ttdsls406{ic}.t_shpm as char))+'-'+
    rtrim(cast(ttdsls406{ic}.t_shln as char))+'-'+  
    isnull(rtrim(ltrim(ttcmpr110{ic}.t_matr +'-'+ 
				cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln,ttcmpr110{ic}.t_matr
                                        order by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln,ttcmpr110{ic}.t_matr )as varchar(3))))
                ,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln
                                        order by       tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln )as varchar(3))
                        )


        ) as id_line,

    tcisli310{ic}.t_tran  as  Trans_Type,
    tcisli310{ic}.t_idoc  as  Invoice_N,
    tcisli305{ic}.t_ccur  as  Currency,
    tcisli310{ic}.t_ofbp  as  Sold_To_BP, 
    ttccom100100.t_nama   as  Desc_STPB,
    tcisli310{ic}.t_dqua  as  Inv_Quantity,
    tcisli310{ic}.t_cuns  as  Qty_Unit ,
    tcisli310{ic}.t_pric  as  Price , 
    tcisli310{ic}.t_cups  as  Price_Unit , 
    tcisli310{ic}.t_orno  as  Sales_O_S_N,
    tcisli310{ic}.t_item  as  Item ,
    ttcibd001100.t_dsca      as  Item_Description,
    tcisli310{ic}.t_amti  as  Net_Line_Amount,
    tcisli305{ic}.t_idat  as  Inv_Date,
    tcisli310{ic}.t_stbp  as  Ship_To_BP,
    '' as  Ship_To_Description,
    
    ttcmpr100{ic}.t_mtex as  Mterial_Exchange,
    ttcmpr110{ic}.t_qmct as  Metal_weight_sales,
    ttdsls301{ic}.t_pric  as  Added_value,
    ttcmpr110{ic}.t_acpr as  Metal_Rate,

    ttdsls301{ic}.t_cono  as  Contract_N,
    ttdsls406{ic}.t_shpm  as  shipment,
    ttdsls406{ic}.t_shln  as  shipment_line, 
    ttcibd004{ic}.t_aitc  as  part_number,
    tcisli310{ic}.t_amth_1  as  Net_Line_Amount_HC    ,'TND'  as  HOME_CURRENCY,
    tcisli310{ic}.t_amth_2  as  Reporting_Amount_Euro ,'EUR'  as  Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3  as  Reporting_Amount_USD  ,'USD'  as  Reporting_Currency_USD,
    ttcmpr110{ic}.t_matr  as  Material_Type,
    tcisli310{ic}.t_sfcp  as  Inv_Company,
    tcisli310{ic}.t_srcp  as  Sales_Company,
    'Tunisia' as region,
    CASE when tcisli310{ic}.t_srcp = 102 then 'COF TN' when tcisli310{ic}.t_srcp = 104 THEN 'COF MED'   END as plant,
    ''as warehouse,
    4 as request  ,
    0 as confirmed,
    1 as Active,
    (case  when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) as TYPE_INVOICE

    from
    tcisli305{ic},
    
    tcisli310{ic} tcisli310{ic} LEFT JOIN ttcibd004{ic} ON  ttcibd004{ic}.t_bpid=tcisli310{ic}.t_stbp 
	                  and ltrim(rtrim(tcisli310{ic}.t_item))=ltrim(rTRIM(ttcibd004{ic}.t_item )),
    ttccom100100 ,
    ttcibd001100,
    ttdsls406{ic} left join ttcmpr100{ic} left join ttcmpr110{ic} on
    ttcmpr110{ic}.t_bobj=ttcmpr100{ic}.t_bobj and
    ttcmpr100{ic}.t_borf=ttcmpr110{ic}.t_borf

    on ttcmpr100{ic}.t_bobj=ttdsls406{ic}.t_orno and ttcmpr100{ic}.t_borf=concat( ttdsls406{ic}.t_pono ,'/',ttdsls406{ic}.t_sqnb,'/',ttdsls406{ic}.t_dsqn,'/',ttdsls406{ic}.t_invl),
    ttdsls401{ic} left join ttdsls301{ic} on ttdsls301{ic}.t_cono=ttdsls401{ic}.t_cono and ttdsls401{ic}.t_cpon=ttdsls301{ic}.t_pono

    WHERE
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) and
    tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
    tcisli305{ic}.t_stat=80 and
    ttcibd001100.t_item=tcisli310{ic}.t_item and
    tcisli310{ic}.t_ofbp= ttccom100100.t_bpid and
    tcisli310{ic}.t_idoc=ttdsls406{ic}.t_invn and
    tcisli310{ic}.t_tran=ttdsls406{ic}.t_ttyp and
    ttdsls406{ic}.t_orno=tcisli310{ic}.t_orno and
    ttdsls406{ic}.t_pono=tcisli310{ic}.t_pono and
   

    ttdsls401{ic}.t_pono=ttdsls406{ic}.t_pono 
	and ttdsls401{ic}.t_ofbp=tcisli310{ic}.t_ofbp 
	and ttdsls401{ic}.t_item=tcisli310{ic}.t_item 
	and ttdsls401{ic}.t_sqnb=ttdsls406{ic}.t_sqnb 
	and ttdsls401{ic}.t_orno=ttdsls406{ic}.t_orno


	and ttdsls406{ic}.t_rcln = tcisli310{ic}.t_shln
	and ttdsls406{ic}.t_rcid = tcisli310{ic}.t_shpm
    and ttdsls406{ic}.t_rcid <>''  
    and ttdsls406{ic}.t_rcid is not null  
    
    """
   #print(text)
    return  pd.read_sql(text, cnx)  

def extract_pt_exception(ic,sc,Start,End,cnx):
    text= f"""
    select
    ('E_'+
    cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
    cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    --rtrim(cast(ttdsls406{sc}.t_shpm as char))+'-'+
    rtrim(cast(ttdsls406{sc}.t_shln as char))+'-'+  
    --isnull(rtrim(ltrim(ttcmpr110{sc}.t_matr ))
        cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln
                                    order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln )as varchar(3))
            --+'-'+  
            --cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm,tcisli310{ic}.t_item ,ttdsls406{sc}.t_shln
    --                                 order by    tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,tcisli310{ic}.t_item ,ttdsls406{sc}.t_shln)as varchar(3))
    ) as id_line,
        
    tcisli310{ic}.t_tran  as  Trans_Type,
    tcisli310{ic}.t_idoc  as  Invoice_N,
    tcisli305{ic}.t_ccur  as  Currency,
    tcisli310{ic}.t_ofbp  as  Sold_To_BP,
    ttccom100100.t_nama  as  Desc_STPB,
    sum(tcisli310{ic}.t_dqua)  as  Inv_Quantity,
    tcisli310{ic}.t_cuns  as  Qty_Unit ,
    tcisli310{ic}.t_pric  as  Price,
    tcisli310{ic}.t_cups  as  Price_Unit ,
    tcisli310{ic}.t_orno  as  Sales_O_S_N,
    tcisli310{ic}.t_item  as  Item ,
    ttcibd001100.t_dsca  as  Item_Description,
    sum(tcisli310{ic}.t_amti)  as  Net_Line_Amount,
    tcisli305{ic}.t_idat  as  Inv_Date ,
    tcisli310{ic}.t_stbp  as  Ship_To_BP,
    ''                   as  Ship_To_Description,
    ttcmpr100{sc}.t_mtex     as  Mterial_Exchange,
    ttcmpr110{sc}.t_qmct     as  Metal_weight_sales,
    ttdsls301{sc}.t_pric     as  Added_value,
    ttcmpr110{sc}.t_acpr     as  Metal_Rate,

    ttdsls301{sc}.t_cono     as  Contract_N,
    ttdsls406{sc}.t_shpm     as  shipment,
    ttdsls406{sc}.t_shln     as  shipment_line,
    ttcibd004{sc}.t_aitc     as  part_number,

    (CASE   when (tcisli310{ic}.t_srcp = {ic} AND tcisli310{ic}.t_sfcp = {ic})  then 'COF PT' 
            when (tcisli310{ic}.t_srcp = {ic} AND tcisli310{ic}.t_sfcp = 127)  then 'COF HG'
            when (tcisli310{ic}.t_srcp = {sc} AND tcisli310{ic}.t_sfcp = {ic})  then 'COF GR'
                
        END)     as plant,
        
        
    'Portugal' as region,

    sum(tcisli310{ic}.t_amth_1)  as  Net_Line_Amount_HC    ,'EUR'  as  HOME_CURRENCY,
    sum(tcisli310{ic}.t_amth_2)  as  Reporting_Amount_Euro ,'EUR'  as  Reporting_Currency_Euro,
    sum(tcisli310{ic}.t_amth_3)  as  Reporting_Amount_USD  ,'USD'  as  Reporting_Currency_USD,
    ttcmpr110{sc}.t_matr as  Material_Type,
    tcisli310{ic}.t_sfcp as  Inv_Company,
    tcisli310{ic}.t_srcp as  Sales_Company,
    '' as  warehouse
    ,4 as request
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
    (tcisli305{ic}.t_idat)  between (CONVERT(DATETIME, '{Start}', 102)) and  (CONVERT(DATETIME, '{End}', 102)) and
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
    --tcisli310{ic}.t_shln= ttdsls406{sc}.t_shln and
    --tcisli310{ic}.t_shpm= ttdsls406{sc}.t_shpm and
    ttdsls401{sc}.t_pono= ttdsls406{sc}.t_pono and 
    ttdsls401{sc}.t_ofbp= tcisli310{ic}.t_ofbp and 
    ttdsls401{sc}.t_item= tcisli310{ic}.t_item and 
    ttdsls401{sc}.t_sqnb= ttdsls406{sc}.t_sqnb and 
    ttdsls401{sc}.t_orno= ttdsls406{sc}.t_orno
        
    and ttdsls406{sc}.t_rcln = tcisli310{ic}.t_shln
    and ttdsls406{sc}.t_rcid=tcisli310{ic}.t_shpm
    and ttdsls406{sc}.t_shln<>tcisli310{ic}.t_shln 
    and tcisli310{ic}.t_shpm<>ttdsls406{sc}.t_shpm
    
    group by 

    tcisli310{ic}.t_tran ,tcisli310{ic}.t_idoc ,tcisli305{ic}.t_ccur,tcisli310{ic}.t_ofbp ,ttccom100100.t_nama,
    tcisli310{ic}.t_cuns ,tcisli310{ic}.t_pric  ,tcisli310{ic}.t_cups  ,tcisli310{ic}.t_orno  ,tcisli310{ic}.t_item  ,ttcibd001100.t_dsca ,tcisli305{ic}.t_idat ,tcisli310{ic}.t_stbp ,
    ttcmpr100{sc}.t_mtex,ttcmpr110{sc}.t_qmct,ttdsls301{sc}.t_pric,ttcmpr110{sc}.t_acpr,ttdsls301{sc}.t_cono,ttdsls406{sc}.t_shpm,ttdsls406{sc}.t_shln  ,ttcibd004{sc}.t_aitc ,
    (CASE   when (tcisli310{ic}.t_srcp = {ic} AND tcisli310{ic}.t_sfcp = {ic})  then 'COF PT' 
            when (tcisli310{ic}.t_srcp = {ic} AND tcisli310{ic}.t_sfcp = 127)  then 'COF HG'
            when (tcisli310{ic}.t_srcp = {sc} AND tcisli310{ic}.t_sfcp = {ic})  then 'COF GR'END)  ,
    ttcmpr110{sc}.t_matr ,tcisli310{ic}.t_sfcp ,tcisli310{ic}.t_srcp ,
    (case  when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) 


    order by 
        (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+cast(tcisli310{ic}.t_srcp as char(3))+'-'+rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
        rtrim(cast(ttdsls406{sc}.t_shln as char))+'-'+ 
        cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln
        order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{sc}.t_shpm ,ttdsls406{sc}.t_shln )as varchar(3)))
        
        """  
    #print(text)
    return  pd.read_sql(text, cnx)  
