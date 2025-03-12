def extract(plant,Start,End):  
    return f""" SELECT top 10
    ttdpur400{plant}.t_orno AS PO_Number,
    ttdpur401{plant}.t_pono AS PO_Line,
    ttdpur401{plant}.t_sqnb AS PO_sqnb,
    ttdpur400{plant}.t_ccon as ID_buyer,
	buyer.t_nama as buyer_Name,
    CONVERT(date, ttdpur400{plant}.t_odat) AS Order_Date,
    ttdpur401{plant}.t_amld AS Discount_Amount,
    ttdpur401{plant}.t_oamt AS Net_Order_Amount,
    ttdpur401{plant}.t_pric AS Unit_Price,
	ttdpur401{plant}.t_cuqp AS Unit,
    ttdpur400{plant}.t_ccur AS Currency,
    ttdpur401{plant}.t_qoor AS Ordered_Quantity,
    ttcibd001100.t_item AS Item_ID,
    ttcibd001100.t_citg AS Item_family,
    ttcmcs023100.t_dsca As Item_Groupe,
    ttcibd001100.t_dsca AS Description,
    ttccom100100.t_bpid AS Business_PartnerID,
    ttccom100100.t_nama AS Business_Partner,
    ttcmcs010100.t_dsca AS BusinessPartner_Country,
    COALESCE(ttcmcs065100.t_cwoc,tdepartemant.t_cwoc,(select ttcmcs065100.t_cwoc  from ttcmcs065100 where ttcmcs065100.t_cwoc=ttdpur400{plant}.t_cofc)) as Department_ID,
    COALESCE(ttcmcs065100.t_dsca,tdepartemant.t_dsca, (SELECT ttcmcs065100.t_dsca FROM ttcmcs065100 WHERE ttcmcs065100.t_cwoc = ttdpur400{plant}.t_cofc)) AS Department,
    CASE
        WHEN {plant}={plant} THEN COALESCE(T_LeadSite.t_desc,'COF TN') 
        WHEN {plant}=104 THEN COALESCE(T_LeadSite.t_desc,'COF MD') 
        WHEN {plant}=122 THEN COALESCE(T_LeadSite.t_desc,'COF PT')
        WHEN {plant}=125 THEN COALESCE(T_LeadSite.t_desc,'COF GR')
    END AS leadSite,
    COALESCE(T_CostCenter.t_desc, '') AS Cost_center,
    COALESCE(T_IVG.t_desc, '') AS IVG,
	COALESCE(ttdpur406{plant}.t_rcno, '0') AS Receipt_Number,
	COALESCE(ttdpur406{plant}.t_rseq, '0') AS Receipt_Number_Lines,
	COALESCE(ttdpur406{plant}.t_sqnb, 0) AS SequanceReceipt,
	CASE
        WHEN ttdpur406{plant}.t_fire = 1 THEN 'Yes'
        WHEN ttdpur406{plant}.t_fire = 2 THEN 'No'
    END AS statusReceipt,
	CASE
        WHEN ttdpur406{plant}.t_conf = 1 THEN 'Yes'
        WHEN ttdpur406{plant}.t_conf = 2 THEN 'No'
    END AS ReceiptConfirmed,
    CONVERT(date,ttdpur406{plant}.t_ddte) as Actual_Receipt_Date,
    COALESCE(ttdpur406{plant}.t_damt, 0) AS Receipt_Amount,
    COALESCE(ttdpur406{plant}.t_qidl, 0) AS Received_Quantity


FROM ttdpur401{plant} WITH (NOLOCK)

    INNER JOIN ttdpur400{plant} ON ttdpur401{plant}.t_orno=ttdpur400{plant}.t_orno
    LEFT JOIN ttdpur402{plant} ON ttdpur401{plant}.t_orno=ttdpur402{plant}.t_orno AND ttdpur401{plant}.t_pono=ttdpur402{plant}.t_pono AND ttdpur401{plant}.t_sqnb=ttdpur402{plant}.t_sqnb

    --extracts the PR that is linked to PO and PO lines and RFQ and R
    left JOIN (select  distinct t1.t_qono ,t1.t_pono,t1.t_opon,t2.t_otbp, t1.t_oorn , t2.t_prno,t2.t_ppon
                from (select ttdpur102{plant}.t_qono ,ttdpur102{plant}.t_pono, ttdpur102{plant}.t_oorn ,ttdpur102{plant}.t_opon from ttdpur102{plant} where ttdpur102{plant}.t_otbp ='') t1
                left join (select ttdpur102{plant}.t_qono ,ttdpur102{plant}.t_pono, ttdpur102{plant}.t_otbp,ttdpur102{plant}.t_prno,ttdpur102{plant}.t_ppon from ttdpur102{plant} where ttdpur102{plant}.t_oorn ='') t2
                on t1.t_qono=t2.t_qono and t1.t_pono=t2.t_pono ) 
                Table1 on (Table1.t_qono = ttdpur402{plant}.t_qono AND Table1.t_pono = ttdpur402{plant}.t_qpon)  
            and ((Table1.t_prno = ttdpur401{plant}.t_orno) OR  (Table1.t_prno=ttdpur402{plant}.t_reto) ) 
    INNER JOIN ttcibd001100 ON ttdpur401{plant}.t_item=ttcibd001100.t_item
    INNER JOIN ttccom100100 ON ttdpur401{plant}.t_otbp=ttccom100100.t_bpid
    left JOIN ttdpur406{plant} ON ttdpur401{plant}.t_orno=ttdpur406{plant}.t_orno AND ttdpur401{plant}.t_pono=ttdpur406{plant}.t_pono AND ttdpur401{plant}.t_sqnb=ttdpur406{plant}.t_sqnb
    
    --second depart with wh
    left join (select TDepart1.t_rqno,ttcmcs065100.t_dsca,ttcmcs065100.t_cwoc from ttcmcs065100 inner join ttdpur200{plant} TDepart1
    on ttcmcs065100.t_cwoc = TDepart1.t_rdep) tdepartemant on Table1.t_oorn = tdepartemant.t_rqno OR ttdpur402{plant}.t_rqno = tdepartemant.t_rqno 

    left join ttfgld010{plant} as T_LeadSite on substring(ttdpur401{plant}.t_glco,14,6) = T_LeadSite.t_dimx and T_LeadSite.t_dtyp=1 and substring(ttdpur401{plant}.t_glco,14,6)<>''
        left join ttfgld010{plant} as T_CostCenter on substring(ttdpur401{plant}.t_glco,24,8) = T_CostCenter.t_dimx and T_CostCenter.t_dtyp=2 and substring(ttdpur401{plant}.t_glco,24,8)<>''
        left join ttfgld010{plant} as T_IVG on  substring(ttdpur401{plant}.t_glco,44,6)=T_IVG.t_dimx AND T_IVG.t_dtyp=4 and substring(ttdpur401{plant}.t_glco,44,6)<>''


    left join 
    ttdpur203{plant} as Creating_Request on ( Creating_Request.t_rqno=Table1.t_oorn OR  Creating_Request.t_rqno=ttdpur402{plant}.t_rqno) AND   Creating_Request.t_rqst=1 
        AND Creating_Request.t_trdt=(SELECT min(CR1.t_trdt) FROM ttdpur203{plant} CR1
        WHERE (CR1.t_rqno=Table1.t_oorn OR  CR1.t_rqno=ttdpur402{plant}.t_rqno) AND CR1.t_rqst=1
    ) 

    left join 
    ttdpur203{plant} as Accepting_Request on (Accepting_Request.t_rqno=Table1.t_oorn OR  Accepting_Request.t_rqno=ttdpur402{plant}.t_rqno) AND   Accepting_Request.t_rqst=3 
        AND Accepting_Request.t_trdt=(SELECT min(CR1.t_trdt) FROM ttdpur203{plant} CR1
        WHERE (CR1.t_rqno=Table1.t_oorn OR  CR1.t_rqno=ttdpur402{plant}.t_rqno) AND CR1.t_rqst=3  
    ) 

    left join 
    ttdpur203{plant} as Final_Approval on (Final_Approval.t_rqno=Table1.t_oorn OR  Final_Approval.t_rqno=ttdpur402{plant}.t_rqno) AND   Final_Approval.t_rqst=3 
        AND Final_Approval.t_trdt=(SELECT max(CR1.t_trdt) FROM ttdpur203{plant} CR1
        WHERE (CR1.t_rqno=Table1.t_oorn OR  CR1.t_rqno=ttdpur402{plant}.t_rqno) AND CR1.t_rqst=3 
    ) 

    left join 
    ttdpur203{plant} as Processed_Request on ( Processed_Request.t_rqno=Table1.t_oorn OR  Processed_Request.t_rqno=ttdpur402{plant}.t_rqno) AND   Processed_Request.t_rqst=7 
        AND Processed_Request.t_trdt=(SELECT max(CR1.t_trdt) FROM ttdpur203{plant} CR1
        WHERE (CR1.t_rqno=Table1.t_oorn OR  CR1.t_rqno=ttdpur402{plant}.t_rqno) AND CR1.t_rqst=7
    ) 
   
    left join ttccom122{plant} on ttccom100100.t_bpid=ttccom122{plant}.t_ifbp
    left join ttcmcs013100  as T_payment on T_payment.t_cpay=ttccom122{plant}.t_cpay
    left join ttcmcs013100 as T_credit on T_credit.t_cpay=ttccom122{plant}.t_rpay
	inner join ttccom130100 on ttccom100100.t_cadr=ttccom130100.t_cadr
	inner join ttcmcs010100 on ttccom130100.t_ccty=ttcmcs010100.t_ccty
   LEFT JOIN (
     SELECT t_orno, t_pono, t_sqnb, t_rcno, t_rseq, t_rsqn, Min(t_logn) AS t_logn
     FROM ttdpur456{plant}
     GROUP BY t_orno, t_pono, t_sqnb, t_rcno, t_rseq, t_rsqn
   ) AS ttdpur456{plant}_distinct ON ttdpur401{plant}.t_orno = ttdpur456{plant}_distinct.t_orno
                            AND ttdpur401{plant}.t_pono = ttdpur456{plant}_distinct.t_pono
                            AND ttdpur401{plant}.t_sqnb = ttdpur456{plant}_distinct.t_sqnb
                            AND ttdpur406{plant}.t_rcno = ttdpur456{plant}_distinct.t_rcno
                            AND ttdpur406{plant}.t_rseq = ttdpur456{plant}_distinct.t_rseq
                            AND ttdpur406{plant}.t_rsqn = ttdpur456{plant}_distinct.t_rsqn
                            AND ttdpur400{plant}.t_odno = ''
	left JOIN ttdpur456{plant} AS return_tab ON ttdpur400{plant}.t_odno = return_tab.t_orno AND ttdpur402{plant}.t_retp=return_tab.t_pono AND ttdpur406{plant}.t_rcno = return_tab.t_rcno 
	AND ttdpur406{plant}.t_rseq = return_tab.t_rseq

    --first depart with login
	left JOIN ttccom001100 ON ttdpur456{plant}_distinct.t_logn = ttccom001100.t_loco OR return_tab.t_logn = ttccom001100.t_loco
    left join ttcmcs065100 ON ttccom001100.t_cwoc=ttcmcs065100.t_cwoc

    --item groupe left join with item families
	left join ttcmcs023100 on ttcmcs023100.t_citg = ttcibd001100.t_citg

    --buyer from the purchase depart
    left join ttccom001100 as buyer on  buyer.t_emno=ttdpur400{plant}.t_ccon

	where ttdpur400{plant}.t_odat BETWEEN '{Start}' AND '{End}' and Table1.t_oorn is null
      AND ttdpur402{plant}.t_rqno IS NULL """