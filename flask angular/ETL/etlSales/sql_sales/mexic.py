import pandas as pd
import numpy as np
#import xlrd
from io import RawIOBase
from contextlib import contextmanager


def extract_mx_1(plant,sc,Start,End,cnx): #sales shcedels

    text= f"""select 
    (
	cast(tcisli310{plant}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{plant}.t_idoc as char))+'-'+
    rtrim(cast(ttdsls340{sc}.t_dlno as char))+'-'+
    rtrim(cast(ttdsls340{sc}.t_shpo as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{sc}.t_mati))
			,cast (row_number() over(partition by tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc, ttdsls340{sc}.t_dlno ,ttdsls340{sc}.t_shpo
                                     order by     tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc, ttdsls340{sc}.t_dlno ,ttdsls340{sc}.t_shpo )as varchar(3))
			)
	) as id_line,

    tcisli310{plant}.t_tran as Trans_Type,
    tcisli310{plant}.t_idoc as Invoice_N,  
    tcisli305{plant}.t_ccur as Currency,  
    tcisli310{plant}.t_ofbp as Sold_To_BP,  
    ttccom100610.t_nama     as Desc_STPB, 
    tcisli310{plant}.t_dqua as Inv_Quantity,
    tcisli310{plant}.t_cuns as Qty_Unit ,
    --tcisli310{plant}.t_pric as Price , 
    tcisli310{plant}.t_cups as Price_Unit , 
    tcisli310{plant}.t_orno as Sales_O_S_N,
    ltrim(rtrim(tcisli310{plant}.t_item)) as Item  ,
    ttcibd001610.t_dsca     as Item_Description,
    tcisli310{plant}.t_amti as Net_Line_Amount,
    tcisli305{plant}.t_idat as Inv_Date,
    tcisli310{plant}.t_stbp as Ship_To_BP,
 
    ttdsls340{sc}.t_dlno as Shipment,
    ttdsls340{sc}.t_shpo as Shipment_line,
    ttcibd004{sc}.t_aitc as Part_Number,
    
    'North America' as region,
    tcisli310{plant}.t_amth_1 as Net_Line_Amount_HC,
    'HNL' as Home_Currency,
    tcisli310{plant}.t_amth_2 as Reporting_Amount_Euro,
    'EUR' as Reporting_Currency_Euro,
    tcisli310{plant}.t_amth_3 as Reporting_Amount_USD,
    'USD' as Reporting_Currency_USD,
    tcisli310{plant}.t_sfcp as Inv_Company,
    tcisli310{plant}.t_srcp as Sales_Company,
    ttdsls301{sc}.t_pric as Added_value,
    ttdsls301{sc}.t_cono as Contract_N,
    ttdsls301{sc}.t_cwar as warehouse,
    ttdmpv102{sc}.t_mprs as Mterial_Exchange,
    ttdmpv102{sc}.t_matf as Metal_weight_sales,
    ttdmpv102{sc}.t_mati as Material_Type,
    ttdmpv102{sc}.t_apri as Metal_Rate,
    case  when tcisli310{plant}.t_cups IN ('km','KM','Km') then 'FG' ELSE 'NFG' END as type_invoice,
    1 as request,
    0 as confirmed,
    1 as active
    
    FROM
    tcisli305{plant},            
    tcisli310{plant} left join ttcibd004{sc} on tcisli310{plant}.t_item=ttcibd004{sc}.t_item and ttcibd004{sc}.t_bpid=tcisli310{plant}.t_stbp ,
    ttccom100610,
    ttcibd001610,
    ttdsls340{sc} left join
    ttdsls321{sc}  
    left join ttdmpv102{sc} on
    ttdmpv102{sc}.t_orno=ttdsls321{sc}.t_schn and ttdmpv102{sc}.t_sqnb=ttdsls321{sc}.t_spon and ttdmpv102{sc}.t_pono=ttdsls321{sc}.t_revn 
    left join  ttdsls311{sc} 
    left join ttdsls301{sc} on ttdsls301{sc}.t_cono= ttdsls311{sc}.t_cono and ttdsls301{sc}.t_pono= ttdsls311{sc}.t_pono
    on ttdsls311{sc}.t_schn= ttdsls321{sc}.t_worn and ttdsls311{sc}.t_sctp=2 
    and ttdsls311{sc}.t_revn=ttdsls321{sc}.t_revn
    on ttdsls321{sc}.t_worn=ttdsls340{sc}.t_schn
    and ttdsls321{sc}.t_sctp=2 and ttdsls321{sc}.t_wsqn=ttdsls340{sc}.t_wsqn

    WHERE
    tcisli305{plant}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
    And tcisli310{plant}.t_ofbp = tcisli305{plant}.t_itbp 
    and tcisli310{plant}.t_idoc = tcisli305{plant}.t_idoc 
    and tcisli310{plant}.t_tran=tcisli305{plant}.t_tran 
    and ttcibd001610.t_item=tcisli310{plant}.t_item  
    and tcisli310{plant}.t_ofbp= ttccom100610.t_bpid 
    and tcisli310{plant}.t_idoc=ttdsls340{sc}.t_invn
    and tcisli310{plant}.t_tran=ttdsls340{sc}.t_ttyp
    and ttdsls340{sc}.t_schn=tcisli310{plant}.t_orno
    and tcisli310{plant}.t_shln=ttdsls340{sc}.t_shpo
    and ttdsls340{sc}.t_dlno=tcisli310{plant}.t_shpm
    """
    return  pd.read_sql(text, cnx)  
    


