import pandas as pd
import numpy as np
from tqdm import tqdm

def extract_EE(Firm, Start, End, cnx):
     text = f"""
     SELECT distinct
     X300SD.lpli.lglgrf AS ID_Line,
     X300SD.lpli.LGBRAR AS Trans_Type,
     X300SD.lpli.LGRGNR AS Invoice_N,
     X300SD.lpli.LGWACD AS Currency,
     X300SD.kdst.kdNAME AS Desc_STPB,
     X300SD.lpli.LGKDNR AS Sold_To_BP,
     CAST(X300SD.lpli.LGNEWT AS DECIMAL(10,2)) AS Net_Line_Amount,
     CAST(X300SD.lpli.LGLIMG AS DECIMAL(10,2)) AS Inv_Quantity,
     CAST(X300SD.lpli.LGNEWT AS DECIMAL(10,2)) / CAST(X300SD.lpli.LGLIMG AS DECIMAL(10,2)) AS Price,
     CAST(SUBSTR(X300SD.lpli.LGRGDA, 5, 2) || '/' || SUBSTR(X300SD.lpli.LGRGDA, 7, 2) || '/' || SUBSTR(X300SD.lpli.LGRGDA, 1, 4) AS DATE) AS Inv_Date,
     CAST(X300SD.lpli.LGPREI AS DECIMAL(10,2)) AS Added_value,
     TRIM(X300SD.lpli.LGTENR) AS item,
     X300SD.teil.TEBEZ1 AS Item_Description,
     X300SD.lpli.LGLIES AS shipment,
     CASE WHEN (X300SD.lpli.lgfirm = '1') THEN 'COF EE'
     WHEN (X300SD.lpli.lgfirm = '2') THEN 'COF PL'
     WHEN (X300SD.lpli.lgfirm = '3') THEN 'COF MK'
     WHEN (X300SD.lpli.lgfirm = '4') THEN 'COF SRB'
     END AS Plant,
     'Eastern Europe' AS Region,
     X300SD.lpli.lglanr AS Type,
     CAST(X300SD.lpli.lgstat AS VARCHAR(4)) AS Inv_Stat,
     X300SD.teil.TEPRGR AS fam,
     X300SD.teil.TETEFA AS sect,
     X300SD.lplp.LPSNBE AS Part_Number,
     SUBSTR(TRIM(FP.FSTEXT), 1, 5) AS Price_Unit,
     SUBSTR(TRIM(FQ.FSTEXT), 1, 5) AS Qty_Unit,
     CAST((CAST(X300SD.afp4.p4emtn AS DECIMAL(10,2)) / CAST(X300SD.afp4.p4baku AS DECIMAL(10,2))) / 1000 AS DECIMAL(10,2)) AS Metal_Rate,
     
     CAST(p4emfk AS DECIMAL(10,2)) AS Metal_weight_sales,
     CASE WHEN X300SD.teil.TETART = '1' AND X300SD.teil.TESTAP = '1' AND SUBSTR(TRIM(FP.FSTEXT), 1, 5) = 'm' THEN 'FG'
     ELSE 'NFG' END AS type_invoice,
     'EUR' AS Reporting_currency_Euro,
     'USD' AS Reporting_currency_USD,
     CASE WHEN X300SD.lpli.lgfirm = '1' THEN '132'
     WHEN X300SD.lpli.lgfirm = '2' THEN '133'
     WHEN X300SD.lpli.lgfirm = '3' THEN '135'
     WHEN X300SD.lpli.lgfirm = '4' THEN '134'
     END AS inv_company,
     CASE WHEN X300SD.lpli.lgfirm = '1' THEN '132'
     WHEN X300SD.lpli.lgfirm = '2' THEN '133'
     WHEN X300SD.lpli.lgfirm = '3' THEN '135'
     WHEN X300SD.lpli.lgfirm = '4' THEN '134'
     END AS sales_company,

     0 AS CONFIRMED,
     1 AS active,
     1 AS request,
     X300SD.lpli.LGVENR AS Ship_To_BP,
     shp.kdNAME AS Ship_To_Description

     FROM X300SD.LPLI

     LEFT JOIN X300SD.teil ON X300SD.lpli.lgfirm = X300SD.teil.tefirm AND X300SD.lpli.lgtenr = X300SD.teil.tetenr
     LEFT JOIN X300SD.lplp ON X300SD.lpli.lgfirm = X300SD.lplp.lpfirm AND X300SD.lpli.lgkdnr = X300SD.lplp.lpkdnr
     AND X300SD.lpli.lgvenr = X300SD.lplp.lpvenr AND X300SD.lpli.lgtenr = X300SD.lplp.lptenr
     LEFT JOIN X300SD.FSTX FQ ON FQ.FSFIRM = (CASE WHEN X300SD.lpli.lgfirm = '4' THEN '1' ELSE X300SD.lpli.LGFIRM END)
     AND X300SD.teil.TEMEIN = RIGHT(TRIM(FQ.FSSCHL), 1) AND FQ.FSFLNA = 'T2TXBZ' AND FQ.FSSCHL LIKE '02%' AND FQ.FSSPCD = 'E'
     LEFT JOIN X300SD.FSTX FP ON FP.FSFIRM = (CASE WHEN X300SD.lpli.lgfirm = '4' THEN '1' ELSE X300SD.lpli.LGFIRM END)
     AND X300SD.teil.temepr = RIGHT(TRIM(FP.FSSCHL), 1) AND FP.FSFLNA = 'T2TXBZ' AND FP.FSSCHL LIKE '02%' AND FP.FSSPCD = 'E'
     LEFT JOIN X300SD.afp4 ON X300SD.lpli.lglgrf = X300SD.afp4.p4lgrf AND P4KUDA > 20221200 AND p4firm = {Firm}
     LEFT JOIN X300SD.kdst ON X300SD.lpli.lgfirm = X300SD.kdst.kdfirm AND X300SD.lpli.lgkdnr = X300SD.kdst.kdkdnr
     AND X300SD.kdst.kdvenr = 1
     LEFT JOIN X300SD.kdst shp ON X300SD.lpli.lgfirm = shp.kdfirm AND X300SD.lpli.lgkdnr = shp.kdkdnr
     AND shp.kdvenr = X300SD.lpli.LGVENR

     WHERE X300SD.lpli.LGRGDA BETWEEN '{Start}' AND '{End}' AND X300SD.lpli.lgfirm = '{Firm}'

     """
     #print(text)
     return pd.read_sql(text, cnx)