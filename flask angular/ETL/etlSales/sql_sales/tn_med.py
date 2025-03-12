import pandas as pd
import pandas as pd
import numpy as np
#purchase

def extract_tn_md_prod_1(ic,Start,End,cnx):#sales schedel
    text= f"""select
    (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shpm as char))+'-'+
    rtrim(cast(tcisli310{ic}.t_shln as char))+'-'+ 
    isnull(rtrim(ltrim(ttcmpr110{ic}.t_matr)),cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm ,ttdsls340{ic}.t_shpo 
    order by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, tcisli310{ic}.t_shpm,ttdsls340{ic}.t_shpo )as varchar(3)))
    ) as id_line,
    tcisli310{ic}.t_tran as Trans_Type,
    tcisli310{ic}.t_idoc as Invoice_N,  
    tcisli305{ic}.t_ccur as Currency,
    tcisli310{ic}.t_ofbp as Sold_To_BP, 
    ttccom100100.t_nama as Desc_STPB,
    tcisli310{ic}.t_dqua as Inv_Quantity,
    tcisli310{ic}.t_cuns as Qty_Unit ,
    tcisli310{ic}.t_pric as Price , 
    tcisli310{ic}.t_cups as Price_Unit , 
    tcisli310{ic}.t_orno as Sales_O_S_N,
    tcisli310{ic}.t_item as Item ,
    ttcibd001100.t_dsca as Item_Description,
    tcisli310{ic}.t_amti as Net_Line_Amount,
    tcisli305{ic}.t_idat as Inv_Date,
    tcisli310{ic}.t_stbp as Ship_To_BP,
    ttdsls340{ic}.t_schn as Ship_To_Description,
	ttcmpr100{ic}.t_mtex as Mterial_Exchange,
	ttcmpr110{ic}.t_qmct as Metal_weight_sales,
	ttdsls301{ic}.t_pric as Added_value,
	ttcmpr110{ic}.t_acpr as Metal_Rate,
	ttdsls301{ic}.t_cono as Contract_N,
    ttdsls340{ic}.t_dlno as shipment,
    ttdsls340{ic}.t_shpo as shipment_line, 
    ttcibd004{ic}.t_aitc as part_number,
    'Tunisia' as region,
    CASE when tcisli310{ic}.t_srcp = 102 then 'COF TN' when tcisli310{ic}.t_srcp = 104 THEN 'COF MED'  when tcisli310{ic}.t_srcp = 105 THEN 'COF SARL' END as plant,
    tcisli310{ic}.t_amth_1 as Net_Line_Amount_HC,'TND' as HOME_CURRENCY,
    tcisli310{ic}.t_amth_2 as Reporting_Amount_Euro,'EUR' as Reporting_Currency_Euro,
    tcisli310{ic}.t_amth_3 as Reporting_Amount_USD,'USD' as Reporting_Currency_USD,
	ttcmpr110{ic}.t_matr as Material_Type,
	tcisli310{ic}.t_sfcp as Inv_Company,
    tcisli310{ic}.t_srcp as Sales_Company,
	''as warehouse,
    1 as request  ,
    0 as confirmed,
    1 as Active,
    (case  when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) as TYPE_INVOICE
   
   
    FROM

    tcisli305{ic},
    tcisli310{ic} tcisli310{ic} LEFT JOIN ttcibd004{ic} ON  ttcibd004{ic}.t_bpid=tcisli310{ic}.t_stbp 
	                  and ltrim(rtrim(tcisli310{ic}.t_item))=ltrim(rTRIM(ttcibd004{ic}.t_item )),
    ttccom100100 ,
    ttcibd001100,
    ttdsls340{ic} left join ttcmpr100{ic}
                                    left join ttcmpr110{ic} on ttcmpr110{ic}.t_bobj=ttcmpr100{ic}.t_bobj and ttcmpr100{ic}.t_borf=ttcmpr110{ic}.t_borf
                                    on ttcmpr100{ic}.t_borf=concat( ttdsls340{ic}.t_spon ,'/',ttdsls340{ic}.t_wpon,'/',ttdsls340{ic}.t_wsqn,'/',ttdsls340{ic}.t_seqn,'/',ttdsls340{ic}.t_invl) and
    ttcmpr100{ic}.t_bobj=concat( ttdsls340{ic}.t_schn,'/',ttdsls340{ic}.t_sctp ,'/',ttdsls340{ic}.t_revn) ,
    ttdsls301{ic},
    ttdsls311{ic},
    ttdsls321{ic}

    WHERE
   
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
    and tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp 
    and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc 
    and ttcibd001100.t_item=tcisli310{ic}.t_item 
    and tcisli310{ic}.t_ofbp= ttccom100100.t_bpid
    and tcisli310{ic}.t_idoc=ttdsls340{ic}.t_invn
    and tcisli310{ic}.t_tran=ttdsls340{ic}.t_ttyp
    and tcisli310{ic}.t_tran=tcisli305{ic}.t_tran 
    and ttdsls340{ic}.t_schn=tcisli310{ic}.t_orno
    and tcisli310{ic}.t_shln=ttdsls340{ic}.t_shpo
    and ttdsls340{ic}.t_dlno=tcisli310{ic}.t_shpm
    and ttdsls321{ic}.t_worn=ttdsls340{ic}.t_schn 
    and ttdsls321{ic}.t_sctp=2 and ttdsls321{ic}.t_wsqn=ttdsls340{ic}.t_wsqn 
    and ttdsls311{ic}.t_schn=ttdsls340{ic}.t_schn and ttdsls311{ic}.t_revn=ttdsls321{ic}.t_revn and ttdsls311{ic}.t_sctp=2
    and ttdsls311{ic}.t_cono=ttdsls301{ic}.t_cono and ttdsls301{ic}.t_pono=ttdsls311{ic}.t_pono

   
    """
    #print(text)
    return  pd.read_sql(text, cnx)
   