#####

def extract_mx_2(plant,sc,Start,End,cnx): #sales order"
    text= f"""Select 
    (
	cast(tcisli310{plant}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{plant}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{plant}.t_shpm as char))+'-'+
    rtrim(cast(tcisli310{plant}.t_shln as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{sc}.t_mati))
			,cast (row_number() over(partition by tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc, tcisli310{plant}.t_shpm ,tcisli310{plant}.t_shln 
                                     order by     tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc, tcisli310{plant}.t_shpm ,tcisli310{plant}.t_shln )as varchar(3))
			)
	) as id_line,

    tcisli310{plant}.t_tran  as  Trans_Type,
    tcisli310{plant}.t_idoc  as  Invoice_N,
    tcisli305{plant}.t_ccur  as  Currency,
    tcisli310{plant}.t_ofbp  as  Sold_To_BP,
    ttccom100610.t_nama  as  Desc_STPB,
    tcisli310{plant}.t_dqua  as  Inv_Quantity,
    tcisli310{plant}.t_cuns  as  Qty_Unit,
    tcisli310{plant}.t_pric  as  Price ,
    tcisli310{plant}.t_cups  as  Price_Unit ,
    tcisli310{plant}.t_orno  as  Sales_O_S_N,
    ltrim(rtrim(tcisli310{plant}.t_item))  as  Item,
    ttcibd001610.t_dsca  as  Item_Description,
    tcisli310{plant}.t_amti  as  Net_Line_Amount,
    tcisli305{plant}.t_idat  as  Inv_Date,
    tcisli310{plant}.t_stbp  as  Ship_To_BP,
    ''  as  Ship_To_Description,
    ttdmpv102{sc}.t_mprs  as  Mterial_Exchange,
    ttdmpv102{sc}.t_matf  as  Metal_weight_sales,
    ttdsls301{sc}.t_pric  as  Added_value,
    ttdmpv102{sc}.t_apri  as  Metal_Rate,
    ttdsls301{sc}.t_cono  as  Contract_N,
    tcisli310{plant}.t_shpm  as  shipment,
    tcisli310{plant}.t_shln  as  shipment_line,
    ttcibd004{sc}.t_aitc  as  Part_Number,
    'North America' as region,
    tcisli310{plant}.t_amth_1  as  Net_Line_Amount_HC,
    'HNL'  as  Home_Currency,
    tcisli310{plant}.t_amth_2  as  Reporting_Amount_Euro,
    'EUR'  as  Reporting_Currency_Euro,
    tcisli310{plant}.t_amth_3  as  Reporting_Amount_USD,
    'USD'  as  Reporting_Currency_USD,
    ttdmpv102{sc}.t_mati  as  Material_Type,
    tcisli310{plant}.t_sfcp  as  Inv_Company,
    tcisli310{plant}.t_srcp  as  Sales_Company,
    case  when tcisli310{plant}.t_cups IN ('km','KM','Km') then 'FG' ELSE 'NFG' END as type_invoice,
    ttdsls401{sc}.t_cwar  as  warehouse,
    2 as request, 
    1 as active,
    0 as confirmed
   , CASE ttdsls406{sc}.t_porg  WHEN 4 THEN 'Manual' WHEN 6 THEN 'Contract' END  as Price_Origine 
    ,tcisli305{plant}.t_stat as stat
    FROM
    tcisli305{plant}, ttdsls401{sc} 
    WITH (NOLOCK)
    left join ttdsls301{sc} on ttdsls301{sc}.t_cono=ttdsls401{sc}.t_cono and ttdsls401{sc}.t_cpon=ttdsls301{sc}.t_pono,
    ttdsls406{sc} left join ttdmpv102{sc} on ttdmpv102{sc}.t_orno=ttdsls406{sc}.t_orno and ttdmpv102{sc}.t_pono=ttdsls406{sc}.t_pono and ttdmpv102{sc}.t_sqnb=ttdsls406{sc}.t_sqnb 
                            and ttdmpv102{sc}.t_bpid= ttdsls406{sc}.t_stbp,
    tcisli310{plant} left join ttcibd004{sc} on tcisli310{plant}.t_item=ttcibd004{sc}.t_item and ttcibd004{sc}.t_bpid=tcisli310{plant}.t_stbp
    --ttcibd001610,
    --ttccom100610
    left join ttcibd001610 on ltrim(rtrim(ttcibd001610.t_item))=ltrim(rtrim(tcisli310{plant}.t_item)) 
	left join ttccom100610 on tcisli310{plant}.t_ofbp= ttccom100610.t_bpid
    WHERE
    tcisli305{plant}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}',102) and
    ttdsls406{sc}.t_pono=tcisli310{plant}.t_pono and
    tcisli310{plant}.t_ofbp = tcisli305{plant}.t_itbp and
    tcisli310{plant}.t_idoc = tcisli305{plant}.t_idoc and 
    tcisli305{plant}.t_stat in(5,6) and
    tcisli310{plant}.t_idoc=ttdsls406{sc}.t_invn and
    tcisli310{plant}.t_tran=ttdsls406{sc}.t_ttyp and
    ttdsls406{sc}.t_orno=tcisli310{plant}.t_orno and
    tcisli305{plant}.t_tran=ttdsls406{sc}.t_ttyp and
    --ttcibd001610.t_item=tcisli310{plant}.t_item and
    --tcisli310{plant}.t_ofbp= ttccom100610.t_bpid and 
    tcisli310{plant}.t_pono= ttdsls406{sc}.t_pono and 
    tcisli310{plant}.t_pono=ttdsls401{sc}.t_pono and 
    tcisli310{plant}.t_orno=ttdsls401{sc}.t_orno and 
    ttdsls401{sc}.t_sqnb=ttdsls406{sc}.t_sqnb and 
    tcisli310{plant}.t_tran=tcisli305{plant}.t_tran and 
    ttdsls406{sc}.t_shln=tcisli310{plant}.t_shln and 
    tcisli310{plant}.t_shpm=ttdsls406{sc}.t_shpm
    and tcisli305{plant}.t_stat in (5,6)
    
    """
    return  pd.read_sql(text, cnx)

