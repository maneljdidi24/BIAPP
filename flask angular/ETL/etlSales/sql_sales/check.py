import pandas as pd



def check_data_1(ic,sc,Start,End,cnx):
    text= f"""select count(*) as X
    FROM
    tcisli305{ic},            
    tcisli310{ic} ,ttdsls340{sc}
    WHERE
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) 
    And tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp 
    and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc 
    and tcisli310{ic}.t_tran = tcisli305{ic}.t_tran 
    and tcisli310{ic}.t_idoc = ttdsls340{sc}.t_invn
    and tcisli310{ic}.t_tran = ttdsls340{sc}.t_ttyp
    and ttdsls340{sc}.t_schn = tcisli310{ic}.t_orno
    and tcisli310{ic}.t_shln = ttdsls340{sc}.t_shpo
    and ttdsls340{sc}.t_dlno = tcisli310{ic}.t_shpm 

    and tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp 
  
    """
    return  pd.read_sql(text, cnx)

def check_data_2(ic,sc,Start,End,cnx):
    text= f"""select count(*) as Y
    from tcisli310{ic},tcisli305{ic},ttdsls406{sc} 
    where 
    tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) and
    tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
    tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
    tcisli305{ic}.t_stat =(case when {ic} in(102,104,105,122,125,127) then 80 else 6 end ) and
    tcisli310{ic}.t_idoc = ttdsls406{sc}.t_invn and
    tcisli310{ic}.t_tran = ttdsls406{sc}.t_ttyp and
    ttdsls406{sc}.t_orno = tcisli310{ic}.t_orno and
    tcisli305{ic}.t_tran = ttdsls406{sc}.t_ttyp and
    tcisli310{ic}.t_pono = ttdsls406{sc}.t_pono and 
    ttdsls406{sc}.t_shln = tcisli310{ic}.t_shln and 
    tcisli310{ic}.t_shpm = ttdsls406{sc}.t_shpm and

    tcisli310{ic}.t_sfcp =tcisli305{ic}.t_sfcp
    

    """
    return  pd.read_sql(text, cnx)



#tn-pt
def check_data_year_ln(ic,sc,Start,End,cnx):
    
    text= f"""
        (
        select 
        year(tcisli305{ic}.t_idat) as Y,isnull(count(*),0) as X ,tcisli310{ic}.t_srcp as S,'Q1' AS Q
        FROM
        tcisli305{ic},            
        tcisli310{ic} ,ttdsls340{sc}
        WHERE
        year(tcisli305{ic}.t_idat) between year(CONVERT(DATETIME, '{Start}', 102)) and year(CONVERT(DATETIME, '{End}', 102)) 
        And tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp 
        and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc 
        and tcisli310{ic}.t_tran = tcisli305{ic}.t_tran 
        and tcisli310{ic}.t_idoc = ttdsls340{sc}.t_invn
        and tcisli310{ic}.t_tran = ttdsls340{sc}.t_ttyp
        and ttdsls340{sc}.t_schn = tcisli310{ic}.t_orno
        and tcisli310{ic}.t_shln = ttdsls340{sc}.t_shpo
        and ttdsls340{sc}.t_dlno = tcisli310{ic}.t_shpm 
        and tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp           
        group by tcisli310{ic}.t_srcp ,year(tcisli305{ic}.t_idat)
        )

        UNION

        (
        select 
        year(tcisli305{ic}.t_idat) as Y,isnull(count(*),0) as X,tcisli310{ic}.t_srcp as S,'Q2' AS Q
        from 
        tcisli310{ic},tcisli305{ic},ttdsls406{sc} 
        where 
        year(tcisli305{ic}.t_idat) between year(CONVERT(DATETIME, '{Start}', 102)) and year(CONVERT(DATETIME, '{End}', 102)) and
        tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
        tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
        tcisli305{ic}.t_stat= (case when {ic} in(102,104,105,122,125,127) then 80 else 6 end ) and
        tcisli310{ic}.t_idoc=ttdsls406{sc}.t_invn and
        tcisli310{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        ttdsls406{sc}.t_orno=tcisli310{ic}.t_orno and 
        tcisli305{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        tcisli310{ic}.t_pono= ttdsls406{sc}.t_pono and 
        ttdsls406{sc}.t_shln=tcisli310{ic}.t_shln and 
        tcisli310{ic}.t_shpm=ttdsls406{sc}.t_shpm and 
        tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp
        group by tcisli310{ic}.t_srcp ,year(tcisli305{ic}.t_idat) 
        ) 
        ORDER BY year(tcisli305{ic}.t_idat) ,Q
    """
    return  pd.read_sql(text, cnx)

