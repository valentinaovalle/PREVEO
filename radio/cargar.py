import requests 
import pandas as pd
import os
import streamlit as st
import requests
import shutil

def download_file(url):
    local_filename = 'Reporte Novedades.xlsx'
    with requests.get(url, stream=True) as r:
        print(r)
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename



BASE_URL = st.secrets["API_PROD"] if st.secrets.get("PROD",False) else st.secrets["API_DEV"]


def traer_toc():
    data = {
        "username": st.secrets["USER"],
        "password": st.secrets["CONTRASENA"],
    }
#Peticiones tipo  post,
    request =requests.Request(
        'POST', 
        f"{BASE_URL}/token",
        files = {
            'username': (None, data['username']),
            'password': (None, data['password']),
        }
    ).prepare()

#Envio la peticion para traer el token
    s =requests.Session()
    response = s.send(request)
    token = eval(response.text).get("access_token")

    return token

def _normalize(s):
	replacements = {
      ("null", "None"),
      ("true", "True"),
      ("false", "False")
    }

	for a, b in replacements:
		s = s.replace(a, b)

	return s

@st.experimental_memo(ttl=900)
def cargar_info():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{BASE_URL}/api/v1/employee", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        employees = pd.DataFrame(dict_data['data'])
    except:
        employees = pd.DataFrame()    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cost_center", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cost_center = pd.DataFrame(dict_data['data'])
    except:
        cost_center = pd.DataFrame()
    try:        
        response = requests.get(f"{BASE_URL}/api/v1/novelty_type", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        tip_nov = pd.DataFrame(dict_data['data'])
    except:
        tip_nov = pd.DataFrame()
    try:        
        response = requests.get(f"{BASE_URL}/api/v1/novelty", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        data = pd.DataFrame(dict_data['data'])
    except:
        data = pd.DataFrame()
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/expense_reimbursement", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_05 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_05 = pd.DataFrame()
    try:    
        response = requests.get(f"{BASE_URL}/api/v1/loan", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        pr = pd.DataFrame(dict_data['data'])
    except: 
        pr = pd.DataFrame()
    try:    
        response = requests.get(f"{BASE_URL}/api/v1/cost_center_inactive", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cc_in = pd.DataFrame(dict_data['data'])
    except:
        cc_in = pd.DataFrame()
    
    descargar()
    return cost_center, employees, data, tip_nov ,F_AD_05, pr, cc_in

def descargar():
    try:
        url = f"{BASE_URL}/api/v1/spreadsheet"
        return download_file(url)
    except:
        pass
    
def cargar_excel(files):
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f"{BASE_URL}/api/v1/spreadsheet", headers=headers, files=files)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    return dict_data 

@st.experimental_memo(ttl=900)
def traer_cale():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f"{BASE_URL}/api/v1/schedule", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    cale = pd.DataFrame(dict_data['data'])
    return cale

def mod_cale(ini,fin):
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    
    envia={
    "format_code": "F-NOM-01",
    "day_from": ini,
    "day_to": fin
    }
    response = requests.post(f"{BASE_URL}/api/v1/active/1", headers=headers, json=envia)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    return dict_data 


@st.experimental_memo(ttl=900)
def cargar_formularios_1():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f"{BASE_URL}/api/v1/contractor_income", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_31 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_31 = pd.DataFrame()
        
    try:
        response = requests.get(f"{BASE_URL}/api/v1/request_for_advances", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        request = pd.DataFrame(dict_data['data'])
    except:
        request = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/petty_cash_reimbursement", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_07 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_07 = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/resource_request", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_14 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_14 = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/review_of_accounts_receivable_invoices", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_16 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_16 = pd.DataFrame()
   
    descargar()
    return F_AD_31,F_AD_16,F_AD_14,F_AD_07,request


@st.experimental_memo(ttl=900)
def cargar_formularios_2():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:        
         response = requests.get(f"{BASE_URL}/api/v1/data_update", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         F_TH_13_B = pd.DataFrame(dict_data['data'])
    except:
         F_TH_13_B = pd.DataFrame()
    try:
         response = requests.get(f"{BASE_URL}/api/v1/emotional_salary_control", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         F_TH_02 = pd.DataFrame(dict_data['data'])
    except:
         F_TH_02 = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/induction_roadmap", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_TH_10 = pd.DataFrame(dict_data['data'])
    except:
        F_TH_10 = pd.DataFrame()
         
    descargar()
    return   F_TH_02,F_TH_13_B,F_TH_10
    
@st.experimental_memo(ttl=900)    
def cargar_formularios_3():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
     response = requests.get(f"{BASE_URL}/api/v1/supplier_customer_data_automation", headers=headers)
     trans_data = _normalize(response.text)
     dict_data = eval(trans_data)
     F_AD_29 = pd.DataFrame(dict_data['data'])
    except:
     F_AD_29 = pd.DataFrame()
    
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/expense_reimbursement", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_05 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_05 = pd.DataFrame()
        
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/delivery_control_and_return", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_22_A = pd.DataFrame(dict_data['data'])
    except:
        F_AD_22_A = pd.DataFrame()
        
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/control_and_monitoring_of_suppliers", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_24_A = pd.DataFrame(dict_data['data'])
    except:
        F_AD_24_A = pd.DataFrame()

    descargar()
    return  F_AD_29,F_AD_05,F_AD_22_A,F_AD_24_A


@st.experimental_memo(ttl=900)
def cargar_formularios_4():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{BASE_URL}/api/v1/training_tracking", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_TH_25 = pd.DataFrame(dict_data['data'])
    except:
        F_TH_25 = pd.DataFrame()
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/job_applicant", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_TH_13_A = pd.DataFrame(dict_data['data'])
    except:
        F_TH_13_A = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cccgp_committee_requests", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_TH_15 = pd.DataFrame(dict_data['data'])
    except:
        F_TH_15 = pd.DataFrame()

    descargar()
    return F_TH_25,F_TH_13_A,F_TH_15


@st.experimental_memo(ttl=900)
def cargar_formularios_5():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{BASE_URL}/api/v1/supervision_tecnica_04", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        supervision = pd.DataFrame(dict_data['data'])
    except:
        supervision = pd.DataFrame()
        
    try:
        response = requests.get(f"{BASE_URL}/api/v1/expense_reimbursement_ratio", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        expense_reimbursement_ratio = pd.DataFrame(dict_data['data'])
    except:
        expense_reimbursement_ratio = pd.DataFrame()
        
    try:
        response = requests.get(f"{BASE_URL}/api/v1/billing_information", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        billing_information = pd.DataFrame(dict_data['data'])
    except:
        billing_information = pd.DataFrame()   
        
    try:
      response = requests.get(f"{BASE_URL}/api/v1/control_and_monitoring_of_suppliers", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      control = pd.DataFrame(dict_data['data'])
    except:
      control = pd.DataFrame() 
        

    descargar()
    return supervision,expense_reimbursement_ratio,billing_information,control

@st.experimental_memo(ttl=900)
def cargar_formularios_6():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_registration", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_AD_17 = pd.DataFrame(dict_data['data'])
    except:
      F_AD_17 = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/certificate_of_delivery_of_work_tools", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_AD_19 = pd.DataFrame(dict_data['data'])
    except:
      F_AD_19 = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/administrative_purchase_order", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_06 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_06 = pd.DataFrame()    
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_evaluation", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_AD_24_B = pd.DataFrame(dict_data['data'])
    except:
      F_AD_24_B = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_reassessment", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_AD_24_D = pd.DataFrame(dict_data['data'])
    except:
      F_AD_24_D= pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/return_control", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_AD_22_B = pd.DataFrame(dict_data['data'])
    except:
      F_AD_22_B= pd.DataFrame()

    descargar()
    return  F_AD_24_B,F_AD_06,F_AD_19,F_AD_17, F_AD_24_D,F_AD_22_B

@st.experimental_memo(ttl=900)
def cargar_formularios_7():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
      response = requests.get(f"{BASE_URL}/api/v1/training_program", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_TH_22 = pd.DataFrame(dict_data['data'])
    except:
      F_TH_22 = pd.DataFrame()
          
    try:
      response = requests.get(f"{BASE_URL}/api/v1/audit_check", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_SG_07 = pd.DataFrame(dict_data['data'])
    except:
      F_SG_07 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/audit_report", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_SG_08 = pd.DataFrame(dict_data['data'])
    except:
      F_SG_08 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/stretcher_and_first_aid_kit_inspection", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_SG_10 = pd.DataFrame(dict_data['data'])
    except:
      F_SG_10 = pd.DataFrame()
      
      
    descargar()
    return F_TH_22,F_SG_07,F_SG_08,F_SG_10


@st.experimental_memo(ttl=900)
def cargar_formularios_8():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
      response = requests.get(f"{BASE_URL}/api/v1/check_list_epcc", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_SG_38 = pd.DataFrame(dict_data['data'])
    except:
      F_SG_38 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/control_of_industrialized_structure", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_05 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_05 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/structural_masonry_control_and_dovelas", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_06 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_06 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/guardrail_load_test_control", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_07 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_07 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/certificate_of_completion_of_technical_supervision", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_11 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_11 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/plan_review", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_12 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_12 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/density_control", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_ST_19 = pd.DataFrame(dict_data['data'])
    except:
      F_ST_19 = pd.DataFrame()
      
    descargar()
    return F_SG_38,F_ST_05,F_ST_06,F_ST_07,F_ST_11,F_ST_12,F_ST_19


@st.experimental_memo(ttl=900)
def cargar_basicos():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{BASE_URL}/api/v1/current_employee", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        current = pd.DataFrame(dict_data['data'])
    except:
        current = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cost_center_employee", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cost_center_employee = pd.DataFrame(dict_data['data'])
    except:
        cost_center_employee = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/iva", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        iva = pd.DataFrame(dict_data['data'])
    except:
        iva = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ica", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        ica = pd.DataFrame(dict_data['data'])
    except:
        ica = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/menu", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        menu = pd.DataFrame(dict_data['data'])
    except:
        menu = pd.DataFrame()
       
    try:        
        response = requests.get(f"{BASE_URL}/api/v1/novelty_type", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        tip_nov = pd.DataFrame(dict_data['data'])
    except:
        tip_nov = pd.DataFrame()
    try:        
        response = requests.get(f"{BASE_URL}/api/v1/novelty", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        data = pd.DataFrame(dict_data['data'])
    except:
        data = pd.DataFrame()
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/expense_reimbursement", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        df = pd.DataFrame(dict_data['data'])
    except:
        df = pd.DataFrame()
    try:    
        response = requests.get(f"{BASE_URL}/api/v1/loan", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        pr = pd.DataFrame(dict_data['data'])
    except: 
        pr = pd.DataFrame()
    try:    
        response = requests.get(f"{BASE_URL}/api/v1/cost_center_inactive", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cc_in = pd.DataFrame(dict_data['data'])
    except:
        cc_in = pd.DataFrame()
        
    try:
        response = requests.get(f"{BASE_URL}/api/v1/employee", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        employees = pd.DataFrame(dict_data['data'])
    except:
        employees = pd.DataFrame()    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cost_center", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cost_center = pd.DataFrame(dict_data['data'])
    except:
        cost_center = pd.DataFrame()
        
    descargar()
    return    data, tip_nov ,df, pr, cc_in,employees,cost_center




























