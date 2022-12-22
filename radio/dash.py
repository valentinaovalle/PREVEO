from PIL import Image
im = Image.open("img/favicon.ico")
import streamlit as st
from app import main
from cargar import cargar_info

st.set_page_config(
  page_title="Tableros Preveo", layout="wide",
  page_icon=im,
  #initial_sidebar_state='collapsed'
)

if 'auth' not in st.session_state:
	st.session_state['auth'] = None



if st.session_state['auth']:
    style = """
    <style>
      footer {visibility: hidden;}
      </style>
    """
    st.markdown(style, unsafe_allow_html=True)
    opt=['PREVEO','Nómina','Administrativa','Prestamos'] if st.session_state['auth']=='prueba@lucro.com' else ['Nómina']
    main(opt)

else:
    cols_img = st.columns(12)
    cols_img[5].image("img/PREVEO.PNG",width=200)
    cols = st.columns((1,3,1))
    form = cols[1].form("login")
    c = form.empty()
    form.markdown('<h3 style="text-align: center;">AUTENTICACIÓN</h3>',unsafe_allow_html=True)
    username = form.text_input("Usuario")
    password = form.text_input("Constraseña",type="password")

    # Every form must have a submit button.
    submitted = form.form_submit_button("Entrar")
    if submitted:
        if username in ['prueba@lucro.com','rquevedo@premiumbpo.com','nomina@preveo.com.co','constanza.mora@preveo.com.co'] and password=='Preveo123*':
            st.session_state['auth'] = username
            cargar_info.clear()
            st.experimental_rerun()
        else:
            c.error("Usuario o contraseña incorrecto.")
	
	