def check_data_month_ln(ic,sc,Start,End,cnx):
    
    text= f"""
        (
        select 
        year(tcisli305{ic}.t_idat) as Y,month(tcisli305{ic}.t_idat) as m ,isnull(count(*),0) as X ,tcisli310{ic}.t_srcp as S,'Q1' AS Q
        FROM
        tcisli305{ic},            
        tcisli310{ic} ,ttdsls340{sc}
        WHERE
        tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
        And tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp 
        and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc 
        and tcisli310{ic}.t_tran = tcisli305{ic}.t_tran 
        and tcisli310{ic}.t_idoc = ttdsls340{sc}.t_invn
        and tcisli310{ic}.t_tran = ttdsls340{sc}.t_ttyp
        and ttdsls340{sc}.t_schn = tcisli310{ic}.t_orno
        and tcisli310{ic}.t_shln = ttdsls340{sc}.t_shpo
        and ttdsls340{sc}.t_dlno = tcisli310{ic}.t_shpm 
        and tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp   
        and tcisli305{ic}.t_stat= (case when {ic} in(102,104,105,122,125,127) then 80 else 6 end )   
        group by month(tcisli305{ic}.t_idat),tcisli310{ic}.t_srcp ,year(tcisli305{ic}.t_idat)
        )

        UNION

        (
        select 
        year(tcisli305{ic}.t_idat) as Y,month(tcisli305{ic}.t_idat) as m,isnull(count(*),0) as X,tcisli310{ic}.t_srcp as S,'Q2' AS Q
        from 
        tcisli310{ic},tcisli305{ic},ttdsls406{sc} 
        where 
        tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) and
        tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
        tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
        tcisli305{ic}.t_stat= (case when {ic} in(102,104,105,122,125,127) then 80 else 6 end ) and
        tcisli310{ic}.t_idoc=ttdsls406{sc}.t_invn and
        tcisli310{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        ttdsls406{sc}.t_orno=tcisli310{ic}.t_orno and 
        tcisli305{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        tcisli310{ic}.t_pono= ttdsls406{sc}.t_pono and
        ttdsls406{sc}.t_shln=tcisli310{ic}.t_shln and
        tcisli310{ic}.t_shpm=ttdsls406{sc}.t_shpm and
        tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp
        group by month(tcisli305{ic}.t_idat) ,tcisli310{ic}.t_srcp ,year(tcisli305{ic}.t_idat) ) 
        ORDER BY year(tcisli305{ic}.t_idat) ,month(tcisli305{ic}.t_idat),Q
    """
    return  pd.read_sql(text, cnx)

