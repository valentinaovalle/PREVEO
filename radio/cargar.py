import requests 
import pandas as pd
import os
import streamlit as st
import requests
import shutil

def download_file(url):
    local_filename = 'Reporte Novedades.xlsx'
    with requests.get(url, stream=True) as r:
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

    response = requests.get(f"{BASE_URL}/api/v1/employee", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    employees = pd.DataFrame(dict_data['data'])

    response = requests.get(f"{BASE_URL}/api/v1/cost_center", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    cost_center = pd.DataFrame(dict_data['data'])
    
    response = requests.get(f"{BASE_URL}/api/v1/novelty_type", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    tip_nov = pd.DataFrame(dict_data['data'])
    
    response = requests.get(f"{BASE_URL}/api/v1/novelty", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    data = pd.DataFrame(dict_data['data'])
    
    response = requests.get(f"{BASE_URL}/api/v1/expense_reimbursement", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    df = pd.DataFrame(dict_data['data'])
    
    response = requests.get(f"{BASE_URL}/api/v1/loan", headers=headers)
    trans_data = _normalize(response.text)
    dict_data = eval(trans_data)
    pr = pd.DataFrame(dict_data['data'])
    
    descargar()
    return cost_center, employees, data, tip_nov ,df, pr

def descargar():
    url = f"{BASE_URL}/api/v1/spreadsheet"
    return download_file(url)
    
   