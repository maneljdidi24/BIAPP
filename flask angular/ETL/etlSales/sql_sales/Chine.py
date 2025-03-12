import pandas as pd
#xpps_maroc_ma&int
import pandas as pd
import numpy as np


def extract_Chine_1(Ic,sc,Start,End,cnx):

    text = f""" 
    select
    (cast(tcisli310{Ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{Ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{Ic}.t_idoc as char))+'-'+
    rtrim(cast(ttdsls340{Ic}.t_dlno as char))+'-'+
    rtrim(cast(ttdsls340{Ic}.t_shpo as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{Ic}.t_mati))
			,cast (row_number() over(partition by tcisli310{Ic}.t_srcp,tcisli310{Ic}.t_idoc, ttdsls340{Ic}.t_dlno ,ttdsls340{Ic}.t_shpo
                                     order by     tcisli310{Ic}.t_srcp,tcisli310{Ic}.t_idoc, ttdsls340{Ic}.t_dlno ,ttdsls340{Ic}.t_shpo )as varchar(3))
			)
	) as ID_Line,

    tcisli310{Ic}.t_tran as Trans_Type,
    tcisli310{Ic}.t_idoc as Invoice_N,  
    tcisli305{Ic}.t_ccur as Currency,  
    tcisli310{Ic}.t_ofbp as Sold_To_BP,  
    ttccom100502.t_nama     as Desc_STPB,
    tcisli310{Ic}.t_dqua as Inv_Quantity,
    tcisli310{Ic}.t_cuns as Qty_Unit ,
    tcisli310{Ic}.t_pric as Price ,
    tcisli310{Ic}.t_cups as Price_Unit ,
    tcisli310{Ic}.t_orno as Sales_O_S_N,
    ltrim(tcisli310{Ic}.t_item) as Item  ,
    ttcibd001{Ic}.t_dsca     as Item_Description,
    tcisli310{Ic}.t_amti as Net_Line_Amount,
    tcisli305{Ic}.t_idat as Inv_Date,
    tcisli310{Ic}.t_stbp as Ship_To_BP,
    ttdsls340{Ic}.t_dlno as Shipment,
    ttdsls340{Ic}.t_shpo as Shipment_line,
    ttcibd004{Ic}.t_aitc as Part_Number ,
    case  tcisli310{sc}.t_sfcp when  153 then 'COF TT' when 502 then 'COF TJ' END as plant,
    tcisli310{Ic}.t_amth_1 as Net_Line_Amount_HC,
    'CNY' as Home_Currency,
    tcisli310{Ic}.t_amth_2 as Reporting_Amount_Euro,
    'EUR' as Reporting_Currency_Euro,
    tcisli310{Ic}.t_amth_3 as Reporting_Amount_USD,
    'USD' as Reporting_Currency_USD,
    tcisli310{Ic}.t_sfcp as Inv_Company,
    tcisli310{Ic}.t_srcp as Sales_Company,
    ttdsls301{Ic}.t_pric as Added_value,
    ttdsls301{Ic}.t_cono as Contract_N,
    ttdsls301{Ic}.t_cwar as warehouse,
    ttdmpv102{Ic}.t_mprs as Mterial_Exchange,
    ttdmpv102{Ic}.t_matf as Metal_weight_sales,
    ttdmpv102{Ic}.t_mati as Material_Type,
    ttdmpv102{Ic}.t_apri as Metal_Rate,
    case when tcisli310{Ic}.t_cups IN ('km','KM','Km','m','M') then 'FG' ELSE 'NFG' END as type_invoice,
    
    1 as request,
    0 as confirmed,
    1 as active 
   
    
    
    FROM

    tcisli305{Ic},            
    tcisli310{Ic} left join ttcibd004{Ic} on tcisli310{Ic}.t_item=ttcibd004{Ic}.t_item and ttcibd004{Ic}.t_bpid=tcisli310{Ic}.t_stbp  ,
    ttccom100502,
    ttcibd001{Ic},
    ttdsls340{Ic} left join
    ttdsls321{Ic}  
    
    left join ttdmpv102{Ic} on
    ttdmpv102{Ic}.t_orno=ttdsls321{Ic}.t_schn and ttdmpv102{Ic}.t_sqnb=ttdsls321{Ic}.t_spon
    and ttdmpv102{Ic}.t_pono=ttdsls321{Ic}.t_revn

    left join  ttdsls311{Ic}
    left join ttdsls301{Ic} on ttdsls301{Ic}.t_cono= ttdsls311{Ic}.t_cono and ttdsls301{Ic}.t_pono= ttdsls311{Ic}.t_pono
    on ttdsls311{Ic}.t_schn= ttdsls321{Ic}.t_worn and ttdsls311{Ic}.t_sctp=2
    and ttdsls311{Ic}.t_revn=ttdsls321{Ic}.t_revn
    on ttdsls321{Ic}.t_worn=ttdsls340{Ic}.t_schn
    and ttdsls321{Ic}.t_sctp=2 and ttdsls321{Ic}.t_wsqn=ttdsls340{Ic}.t_wsqn

    WHERE

    tcisli305{Ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
    And tcisli310{Ic}.t_ofbp = tcisli305{Ic}.t_itbp
    and tcisli310{Ic}.t_idoc = tcisli305{Ic}.t_idoc
    and tcisli310{Ic}.t_tran=tcisli305{Ic}.t_tran
    and ttcibd001{Ic}.t_item=tcisli310{Ic}.t_item  
    and tcisli310{Ic}.t_ofbp= ttccom100502.t_bpid
    and tcisli310{Ic}.t_idoc=ttdsls340{Ic}.t_invn
    and tcisli310{Ic}.t_tran=ttdsls340{Ic}.t_ttyp
    and ttdsls340{Ic}.t_schn=tcisli310{Ic}.t_orno
    and tcisli310{Ic}.t_shln=ttdsls340{Ic}.t_shpo
    and ttdsls340{Ic}.t_dlno=tcisli310{Ic}.t_shpm
    """
   #print(text)
    return pd.read_sql(text, cnx)