def check_data_day_ln(ic,sc,Start,End,cnx):
    
    text= f"""
        (
        select 
        year(tcisli305{ic}.t_idat) as Y,month(tcisli305{ic}.t_idat) as m ,isnull(count(*),0) as X ,tcisli310{ic}.t_srcp as S,'Q1' AS Q ,day(tcisli305{ic}.t_idat) as d
        FROM
        tcisli305{ic},            
        tcisli310{ic} ,ttdsls340{sc}
        WHERE
        tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
        And tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp 
        and tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc 
        and tcisli310{ic}.t_tran = tcisli305{ic}.t_tran 
        and tcisli310{ic}.t_idoc = ttdsls340{sc}.t_invn
        and tcisli310{ic}.t_tran = ttdsls340{sc}.t_ttyp
        and ttdsls340{sc}.t_schn = tcisli310{ic}.t_orno
        and tcisli310{ic}.t_shln = ttdsls340{sc}.t_shpo
        and ttdsls340{sc}.t_dlno = tcisli310{ic}.t_shpm 
        and tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp           
        group by year(tcisli305{ic}.t_idat),month(tcisli305{ic}.t_idat),day(tcisli305{ic}.t_idat),tcisli310{ic}.t_srcp 
        )

        UNION

        (
        select 
        year(tcisli305{ic}.t_idat) as Y,month(tcisli305{ic}.t_idat) as m,isnull(count(*),0) as X,tcisli310{ic}.t_srcp as S,'Q2' AS Q ,day(tcisli305{ic}.t_idat) as d
        from 
        tcisli310{ic},tcisli305{ic},ttdsls406{sc} 
        where 
        tcisli305{ic}.t_idat between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102) and
        tcisli310{ic}.t_ofbp = tcisli305{ic}.t_itbp and
        tcisli310{ic}.t_idoc = tcisli305{ic}.t_idoc and 
        tcisli305{ic}.t_stat= (case when {ic} in(102,104,105,122,125,127) then 80 else 6 end ) and
        tcisli310{ic}.t_idoc=ttdsls406{sc}.t_invn and
        tcisli310{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        ttdsls406{sc}.t_orno=tcisli310{ic}.t_orno and 
        tcisli305{ic}.t_tran=ttdsls406{sc}.t_ttyp and
        tcisli310{ic}.t_pono= ttdsls406{sc}.t_pono and
        ttdsls406{sc}.t_shln=tcisli310{ic}.t_shln and
        tcisli310{ic}.t_shpm=ttdsls406{sc}.t_shpm and
        tcisli310{ic}.t_sfcp = tcisli305{ic}.t_sfcp
        group by year(tcisli305{ic}.t_idat) ,month(tcisli305{ic}.t_idat) ,day(tcisli305{ic}.t_idat) ,tcisli310{ic}.t_srcp
        )
        ORDER BY year(tcisli305{ic}.t_idat) ,month(tcisli305{ic}.t_idat),day(tcisli305{ic}.t_idat),Q
    """
    return  pd.read_sql(text, cnx)



#azure**********************************************************

def check_data_year_azure_local(ic,sc,Start,End,cnx,tables):
    
    text= f"""
        select 
        year(inv_date) as Y_ ,isnull(count(*),0) as X_ ,inv_company as S_ ,(case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END ) as Q_
        FROM
        {tables}
        WHERE
        year(inv_date) between year(CONVERT(DATETIME, '{Start}', 102)) and year(CONVERT(DATETIME, '{End}', 102))
        and request in (1,2)
        and inv_company in ({ic})
        and sales_company in ({sc})
        group by year(inv_date),inv_company,request
        ORDER BY year(inv_date),inv_company,(case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END )
        """
    return  pd.read_sql(text, cnx)

def check_data_month_azure_local(ic,sc,Start,End,cnx,tables):
    
    text= f"""
        select 
        year(inv_date) as Y_,month(inv_date) as m_ ,isnull(count(*),0) as X_ ,inv_company as S_, (case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END ) as Q_
        FROM
        {tables}
        WHERE
        inv_date between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
        and request in (1,2)
        and inv_company  in ({ic})
        and sales_company in  ({sc})
        group by month(inv_date),year(inv_date),inv_company,request
        ORDER BY year(inv_date), month(inv_date),inv_company,(case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END )
        """
    return  pd.read_sql(text, cnx)