####


def Manual_Sales_Envoice_mexico(plant,Start,End,cnx):# manual invoice
    text= f"""Select 
    (cast(tcisli310{plant}.t_srcp as char(3))
    +'-'
    + rtrim(cast(tcisli310{plant}.t_idoc as char))
    +'-'
    +cast (row_number() over(partition by tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc
                             order by    tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc )as varchar(3))
    
    +tcisli310{plant}.t_tran )as id_line,

    tcisli310{plant}.t_tran as Trans_Type ,
    tcisli310{plant}.t_idoc as  Invoice_N,
    tcisli305{plant}.t_ccur as  Currency,
    tcisli310{plant}.t_ofbp as  Sold_To_BP,
    tcisli310{plant}.t_dqua as  Inv_Quantity,
    tcisli310{plant}.t_cuns as  Qty_Unit,
    tcisli310{plant}.t_pric as  Price,
    tcisli310{plant}.t_cups as  Price_Unit,
    tcisli310{plant}.t_orno as Sales_O_S_N,
    (CASE WHEN rtrim(ltrim(tcisli310{plant}.t_item)) ='' then 'Manual' else rtrim(ltrim(tcisli310{plant}.t_item)) END  ) as  Item,
    tcisli310{plant}.t_amti as  Net_Line_Amount,
    tcisli305{plant}.t_idat as  Inv_Date,
    tcisli310{plant}.t_stbp as  Ship_To_BP,
    tcisli310{plant}.t_amth_1 as  Net_Line_Amount_HC,
    tcisli310{plant}.t_amth_2 as  Reporting_Amount_Euro,
    tcisli310{plant}.t_amth_3 as  Reporting_Amount_USD,
    tcisli310{plant}.t_sfcp as  Inv_Company,
    tcisli310{plant}.t_srcp as  Sales_Company,
    'M-'+CAST(tcisli310{plant}.t_srcp as char) as  plant,
    tcisli310{plant}.t_shln as  shipment_line,
    tcisli310{plant}.t_shpm as  shipment,
    'North America' as region,
    'HNL'  as  Home_Currency,
    'EUR'  as  Reporting_Currency_Euro,
    'USD'  as  Reporting_Currency_USD,
    3 as request, 
    1 as active,
    0 as confirmed,
    'NFG' as TYPE_INVOICE,

    'M-'+cast(tcisli310{plant}.t_srcp as char) as Sales_Company_Dsc,
    'Manual Sales invoice_'+cast(tcisli310{plant}.t_srcp as char) as INV_Company_DESC
    ,tcisli305{plant}.t_stat as stat

    FROM
    tcisli310{plant},tcisli305{plant}
        
    WHERE
    tcisli305{plant}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) 
	and tcisli310{plant}.t_orno not in (select ttdsls406630.t_orno from ttdsls406630) 
	and tcisli310{plant}.t_orno not in (select ttdsls406640.t_orno from ttdsls406640)  

	and tcisli310{plant}.t_orno not in (select ttdsls340630.t_schn from ttdsls340630) 
	and tcisli310{plant}.t_orno not in (select ttdsls340640.t_schn from ttdsls340640) 

	and tcisli310{plant}.t_ofbp = tcisli305{plant}.t_itbp 
	and tcisli310{plant}.t_idoc = tcisli305{plant}.t_idoc 
    and tcisli310{plant}.t_tran = tcisli305{plant}.t_tran
	and tcisli305{plant}.t_stat in (5,6)

    """
    #print (text)
    return pd.read_sql(text,cnx)