def extract_Chine_2(Ic,sc,Start,End,cnx):

    text = f""" Select
     (cast(tcisli310{Ic}.t_sfcp as char(3))+'-'+
	cast(tcisli310{Ic}.t_srcp as char(3))+'-'+
    rtrim(cast(tcisli310{Ic}.t_idoc as char))+'-'+
    rtrim(cast(tcisli310{Ic}.t_shpm as char))+'-'+
    rtrim(cast( tcisli310{Ic}.t_shln as char))+'-'+  
	
	isnull(rtrim(ltrim(ttdmpv102{Ic}.t_mati))
			,cast (row_number() over(partition by tcisli310{Ic}.t_srcp,tcisli310{Ic}.t_idoc, tcisli310{Ic}.t_shpm ,tcisli310{Ic}.t_shln
                                     order by     tcisli310{Ic}.t_srcp,tcisli310{Ic}.t_idoc, tcisli310{Ic}.t_shpm ,tcisli310{Ic}.t_shln )as varchar(3))
			)
	) as id_line,

    tcisli310{Ic}.t_tran  as  Trans_Type,
    tcisli310{Ic}.t_idoc  as  Invoice_N,
    tcisli305{Ic}.t_ccur  as  Currency,
    tcisli310{Ic}.t_ofbp  as  Sold_To_BP,
    ttccom100502.t_nama   as  Desc_STPB,
    tcisli310{Ic}.t_dqua  as  Inv_Quantity,
    tcisli310{Ic}.t_cuns  as  Qty_Unit,
    tcisli310{Ic}.t_pric  as  Price ,
    tcisli310{Ic}.t_cups  as  Price_Unit ,
    tcisli310{Ic}.t_orno  as  Sales_O_S_N,
    ltrim(tcisli310{Ic}.t_item)  as  Item,
    ttcibd001{Ic}.t_dsca  as  Item_Description,
    tcisli310{Ic}.t_amti  as  Net_Line_Amount,
    tcisli305{Ic}.t_idat  as  Inv_Date,
    tcisli310{Ic}.t_stbp  as  Ship_To_BP,
    ttdmpv102{Ic}.t_mprs  as  Mterial_Exchange,
    ttdmpv102{Ic}.t_matf  as  Metal_weight_sales,
    ttdsls301{Ic}.t_pric  as  Added_value,
    ttdsls401{Ic}.t_bpri  as  Bpri,
    ttdmpv102{Ic}.t_apri  as  Metal_Rate,
    ttdsls301{Ic}.t_cono  as  Contract_N,
    tcisli310{Ic}.t_shpm  as  shipment,
    tcisli310{Ic}.t_shln  as  shipment_line,
    ttcibd004{Ic}.t_aitc  as  Part_Number,
    case  tcisli310{sc}.t_sfcp when  153 then 'COF TT' when 502 then 'COF TJ' END  as plant,
    tcisli310{Ic}.t_amth_1  as  Net_Line_Amount_HC,
    'CNY'  as  Home_Currency,
    tcisli310{Ic}.t_amth_2  as  Reporting_Amount_Euro,
    'EUR'  as  Reporting_Currency_Euro,
    tcisli310{Ic}.t_amth_3  as  Reporting_Amount_USD,
    'USD'  as  Reporting_Currency_USD,
    ttdmpv102{Ic}.t_mati  as  Material_Type,
    tcisli310{Ic}.t_sfcp  as  Inv_Company,
    tcisli310{Ic}.t_srcp  as  Sales_Company,
    case  when tcisli310{Ic}.t_cups IN ('km','KM','Km','m','M') then 'FG' ELSE 'NFG' END as type_invoice,
    ttdsls401{Ic}.t_cwar  as  warehouse,
    2 as request, 1 as active,0 as confirmed
    --,CASE ttdsls406{Ic}.t_porg  WHEN 4 THEN 'Manual' WHEN 6 THEN 'Contract' END  as Price_Origine 
    FROM
    tcisli305{Ic}, ttdsls401{Ic}
    WITH (NOLOCK)
    left join ttdsls301{Ic} on ttdsls301{Ic}.t_cono=ttdsls401{Ic}.t_cono and ttdsls401{Ic}.t_cpon=ttdsls301{Ic}.t_pono,
    ttdsls406{Ic} left join ttdmpv102{Ic} on ttdmpv102{Ic}.t_orno=ttdsls406{Ic}.t_orno and ttdmpv102{Ic}.t_pono=ttdsls406{Ic}.t_pono and ttdmpv102{Ic}.t_sqnb=ttdsls406{Ic}.t_sqnb ,
    tcisli310{Ic} left join ttcibd004{Ic} on tcisli310{Ic}.t_item=ttcibd004{Ic}.t_item and ttcibd004{Ic}.t_bpid=tcisli310{Ic}.t_stbp,
    ttcibd001{Ic},
    ttccom100502

    where

    tcisli305{Ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}',102) and
    ttdsls406{Ic}.t_pono = tcisli310{Ic}.t_pono and
    tcisli310{Ic}.t_ofbp = tcisli305{Ic}.t_itbp and
    tcisli310{Ic}.t_idoc = tcisli305{Ic}.t_idoc and
    tcisli305{Ic}.t_stat= 6 and
    tcisli310{Ic}.t_idoc=ttdsls406{Ic}.t_invn and
    tcisli310{Ic}.t_tran=ttdsls406{Ic}.t_ttyp and
    ttdsls406{Ic}.t_orno=tcisli310{Ic}.t_orno and
    tcisli305{Ic}.t_tran=ttdsls406{Ic}.t_ttyp and
    ttcibd001{Ic}.t_item=tcisli310{Ic}.t_item and
    tcisli310{Ic}.t_ofbp= ttccom100502.t_bpid and
    tcisli310{Ic}.t_pono= ttdsls406{Ic}.t_pono and
    tcisli310{Ic}.t_pono=ttdsls401{Ic}.t_pono and
    tcisli310{Ic}.t_orno=ttdsls401{Ic}.t_orno and
    ttdsls401{Ic}.t_sqnb=ttdsls406{Ic}.t_sqnb and
    ttdsls406{Ic}.t_shln=tcisli310{Ic}.t_shln and
    tcisli310{Ic}.t_shpm=ttdsls406{Ic}.t_shpm

    """
   #print(text)
    return pd.read_sql(text, cnx)


