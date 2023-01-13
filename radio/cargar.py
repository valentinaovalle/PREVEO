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

@st.experimental_memo(ttl=300)
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
    
    descargar()
    return cost_center, employees, data, tip_nov ,df, pr, cc_in

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

@st.experimental_memo(ttl=300)
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


@st.experimental_memo(ttl=300)
def cargar_formularios_1():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

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
        petty = pd.DataFrame(dict_data['data'])
    except:
        petty = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/resource_request", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        resource = pd.DataFrame(dict_data['data'])
    except:
        resource = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/review_of_accounts_receivable_invoices", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        review = pd.DataFrame(dict_data['data'])
    except:
        review = pd.DataFrame()
   
    try:
        response = requests.get(f"{BASE_URL}/api/v1/job_applicant", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        job = pd.DataFrame(dict_data['data'])
    except:
        job = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cccgp_committee_requests", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        cccgp = pd.DataFrame(dict_data['data'])
    except:
        cccgp = pd.DataFrame()

    descargar()
    return cccgp,job,review,resource,petty,request


@st.experimental_memo(ttl=900)
def cargar_formularios_2():
        token = traer_toc()
        headers = {'Authorization': f'Bearer {token}'}
       
        try:
         response = requests.get(f"{BASE_URL}/api/v1/supplier_customer_data_automation", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         data_automation = pd.DataFrame(dict_data['data'])
        except:
         data_automation = pd.DataFrame()
        try:
         response = requests.get(f"{BASE_URL}/api/v1/emotional_salary_control", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         emotional = pd.DataFrame(dict_data['data'])
        except:
         emotional = pd.DataFrame()
        try:
         response = requests.get(f"{BASE_URL}/api/v1/staff_requirement", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         staff = pd.DataFrame(dict_data['data'])
        except:
         staff = pd.DataFrame()
        try:
         response = requests.get(f"{BASE_URL}/api/v1/wage_equalization", headers=headers)
         trans_data = _normalize(response.text)
         dict_data = eval(trans_data)
         wage = pd.DataFrame(dict_data['data'])
        except:
         wage = pd.DataFrame()  
         
        descargar()
        return   wage,staff,emotional,data_automation
    
@st.experimental_memo(ttl=900)    
def cargar_formularios_3():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

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
        response = requests.get(f"{BASE_URL}/api/v1/delivery_control_and_return", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        delivery_control_and_return = pd.DataFrame(dict_data['data'])
    except:
        delivery_control_and_return = pd.DataFrame()
        
    try:         
        response = requests.get(f"{BASE_URL}/api/v1/control_and_monitoring_of_suppliers", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_22_B  = pd.DataFrame(dict_data['data'])
    except:
        F_AD_22_B = pd.DataFrame()

    descargar()
    return  data,df,delivery_control_and_return,F_AD_22_B


@st.experimental_memo(ttl=900)
def cargar_formularios_4():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{BASE_URL}/api/v1/training_tracking", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        training = pd.DataFrame(dict_data['data'])
    except:
        training = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/vacation_request", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        vacation = pd.DataFrame(dict_data['data'])
    except:
        vacation = pd.DataFrame()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/project_transfer_request", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        project = pd.DataFrame(dict_data['data'])
    except:
        project = pd.DataFrame()

    try:
        response = requests.get(f"{BASE_URL}/api/v1/contractor_income", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_AD_31 = pd.DataFrame(dict_data['data'])
    except:
        F_AD_31 = pd.DataFrame()
        
    try:
        response = requests.get(f"{BASE_URL}/api/v1/induction_roadmap", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        F_TH_10 = pd.DataFrame(dict_data['data'])
    except:
        F_TH_10 = pd.DataFrame()

    descargar()
    return project, vacation,training,F_AD_31,F_TH_10


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
        response = requests.get(f"{BASE_URL}/api/v1/administrative_purchase_order", headers=headers)
        trans_data = _normalize(response.text)
        dict_data = eval(trans_data)
        administrative_purchase_order = pd.DataFrame(dict_data['data'])
    except:
        administrative_purchase_order = pd.DataFrame()   
        

    descargar()
    return supervision,expense_reimbursement_ratio,billing_information,administrative_purchase_order

@st.experimental_memo(ttl=900)
def cargar_formularios_6():
    token = traer_toc()
    headers = {'Authorization': f'Bearer {token}'}
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_registration", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      supplier_registration = pd.DataFrame(dict_data['data'])
    except:
      supplier_registration = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/certificate_of_delivery_of_work_tools", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      certificate = pd.DataFrame(dict_data['data'])
    except:
      certificate = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/control_and_monitoring_of_suppliers", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      control = pd.DataFrame(dict_data['data'])
    except:
      control = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_evaluation", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      supplier = pd.DataFrame(dict_data['data'])
    except:
      supplier = pd.DataFrame()
    try:
      response = requests.get(f"{BASE_URL}/api/v1/supplier_reassessment", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      reassessment = pd.DataFrame(dict_data['data'])
    except:
      reassessment= pd.DataFrame()

    descargar()
    return  supplier,control,certificate,supplier_registration, reassessment

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
      response = requests.get(f"{BASE_URL}/api/v1/withdrawal_from_the_company", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_TH_24 = pd.DataFrame(dict_data['data'])
    except:
      F_TH_24 = pd.DataFrame()
      
    try:
      response = requests.get(f"{BASE_URL}/api/v1/evaluation_trial_period", headers=headers)
      trans_data = _normalize(response.text)
      dict_data = eval(trans_data)
      F_TH_27 = pd.DataFrame(dict_data['data'])
    except:
      F_TH_27 = pd.DataFrame()
      
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
    return F_TH_22,F_TH_24,F_TH_27,F_SG_07,F_SG_08,F_SG_10


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
      
    descargar()
    return F_SG_38,F_ST_05,F_ST_06,F_ST_07,F_ST_11,F_ST_12


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




