####

def Manual_Sales_Envoice_mexico_sp(plant,Start,End,cnx):# manual invoice
   
    text= f"""Select 
   (cast(tcisli310{plant}.t_srcp as char(3))
    +'-'
    + rtrim(cast(tcisli310{plant}.t_idoc as char))
    +'-'
    +cast (row_number() over(partition by tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc
                             order by    tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc )as varchar(3))
    
    +tcisli310{plant}.t_tran )as id_line,

    tcisli310{plant}.t_tran as Trans_Type ,
    tcisli310{plant}.t_idoc as  Invoice_N,
    tcisli305{plant}.t_ccur as  Currency,
    tcisli310{plant}.t_ofbp as  Sold_To_BP,
    tcisli310{plant}.t_dqua as  Inv_Quantity,
    tcisli310{plant}.t_cuns as  Qty_Unit,
    tcisli310{plant}.t_pric as  Price,
    tcisli310{plant}.t_cups as  Price_Unit,
    tcisli310{plant}.t_orno as Sales_O_S_N,
    (CASE WHEN rtrim(ltrim(tcisli310{plant}.t_item)) ='' then 'Manual' else rtrim(ltrim(tcisli310{plant}.t_item)) END  ) as  Item,
    tcisli310{plant}.t_amti as  Net_Line_Amount,
    tcisli305{plant}.t_idat as  Inv_Date,
    tcisli310{plant}.t_stbp as  Ship_To_BP,
    tcisli310{plant}.t_amth_1 as  Net_Line_Amount_HC,
    tcisli310{plant}.t_amth_2 as  Reporting_Amount_Euro,
    tcisli310{plant}.t_amth_3 as  Reporting_Amount_USD,
    tcisli310{plant}.t_sfcp as  Inv_Company,
    tcisli310{plant}.t_srcp as  Sales_Company,
    'M-'+CAST(tcisli310{plant}.t_srcp as char) as  plant,
    tcisli310{plant}.t_shln as  shipment_line,
    tcisli310{plant}.t_shpm as  shipment,
    'North America' as region,
    'HNL'  as  Home_Currency,
    'EUR'  as  Reporting_Currency_Euro,
    'USD'  as  Reporting_Currency_USD,
    3 as request, 
    1 as active,
    0 as confirmed,
    'NFG' as TYPE_INVOICE,
    '' as warehouse,
    'M-'+cast(tcisli310{plant}.t_srcp as char) as Sales_Company_Dsc,
    'Manual Sales invoice_'+cast(tcisli310{plant}.t_srcp as char) as INV_Company_DESC
    ,tcisli305{plant}.t_stat as stat
   
    
    FROM

    tcisli310{plant},tcisli305{plant}
        
    WHERE

    tcisli305{plant}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) 
	and tcisli310{plant}.t_orno not in (select ttdsls406660.t_orno from ttdsls406660 WHERE ttdsls406660.t_ttyp= tcisli310660.t_tran and ttdsls406660.t_invn=tcisli310660.t_idoc) 
	and tcisli310{plant}.t_orno not in (select ttdsls340660.t_schn from ttdsls340660 WHERE ttdsls340660.t_ttyp= tcisli305660.t_tran  and ttdsls340660.t_invn=tcisli310660.t_idoc)

    and tcisli310{plant}.t_tran = tcisli305{plant}.t_tran 
	and tcisli310{plant}.t_ofbp = tcisli305{plant}.t_itbp 
	and tcisli310{plant}.t_idoc = tcisli305{plant}.t_idoc 
	and tcisli305{plant}.t_stat in (5,6)

    """
    #print (text)
    return pd.read_sql(text,cnx)
###