def Manual_Sales_Envoice_Chine(plant,Start,End,cnx):# manual invoice
    text= f"""Select 

   ('R3_'+cast(tcisli310{plant}.t_sfcp as char(3))+'-'+
    cast(tcisli310{plant}.t_srcp as char(3))+'-'+ 
    rtrim(cast(tcisli310{plant}.t_idoc as char))+'-'+
    cast (row_number() over(partition by tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc
                             order by    tcisli310{plant}.t_srcp,tcisli310{plant}.t_idoc )as varchar(10))) as id_line,

    tcisli310{plant}.t_tran as Trans_Type ,
    tcisli310{plant}.t_idoc as  Invoice_N,
    tcisli305{plant}.t_ccur as  Currency,
    tcisli310{plant}.t_ofbp as  Sold_To_BP,
    tcisli310{plant}.t_dqua as  Inv_Quantity,
    tcisli310{plant}.t_cuns as  Qty_Unit,
    tcisli310{plant}.t_pric as  Price,
    tcisli310{plant}.t_cups as  Price_Unit,
    tcisli310{plant}.t_orno as Sales_O_S_N,
    rtrim(ltrim(CASE WHEN tcisli310{plant}.t_item ='' then 'Manual' else tcisli310{plant}.t_item END )) as  Item,
    tcisli310{plant}.t_amti as  Net_Line_Amount,
    tcisli305{plant}.t_idat as  Inv_Date,
    tcisli310{plant}.t_stbp as  Ship_To_BP,
    tcisli310{plant}.t_amth_1 as  Net_Line_Amount_HC,
    tcisli310{plant}.t_amth_2 as  Reporting_Amount_Euro,
    tcisli310{plant}.t_amth_3 as  Reporting_Amount_USD,
    tcisli310{plant}.t_sfcp as  Inv_Company,
    tcisli310{plant}.t_srcp as  Sales_Company,
    (case when tcisli310{plant}.t_sfcp =153 then 'M-153' ELSE 'M-502' END )as plant,
    tcisli310{plant}.t_shln as  shipment_line,
    tcisli310{plant}.t_shpm as  shipment,
    
    'HNL'  as  Home_Currency,
    'EUR'  as  Reporting_Currency_Euro,
    'USD'  as  Reporting_Currency_USD,
    3 as request, 
    1 as active,
    0 as confirmed,
    'NFG' as TYPE_INVOICE,
    '' as warehouse,
    'Manual Sales invoice_'+cast(tcisli310{plant}.t_srcp as char) as Sales_Company_Dsc,
    'Manual Sales invoice_'+cast(tcisli310{plant}.t_srcp as char) as INV_Company_DESC

    FROM
        tcisli310{plant},tcisli305{plant}
        
    WHERE
        tcisli305{plant}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) 
    and tcisli310{plant}.t_orno not in (select ttdsls406{plant}.t_orno from ttdsls406{plant}) 
    and tcisli310{plant}.t_orno not in (select ttdsls340{plant}.t_schn from ttdsls340{plant})
	and tcisli310{plant}.t_ofbp = tcisli305{plant}.t_itbp 
	and tcisli310{plant}.t_idoc = tcisli305{plant}.t_idoc 
    and tcisli310{plant}.t_tran = tcisli305{plant}.t_tran

	and tcisli305{plant}.t_stat=6
    """
    #print (text)
    return pd.read_sql(text,cnx)