#
def extract_tn_md_prod_2(ic,Start,End,cnx):#sales order#

    text= f"""select
    
    (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'+
    rtrim(cast(ttdsls406{ic}.t_shpm as char))+'-'+
    rtrim(cast(ttdsls406{ic}.t_shln as char))+'-'+  
	isnull(rtrim(ltrim(ttcmpr110{ic}.t_matr ))
		,cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln
                                 order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc, ttdsls406{ic}.t_shpm ,ttdsls406{ic}.t_shln )as varchar(3))
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
    CASE when tcisli310{ic}.t_srcp = 102 then 'COF TN' when tcisli310{ic}.t_srcp = 104 THEN 'COF MED' when tcisli310{ic}.t_srcp = 105 THEN 'COF SARL'  END as plant,
    ''as warehouse,
    2 as request  ,
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
    tcisli310{ic}.t_tran=tcisli305{ic}.t_tran and
    
    ttdsls406{ic}.t_orno=tcisli310{ic}.t_orno and
    ttdsls406{ic}.t_pono=tcisli310{ic}.t_pono and
    tcisli310{ic}.t_shln=ttdsls406{ic}.t_shln and
    tcisli310{ic}.t_shpm=ttdsls406{ic}.t_shpm and

    ttdsls401{ic}.t_pono=ttdsls406{ic}.t_pono and ttdsls401{ic}.t_ofbp=tcisli310{ic}.t_ofbp and ttdsls401{ic}.t_item=tcisli310{ic}.t_item and ttdsls401{ic}.t_sqnb=ttdsls406{ic}.t_sqnb and ttdsls401{ic}.t_orno=ttdsls406{ic}.t_orno
    
    """
    return  pd.read_sql(text, cnx)

# 
def Manual_Sales_Invoice(ic,Start,End,cnx):#
    text= f"""select

    (cast(tcisli310{ic}.t_sfcp as char(3))+'-'+
    cast(tcisli310{ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{ic}.t_idoc as char))+'-'
	+cast (row_number() over(partition by tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc
                             order by     tcisli310{ic}.t_srcp,tcisli310{ic}.t_idoc)as varchar(3))
	)as id_line,

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
    'Tunisia' as region,
    CASE when tcisli310{ic}.t_srcp = 102 then 'M-102' when tcisli310{ic}.t_srcp = 104 THEN 'M-104' when tcisli310{ic}.t_srcp = 105 THEN 'M-105'   END as plant,
    (case  when tcisli310{ic}.t_cups in('km','KM','Km','kM') then 'FG'  ELSE 'NFG' END) as TYPE_INVOICE
    from
    tcisli310{ic},
    tcisli305{ic}
    where
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
    and tcisli310{ic}.t_orno not in (select ttdsls406{ic}.t_orno from ttdsls406{ic})
    and tcisli310{ic}.t_orno not in (select ttdsls340{ic}.t_schn from ttdsls340{ic})
    and tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
    tcisli305{ic}.t_stat=80
    """

    return pd.read_sql(text,cnx)

