import requests 
import pandas as pd
import os
import streamlit as st


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
    

    return cost_center, employees, data, tip_nov