def check_data_day_azure_local(ic,sc,Start,End,cnx,tables):
    
    text= f"""
        select 
        year(inv_date) as Y_,
        month(inv_date) as m_ ,
        isnull(count(*),0) as X_ ,
        inv_company as S_, 
        (case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END ) as Q_,
        day(inv_date) as d_
        FROM
        {tables}
        WHERE
        inv_date between CONVERT(DATETIME, '{Start}', 102) and CONVERT(DATETIME, '{End}', 102)
        and request in(1,2)
        and inv_company in ({ic})
        and sales_company in ({sc})
        group by year(inv_date),month(inv_date),inv_company,day(inv_date),request
        ORDER BY year(inv_date), month(inv_date),inv_company,day(inv_date) ,(case request when 1 then 'Q1' WHEN 2 THEN 'Q2' END )
        """
    return  pd.read_sql(text, cnx)




#xpps*************************************************************
def CKECK_xpps_year_ma_int(Start,End,cnx):
    text = f"""
    
    select 
    year(X301SD.lpli.lgrgda) as Y,count(*) as X ,(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) as S,'-' AS Q
    FROM X301SD.lpli 
    WHERE 
    year(X301SD.lpli.LGRGDA)  between year('{Start}') AND year('{End}')
    GROUP BY year(X301SD.lpli.LGRGDA) ,(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) 
    ORDER BY year(X301SD.lpli.LGRGDA) ,(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END )


    """
    return  pd.read_sql(text, cnx)

def CKECK_xpps_mth_ma_int(Start,End,cnx):
    text = f"""
    
    select 
        year(X301SD.lpli.lgrgda) as Y,month(X301SD.lpli.lgrgda) as m ,count(*) as X ,(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) as S,'-' AS Q
    FROM X301SD.lpli 
    WHERE 
    year(X301SD.lpli.LGRGDA) between year('{Start}') and year('{End}')
    AND month(X301SD.lpli.LGRGDA) between month('{Start}') and month('{End}')
    GROUP BY year(X301SD.lpli.LGRGDA) ,month(X301SD.lpli.lgrgda),(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) 
    ORDER BY year(X301SD.lpli.LGRGDA) ,month(X301SD.lpli.lgrgda),(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END )
    
    """
    print(text)
    return  pd.read_sql(text, cnx)

def CKECK_xpps_day_ma_int(Start,End,cnx):
    text = f"""
    SELECT 
    year(X301SD.lpli.lgrgda) as Y,month(X301SD.lpli.lgrgda) as m,day(X301SD.lpli.lgrgda) as d,count(*) as X ,(CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) as S,'-' AS Q
    FROM X301SD.lpli 
    WHERE 
    X301SD.lpli.LGRGDA between '{Start}' AND '{End}'
    GROUP BY (CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) ,year(X301SD.lpli.LGRGDA) ,month(X301SD.lpli.lgrgda),day(X301SD.lpli.lgrgda)
    ORDER BY (CASE when (X301SD.lpli.lgfirm = '1') THEN '112' ELSE '114' END) ,year(X301SD.lpli.LGRGDA) ,month(X301SD.lpli.lgrgda),day(X301SD.lpli.lgrgda)
    """
    return  pd.read_sql(text, cnx)



def CKECK_xpps_year_kt(Start,End,cnx):
    text = f""" SELECT
    year(X301SD.lpli.LGRGDA)as Y,count(*) as X,113 as S,'-' as Q
    FROM X301SD.lpli 
    WHERE  X301SD.lpli.lgfirm=1 and
    year(X301SD.lpli.LGRGDA) between year('{Start}') AND year('{End}')
    GROUP BY year(X301SD.lpli.LGRGDA) 
    ORDER BY year(X301SD.lpli.LGRGDA)  
    """
    return  pd.read_sql(text, cnx)

def CKECK_xpps_mth_kt(Start,End,cnx):
    text = f""" SELECT
    year(X301SD.lpli.LGRGDA)as Y,month(X301SD.lpli.LGRGDA) as m,count(*) as X,113 as S,'-' as Q
    FROM X301SD.lpli 
    WHERE  X301SD.lpli.lgfirm=1 and
    year(X301SD.lpli.LGRGDA) between year('{Start}') AND year('{End}')
    GROUP BY year(X301SD.lpli.LGRGDA),month(X301SD.lpli.LGRGDA) 
    ORDER BY year(X301SD.lpli.LGRGDA),month(X301SD.lpli.LGRGDA) 
    """
    return  pd.read_sql(text, cnx)

def CKECK_xpps_day_kt(Start,End,cnx):
    text = f""" SELECT
    year(X301SD.lpli.LGRGDA)as Y,month(X301SD.lpli.LGRGDA) as m,day(X301SD.lpli.LGRGDA) as d ,count(*) as X,113 as S,'-' as Q
    FROM X301SD.lpli 
    WHERE  X301SD.lpli.lgfirm=1 and
    year(X301SD.lpli.LGRGDA) between year('{Start}') AND year('{End}')
    GROUP BY year(X301SD.lpli.LGRGDA),month(X301SD.lpli.LGRGDA),day(X301SD.lpli.LGRGDA) 
    ORDER BY year(X301SD.lpli.LGRGDA),month(X301SD.lpli.LGRGDA),day(X301SD.lpli.LGRGDA) 
    """
    return  pd.read_sql(text, cnx)



def CKECK_xpps_year_EE(Start,End,f,cnx):
    text = f""" SELECT
    year(X300SD.lpli.LGRGDA) as Y,count(*) as X ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end) as S ,'-' as Q
    FROM X300SD.lpli 
    WHERE  X300SD.lpli.lgfirm = {f}
    AND year(X300SD.lpli.LGRGDA) between year('{Start}') and year('{End}') 
    AND month(X300SD.lpli.LGRGDA) between month('{Start}') AND month('{End}')
    GROUP BY year(X300SD.lpli.LGRGDA),(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    ORDER BY year(X300SD.lpli.LGRGDA) ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    """
    return  pd.read_sql(text, cnx)

def CKECK_xpps_mth_EE(Start,End,f,cnx):
    text = f""" SELECT
    year(X300SD.lpli.LGRGDA) as Y,month(X300SD.lpli.LGRGDA) as m,count(*) as X ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end) as S ,'-' as Q
    FROM X300SD.lpli 
    WHERE  X300SD.lpli.lgfirm={f}
    AND year(X300SD.lpli.LGRGDA) between year('{Start}') and year('{End}') 
    AND month(X300SD.lpli.LGRGDA) between month('{Start}') AND month('{End}')
    GROUP BY year(X300SD.lpli.LGRGDA),month(X300SD.lpli.LGRGDA) ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    ORDER BY year(X300SD.lpli.LGRGDA),month(X300SD.lpli.LGRGDA) ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    """
    return  pd.read_sql(text, cnx)

def CKECK_xpps_day_EE(Start,End,f,cnx):
    text = f""" SELECT
    year(X300SD.lpli.LGRGDA)as Y,month(X300SD.lpli.LGRGDA) as m,day(X300SD.lpli.LGRGDA) as d,count(*) as X,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end) as S,'-' as Q
    FROM X300SD.lpli 
    WHERE  
    X300SD.lpli.lgfirm={f} AND 
    X300SD.lpli.LGRGDA between '{Start}' and '{End}'
    GROUP BY year(X300SD.lpli.LGRGDA),month(X300SD.lpli.LGRGDA),day(X300SD.lpli.LGRGDA) ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    ORDER BY year(X300SD.lpli.LGRGDA),month(X300SD.lpli.LGRGDA),day(X300SD.lpli.LGRGDA) ,(case X300SD.lpli.lgfirm when '1' then '132' when '2' then '133' when '3' then '135'  when '4' then '134' end)
    """
    return  pd.read_sql(text, cnx)
