import streamlit as st
#from streamlit_metrics import metric, metric_row
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
#import matplotlib
#import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO, StringIO
from PIL import Image
import os
import cargar
import datatable as dt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import markdown


#from typing import List, Optional
#from tkinter import * from tkinter.ttk import *
def main(opt):
    
    F_AD_31,F_AD_16,F_AD_14,F_AD_07,request=cargar.cargar_formularios_1()
    F_TH_02,F_TH_13_B,F_TH_10=cargar.cargar_formularios_2()
    F_AD_29,F_AD_05,F_AD_22_A,F_AD_24_A=cargar.cargar_formularios_3()
    F_TH_25,F_TH_13_A,F_TH_15=cargar.cargar_formularios_4()
    supervision,expense_reimbursement_ratio,billing_information,control=cargar.cargar_formularios_5()
    F_AD_24_B,F_AD_06,F_AD_19,F_AD_17, F_AD_24_D,F_AD_22_B=cargar.cargar_formularios_6()
    F_TH_22,F_SG_07,F_SG_08,F_SG_10=cargar.cargar_formularios_7()
    F_SG_38,F_ST_05,F_ST_06,F_ST_07,F_ST_11,F_ST_12,F_ST_19=cargar.cargar_formularios_8()
    
    
    data, tip_nov ,F_AD_05, pr, cc_in,employees,cost_center =cargar.cargar_info()
    data, tip_nov ,df, pr, cc_in,employees,cost_center=cargar.cargar_basicos()
    cale=cargar.traer_cale()
    with open('styles.css') as f:
        
        st.markdown(f"""<style>
                    {f.read()}
                    </style>"""
        , unsafe_allow_html=True)
    
    
    #scope = ["https://spreadsheets.gptgle.com/feeds",'https://www.googleapis.com/auth/sprea...,"https://www.googleapis.com/auth/drive...","https://www.googleapis.com/auth/drive"]
    #creds = ServiceAccountCredentials.from_json_keyfile_name("tuarchivo.json", scope)
    #client=gspread.authorize(creds)
    #pr=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-NOM-02/find_query.xlsx")
    #pr2=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-NOM-02/find_query.xlsx")
    #st.write(F_ST_19)
    pr['año_mes']=pd.to_datetime(pr['fecha'])
    cantpr=pr.groupby(['centro_de_costos','año_mes'],as_index=False)['valor_del_prestamo'].sum()
    contarpr=pr.groupby(['centro_de_costos'],as_index=False)['valor_del_prestamo'].count()

    #------------------------------------------------------------------------------
    url2='https://drive.google.com/file/d/1-21f9kCJfkcDce91hJYo3e_7030aKoII/view?usp=sharing'
    url2='https://drive.google.com/uc?id=' + url2.split('/')[-2]
    dff2 = pd.read_csv(url2,sep=';')
   
    #df=df.drop(['codigo'], axis=1)
    #df=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-AD-05/find_query.xlsx")
    #df['valor_rembolso']=format(df['valor_rembolso'])
    #df=df.explode('centro_costo')
    #df=df.explode('pagado')
    #df=pd.concat([df.drop(['centro_costo'], axis=1), df['centro_costo'].apply(pd.Series)], axis=1)
    #df=df.drop(['historico_de_aprobacion'], axis=1)
    #df=pd.concat([df.drop(['centro_costo'], axis=1), df['centro_costo'].apply(pd.Series)], axis=1)
    #df=pd.concat([df.drop(['pagado'], axis=1), df['pagado'].apply(pd.Series)], axis=1)
    #df=df.drop(['monto_aprobado_para_rembolso'], axis=1)
    #df=df.drop(['valor_total'], axis=1)
    #df=pd.concat([df.drop(['recibo_o_factura'], axis=1), df['recibo_o_factura'].apply(pd.Series)], axis=1)
   
    
    #reem=df.groupby(['nombres_y_apellidos','numero_cc','nombre'],as_index=False)['valor_rembolso'].sum()
    #top=reem.head(5)
    #vf=df['reembonsable_al_cliente'].value_counts()
    #df['vf']=vf
    
    #vf2=df.groupby(['nombre','reembonsable_al_cliente']).size().unstack(fill_value=0)
    #df['fecha']=pd.to_datetime(df['fecha'], errors='coerce')
    #df['año_mes']=df['fecha'].dt.strftime('%Y-%m')
    
    #cant=df.groupby(['nombre','año_mes'],as_index=False)['valor_rembolso'].sum()
    #topcenter=cant.head(5)
    #contar=df.groupby(['nombre'],as_index=False)['valor_rembolso'].count()
    #men=df.groupby(['fecha_de_pago'],as_index=False)['valor_rembolso'].sum
    #-----------------------------------------------------------------------------
    #data = pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/LUCRO/prueba.xlsx")
    data=data.drop(["codigo_centro_de_costos"],axis=1) 
    data.columns = data.columns.str.replace(' ', '_') 
    data['fecha_inicial_novedad'] = pd.to_datetime(data['fecha_inicial_novedad'],format='%Y-%m-%d')
    
    data['fecha_final_novedad'] = pd.to_datetime(data['fecha_final_novedad'], errors='coerce')
    data['documento_de_identificacion'] = data['documento_de_identificacion'].astype(str)
    data['año_mes']=data['fecha_inicial_novedad'].dt.strftime('%Y-%m')
    #graf=data.groupby(['nombre_del_empleado','centro_de_costos'])['dias_laborados']   
    #Fac = data.groupby(['Nombre Del Empleado', 'Documento De Identificacion'])['Dias Laborados'].sum() 
    data['empleado']=data['nombre_del_empleado']+ "-" +data["documento_de_identificacion"]
    
    data['Alerta']=""
    for i in range(len(data['nombre_del_empleado'])):
        if data.iloc[i,3] == 30:
           data.iloc[i,4] = "OK"
        else:
           data.iloc[i,4] = "Revisar"
    
    
    
    Lab =data.groupby(['nombre_del_empleado','documento_de_identificacion','año_mes'],as_index=False)['dias_laborados'].sum()
    Lab['Alerta']=""
    
    for i in range(len(Lab['nombre_del_empleado'])):
        if Lab.iloc[i,3] == 30:
            Lab.iloc[i,4] = "OK"
        else:
            Lab.iloc[i,4] = "Revisar"
    
    #Lab['centro_de_costos']=data['centro_de_costos']        
    
    Por_tra = (Lab['dias_laborados']/30)*100
    Lab['Por_tra']=Por_tra   
    #-----------------------------------------------------------------------------
    url='https://drive.google.com/file/d/1SYecV7Sm7NOarvSg6uAoZSgRdRcECLua/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    cm = pd.read_csv(url,sep=';')
    #cm=pd.read_excel("https://docs.google.com/spreadsheets/d/1dxWGKibM_6n5llwR68zUxVuxQ8AAKn2T/edit?usp=sharing&ouid=112502888078542287829&rtpof=true&sd=true")
  
    cm['año_mes']=pd.to_datetime(cm['fecha_de_elaboracion'],format='%d/%m/%Y')
    cantcm=cm.groupby(['cargar_a_centro_de_costos','año_mes'],as_index=False)['total'].sum()
    contarcm=cm.groupby(['cargar_a_centro_de_costos'],as_index=False)['total'].count()
    reemcm=cm.groupby(['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos'],as_index=False)['total'].sum()
    cmv=cm['reembonsable_al_cliente'].value_counts()
    #-----------------------------------------------------------------------------
    #emplea=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/EMPLEADOS/em.xlsx")
    employees['salario']=employees['salario'].replace({',':''}, regex=True)
    employees['salario']=employees['salario'].astype(int)
    sorteo=employees.sort_values(by='salario')
    #----------------------------------------------------------------------------
    def SetMoneda(num, simbolo="$", n_decimales=2):
        #con abs, nos aseguramos que los dec. sea un positivo.
        n_decimales = abs(n_decimales)
        #se redondea a los decimales idicados.
        num = round(num, n_decimales)
        #se divide el entero del decimal y obtenemos los string
        num, dec = str(num).split(".")
        #si el num tiene menos decimales que los que se quieren mostrar,
        #se completan los faltantes con ceros.
        dec += "0" * (n_decimales - len(dec))
        #se invierte el num, para facilitar la adicion de comas.
        num = num[::-1]
        #se crea una lista con las cifras de miles como elementos.
        l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])]
        l.reverse()
        #se pasa la lista a string, uniendo sus elementos con comas.
        num = str.join(",", l)
        #si el numero es negativo, se quita una coma sobrante.
        try:
            if num[0:2] == "-,":
                num = "-%s" % num[2:]
        except IndexError:
            pass
        #si no se especifican decimales, se retorna un numero entero.
        if not n_decimales:
            return "%s %s" % (simbolo, num)
        return "%s %s.%s" % (simbolo, num, dec)
    
    #-------------------------------------------------------------------------------
    
#QUITAR ESPACIO DE EL BORDE SUPERIOR
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)

#CENTRAR EL LOGO EN LA BARRA LATERAL    
    st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
    )
#INSERTAR LOGO EN LA BARRA LATERAL    
    with st.sidebar.container():
     image =Image.open('PREVEO5.png') 
     new_image = image.resize((185, 160))
     st.image(new_image, width=None, use_column_width=False)
     
     
   
    #sidebar-> menú desplegable a un lado
    #selectbox-> menú desplegable centrado a lo largo
    #---------------------------------------------------------------------------
    #CREANDO FILTROS
    #-----------------------------------------------------------------------------
    #-------------------------------------INICIO----------------------------------
    #-----------------------------------------------------------------------------
    #"""def home(Lab):
     #   st.header('')
         
      #  mes= st.sidebar.selectbox(
       # "Mes:",
       # pd.unique(data['año_mes'])
    #    )
     #   dataf=data[(data.año_mes == mes)]
     #   ms1=pd.unique(dataf['centro_de_costos'])
     #   ms2=np.append(ms1,"Todos")
    
      #  cent_cost_filter= st.sidebar.selectbox(
       # "Centro Costos:",
       #  ms2
        # )
        #if "Todos" in cent_cost_filter: 
         #   cent_cost_filter = dataf['centro_de_costos']
        #else:
         #   cent_cost_filter=[cent_cost_filter]
        #dataf=dataf[(dataf.centro_de_costos.isin(cent_cost_filter))]
        #cd1=pd.unique(dataf['nombre_del_empleado'])
    #    cd2=np.append(cd1,"Todos")
    #    empleado = st.sidebar.selectbox(
    #    "Empleado:",
    #    cd2
    #     ) 
    #    if "Todos" in empleado: 
    #        empleado = dataf['nombre_del_empleado']
    #    else:
    #        empleado=[empleado]
        
    #    data_selection=dataf[(dataf.nombre_del_empleado.isin(empleado)) & (dataf.año_mes==mes)]
        #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
        
        #Tipo2=pd.merge(data_selection,tip_nov,left_on='tipo_de_novedad',right_on='uuid')   
        #data_selection['Tipo Novedad']=Tipo2['novedad'].values
    #    empleados_centro=employees[employees.centro_de_costo.isin(cent_cost_filter)]
    #    data_selection=pd.merge(empleados_centro.astype(str),data_selection.astype(str),how='left',left_on='identificacion',right_on='documento_de_identificacion')
    #    data_selection['dias_laborados']=data_selection['dias_laborados'].fillna(0).astype(int)
    #    data_selection['nombre_del_empleado']=data_selection['empleado_x']
    #    por_tra = (data_selection['dias_laborados']/30)*100
    #    data_selection['Por_tra']=por_tra
        
        #st.write(data_selection[['nombre_del_empleado','documento_de_identificacion','centro_de_costos','dias_laborados','año_mes','Tipo Novedad']])
    #    data_selection['Alerta']=""
    #    for i in data_selection['nombre_del_empleado'].index:
    #      if data_selection.loc[i,'dias_laborados'] == 30:
    #         data_selection.loc[i,'Alerta'] = "OK"
    #      else:
    #        data_selection.loc[i,'Alerta'] = "Revisar"
        
    #    st.write(data_selection[['nombre_del_empleado','documento_de_identificacion','centro_de_costos','dias_laborados','año_mes','tipo_de_novedad','Alerta']])
        
        
    #    def to_excel(data_selection):
    #     output = BytesIO()
    #     writer = pd.ExcelWriter(output, engine='xlsxwriter')
    #     data_selection.to_excel(writer, index=False, sheet_name='Sheet1')
    #     workbook = writer.book
    #     worksheet = writer.sheets['Sheet1']
    #     format1 = workbook.add_format({'num_format': '0.00'}) 
    #     worksheet.set_column('A:A', None, format1)  
    #     writer.save()
    #     processed_data = output.getvalue()
    #     return processed_data
    #    Lab_xlsx = to_excel(data_selection)
    #    st.download_button(label='Resultados en XLSX',
    #                                data=Lab_xlsx ,
    #                                file_name= 'df_test.xlsx')"""
    #-----------------------------------------------------------------------------
    #-------------------------------PREVEO----------------------------------------
    #------------------------------------------------------------------------------
    #st.write(data)
    def preveo():
        st.header('')
        
        def cc():
            st.header('CENTROS DE COSTOS')
            cost_center, employees, data, tip_nov ,df, pr, cc_in =cargar.cargar_info()
            url='https://drive.google.com/file/d/1PLqE00MJbjR_P9f64-AAd1NeFw0gPFIr/view?usp=sharing'
            url='https://drive.google.com/uc?id=' + url.split('/')[-2]
            cost_center = pd.read_csv(url,sep=';')
            
            #cost_center=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/COST_CENTER/cc.xlsx")
            cost_center=cost_center.fillna('No_Aplica')
            cost_center['vigencia_del_proyecto'] = cost_center['vigencia_del_proyecto'].replace(
             { "NO": 'NO_VIGENTE'})
            cost_center['vigencia_del_proyecto']=cost_center['vigencia_del_proyecto'].str.upper()
            
            #cost_center=cost_center.explode('empleados')
            #empleados_centro=empleados_centro.empleados.apply(pd.Series)
            #cost_center=cost_center.explode('quien_reporta')
            #quien_centro=quien_centro.quien_reporta.apply(pd.Series)
            conteo=cost_center.groupby(['centro_de_costo'])['vigencia_del_proyecto'].count()
            
            
            #grid = st.grid()
            #with grid("1 1 1") as grid:
             #   grid.cell(
              #      class_="a",
               #     grid_column_start=2,
                #    grid_column_end=3,
                 #   grid_row_start=1,
                  #  grid_row_end=2,
                #).markdown("# This is A Markdown Cell")
                #grid.cell("b", 2, 3, 2, 3).text("The cell to the left is a dataframe")
                #grid.cell("c", 3, 4, 2, 3).plotly_chart(get_plotly_fig())
                #grid.cell("d", 1, 2, 1, 3).dataframe(get_dataframe())
                #grid.cell("e", 3, 4, 1, 2).markdown("Try changing the **block container style** in the sidebar!")
            
            
            #m1,m2=st.columns(2):
            #m1.metric(label='TOTAL', value=cost_center['centro_de_costo'].count())
            
                  
         
            #a1,a2,a3=st.columns(3)
            #a1.metric(label='', value=(''))
            
            #st.metric(label='TOTAL', value=cost_center['centro_de_costo'].count())
            #a3.metric(label='', value=(''))
            
            
            freqsi = cost_center['vigencia_del_proyecto'].str.contains('SI').value_counts()[True]
            freqna = cost_center['vigencia_del_proyecto'].str.contains('NO_APLICA').value_counts()[True]
            freqno = cost_center['vigencia_del_proyecto'].str.contains('NO_VIGENTE').value_counts()[True]
            #freqni = cost_center['vigencia_del_proyecto'].str.contains('NO HA INICIADO').value_counts()[True]
            
            c1,c2,c3,c4=st.columns(4)
            c1.metric(label='TOTAL', value=cost_center['centro_de_costo'].count())
            c2.metric(label='VIGENTE', value=freqsi)
            c3.metric(label='NO VIGENTE', value=freqno)
            c4.metric(label='NO APLICA', value=freqna)
            #c4.metric(label='SIN INICIAR', value=freqni)
                   
            cost_center=cost_center.rename({'centro_de_costo': 'Centros De Costos','vigencia_del_proyecto':'Vigencia'}, axis=1)
            #AgGrid(cost_center)
            gb = GridOptionsBuilder.from_dataframe(cost_center)
            #gb.configure_pagination(enabled=True) #Add pagination
            gb.configure_default_column(editable=True,groupable=True)
            gb.configure_side_bar() #Add a sidebar
            gb.configure_selection('multiple') #Enable multi-row selection
            gridOptions = gb.build()
            for column in gridOptions['columnDefs']:
                column["cellStyle"]= {'color': 'black', 'background-color': '#f3f5c3'}
            #st.write(gridOptions['columnDefs'])
           
            grid_response = AgGrid(
              cost_center,
              editable=True,
              gridOptions=gridOptions,
              data_return_mode='AS_INPUT', 
              update_mode=GridUpdateMode.VALUE_CHANGED, 
              fit_columns_on_grid_load=False,
              allow_unsafe_jscode=True,
              theme='alpine', #Add theme color to the table
              enable_enterprise_modules=True,
              height=350, 
              width='100%',
              reload_data=True
              )
            cost_center = grid_response['data']
            selected_rows = grid_response['selected_rows'] 
            
            return cost_center,selected_rows
            #AgGrid(cost_center_df)  
                
        def sa():
            st.header('DATOS')
            

            def ad():
                st.header('')
                ms1=pd.unique(data['fecha'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Fecha:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = data['fecha']
                else:
                   formulario=formulario
                dataf1=data[(data.fecha.isin(formulario))]
                st.write(dataf1)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf1)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
                
                
                
                total_1=pd.concat([petty,resource,supplier_registration,supplier,delivery_control_and_return])
                total_2=pd.concat([expense_reimbursement_ratio,administrative_purchase_order])
                total_3=pd.concat([certificate,review,F_AD_31,data_automation,reassessment,F_AD_22_B])
                
                #st.write(petty)
                sabana=pd.concat([total_1,total_2,total_3])
                #st.write(sabana)
                sabana['fecha_version'] = (
                    pd.to_datetime(sabana['fecha_version'], errors='coerce', dayfirst=True)
                    .dt.strftime('%d-%m-%Y')
                    )
            
                ad=sabana[sabana['codigo'].str.contains("AD")]
              
                ms1=pd.unique(ad['codigo'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Formulario:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = ad['codigo']
                else:
                   formulario=formulario
                dataf=ad[(ad.codigo.isin(formulario))]
                st.write(dataf)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
            def com():
                st.header('')
                             
                total_1=pd.concat([cccgp, job,request,wage,staff,emotional])
                total_6=pd.concat([df,project, vacation,training,F_TH_10])
                total_3=pd.concat([supervision,billing_information])
                total_4=pd.concat([control,F_TH_22,F_TH_24,F_TH_27,F_SG_07,F_SG_08,F_SG_10])
                total_5=pd.concat([F_SG_38,F_ST_05,F_ST_06,F_ST_07,F_ST_11,F_ST_12])
                
                sabana=pd.concat([total_1,total_3,total_4,total_5,total_6])
                sabana['fecha_version'] = (
                    pd.to_datetime(sabana['fecha_version'], errors='coerce', dayfirst=True)
                    .dt.strftime('%d-%m-%Y')
                    )
            
                com=sabana[sabana['codigo'].str.contains("CON")]
                
                ms1=pd.unique(com['codigo'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Formulario:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = com['codigo']
                else:
                   formulario=formulario
                dataf=com[(com.codigo.isin(formulario))]
                st.write(dataf)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
                
            def th():
                st.header('')
                
                
                               
                total_1=pd.concat([cccgp,project,vacation,F_TH_27,training])
                total_2=pd.concat([F_TH_24,F_TH_22,job,F_TH_10,F_TH_10,staff,emotional])
                
    
                sabana=pd.concat([total_1,total_2])
                sabana['fecha_version'] = (
                    pd.to_datetime(sabana['fecha_version'], errors='coerce', dayfirst=True)
                    .dt.strftime('%d-%m-%Y')
                    )
            
                th=sabana[sabana['codigo'].str.contains("TH")]
                ms1=pd.unique(th['codigo'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Formulario:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = th['codigo']
                else:
                   formulario=formulario
                dataf=th[(th.codigo.isin(formulario))]
                st.write(dataf)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
            
            def sg():
                st.header('')
                
                total_1=pd.concat([F_SG_38,F_SG_07,F_SG_08,F_SG_10])
           
                sabana=pd.concat([total_1])
                sabana['fecha_version'] = (
                    pd.to_datetime(sabana['fecha_version'], errors='coerce', dayfirst=True)
                    .dt.strftime('%d-%m-%Y')
                    )
            
                sg=sabana[sabana['codigo'].str.contains("SG")]
                ms1=pd.unique(sg['codigo'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Formulario:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = sg['codigo']
                else:
                   formulario=formulario
                dataf=sg[(sg.codigo.isin(formulario))]
                st.write(dataf)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
                
            def fst():
                st.header('')

                total_5=pd.concat([F_ST_05,F_ST_06,F_ST_07,F_ST_11,F_ST_12])
      
                sabana=pd.concat([total_5])
                sabana['fecha_version'] = (
                    pd.to_datetime(sabana['fecha_version'], errors='coerce', dayfirst=True)
                    .dt.strftime('%d-%m-%Y')
                    )
            
                fst=sabana[sabana['codigo'].str.contains("ST")]
                ms1=pd.unique(fst['codigo'])
                ms2=np.append(ms1,"Todos")
                formulario= st.sidebar.multiselect(
                            "Formulario:",
                            ms2,
                            default='Todos'
                            )
                if "Todos" in formulario: 
                   formulario = fst['codigo']
                else:
                   formulario=formulario
                dataf=fst[(fst.codigo.isin(formulario))]
                st.write(dataf)
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
                    #Indicate workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Hoja1']
                    
                    for i, col in enumerate(df.columns):
            # find length of column i
                     column_len = df[col].astype(str).str.len().max()
                     # Setting the length if the column header is larger
                     # than the max column value length
                     column_len = max(column_len, len(col)) + 2
                     # set the column length
                     worksheet.set_column(i, i, column_len)
                     writer.save()
                     processed_data = output.getvalue()
                     return processed_data   

                Lab_xlsx = to_excel(dataf)
                st.download_button(label='Resultados',
                                        data=Lab_xlsx ,
                                        file_name= 'df_test.xlsx') 
            
            filpre=st.sidebar.selectbox('',options=['AD','CON','TH','SG','ST'])
            if filpre == 'AD':
                ad()
            elif filpre == 'CON':
                com()
            elif filpre == 'TH':
                th()
            elif filpre == 'SG':
                sg()
            elif filpre == 'ST':
                fst()

            

            #df_1['fecha_version'] = pd.to_datetime(df_1['fecha_version'], format='%Y/%m/%d').dt.strftime('%d-%m-%Y')
            
            

                
            

            
        def em():
            st.header('EMPLEADOS')
            
            
            mujer=employees['sexo'].str.contains('F').value_counts()[True]
            man=employees['sexo'].str.contains('M').value_counts()[True]
            
            a1,a2,a3=st.columns(3)
            a1.metric(label='TOTAL', value=employees['empleado'].count())
            a2.metric(label='MUJERES', value=mujer)
            a3.metric(label='HOMBRES', value=man)
            
               
            maxi=employees['salario'].astype(int).max()
            mini=employees['salario'].astype(int).min()
            #nb_deputies = employees['salario']
            st.write(sorteo) 
            nb_mbrs = st.select_slider("salario",sorteo['salario'],value=(mini,maxi))
            #st.write((sorteo['salario']<= ) & (sorteo['salario'].min()))
            mask_mbrs =sorteo[(sorteo['salario'] <= nb_mbrs[1]) & (sorteo['salario'] >= nb_mbrs[0])]
            
            #mask_mbrs = sorteo.between(nb_mbrs[0], nb_mbrs[1]).to_frame()
            st.write(mask_mbrs)
            def to_excel(df):
             output = BytesIO()
             writer = pd.ExcelWriter(output, engine='xlsxwriter')
             df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
             #Indicate workbook and worksheet for formatting
             workbook = writer.book
             worksheet = writer.sheets['Hoja1']

             #Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
             for i, col in enumerate(df.columns):
        # find length of column i
                 column_len = df[col].astype(str).str.len().max()
                 # Setting the length if the column header is larger
                 # than the max column value length
                 column_len = max(column_len, len(col)) + 2
                 # set the column length
                 worksheet.set_column(i, i, column_len)
             writer.save()
             processed_data = output.getvalue()
             return processed_data   
         #def to_excel(dataf):
          #          output = BytesIO()
           #         writer = pd.ExcelWriter(output, engine='xlsxwriter')
            #        dataf.to_excel(writer, index=False, sheet_name='Sheet1')
             #       workbook = writer.book
              #      worksheet = writer.sheets['Sheet1']
               #     format1 = workbook.add_format({'num_format': '0.00'}) 
                #    worksheet.set_column('A:A', None, format1)  
                 #   writer.save()
                  #  processed_data = output.getvalue()
                   # return processed_data
            Lab_xlsx = to_excel(mask_mbrs)
            st.download_button(label='Resultados en XLSX',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')             
            
       
        filpre=st.sidebar.selectbox('',options=['Centros de Costos','Empleados','Datos'])
        if filpre == 'Centros de Costos':
            cc()
        elif filpre == 'Empleados':
            em()
        elif filpre == 'Datos':
            sa()
        
        
    
    #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
    #-----------------------------------NOVEDADES---------------------------------
    #-----------------------------------------------------------------------------    
    def tab(Lab):
        st.header('')
        def edu(Lab):
         st.header('')
         
         
         mes= st.sidebar.selectbox(
                     "Mes:",
                     pd.unique(data['año_mes']),
                     index=len(pd.unique(data['año_mes']))-1
                     )
         dataf=data[(data.año_mes == mes)]
         ms1=pd.unique(dataf['centro_de_costos'])
         ms2=np.append(ms1,"Todos")
                 
         cent_cost_filter= st.sidebar.selectbox(
                     "Centro Costos:",
                     ms2,
                     index=len(ms2)-1
                     )
         if "Todos" in cent_cost_filter: 
            cent_cost_filter = dataf['centro_de_costos']
         else:
            cent_cost_filter=[cent_cost_filter]
         dataf=dataf[(dataf.centro_de_costos.isin(cent_cost_filter))]
         cd1=pd.unique(dataf['nombre_del_empleado'])
         cd2=np.append(cd1,"Todos")
         empleado = st.sidebar.selectbox(
                "Empleado:",
                cd2,
                index=len(cd2)-1
                ) 
         if "Todos" in empleado: 
            empleado = dataf['nombre_del_empleado']
         else:
            empleado=[empleado]
        
         data_selection=dataf[(dataf.nombre_del_empleado.isin(empleado)) & (dataf.año_mes==mes)]
         
         st.subheader("Novedades")
        #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
         fig2 = make_subplots()
         fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
         colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(75, 177, 61, 1)","rgb(224, 231, 104)","rgb(124, 144, 132)","rgb(63, 140, 90, 1)"]
         

         for t,c in zip(data_selection.tipo_de_novedad.unique(),colors):
            plot_df = data_selection[data_selection.tipo_de_novedad == t]
            fig2.add_trace(go.Bar(name=t,
                                  x=plot_df.nombre_del_empleado,
                                  y=plot_df.dias_laborados,
                                  text=plot_df.dias_laborados,
                                  marker_color=c))
                    
         fig2.update_layout(title_text='Empleados Por Novedad',title_x=0.5,barmode="stack") 
         fig2.update_yaxes(
             title_text = "Dias Laborados")
         st.plotly_chart(fig2,use_container_width=True)
       
#------------------------------------------------------------------------------------------------------        
         colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(124, 144, 132)","rgb(224, 231, 104)"]
         fig3 = px.pie(data_selection, values='dias_laborados', names='tipo_de_novedad', color_discrete_sequence=colors
                       ,#title='Novedad Mensual Por Centro De Costos'
                       )
         fig3.update_layout(legend=dict(orientation="h"))
         st.plotly_chart(fig3,use_container_width=True)
         #fig3.update_layout(title='Novedad Mensual Por Centro De Costos',title_x=0.5) 
         #st.plotly_chart(fig3,use_container_width=True)
#------------------------------------------------------------------------------------------------------        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #Tipo2=pd.merge(data_selection,tip_nov,left_on='tipo_de_novedad',right_on='uuid')   
        #data_selection['Tipo Novedad']=Tipo2['novedad'].values
        #empleados_centro=employees[employees.centro_de_costo.isin(cent_cost_filter)]
         cc_seleccionado=cost_center[cost_center.centro_de_costo.isin(cent_cost_filter)]
         empleados_centro=cc_seleccionado.explode('empleados')
         empleados_centro=empleados_centro.empleados.apply(pd.Series)
       
        #empleados_centro=employees[employees.identificacion.astype(str).isin(data_selection.documento_de_identificacion.astype(str))]
         data_selection=pd.merge(empleados_centro.astype(str),data_selection.astype(str),how='left',left_on='identificacion',right_on='documento_de_identificacion')
         data_selection['dias_laborados']=data_selection['dias_laborados'].fillna(0).astype(int)
         data_selection['nombre_del_empleado']=data_selection['empleado_x']
         por_tra = (data_selection['dias_laborados']/30)*100
         data_selection['Por_tra']=por_tra
        
        #st.write(data_selection[['nombre_del_empleado','documento_de_identificacion','centro_de_costos','dias_laborados','año_mes','Tipo Novedad']])
         data_selection['Alerta']=""
         for i in data_selection['nombre_del_empleado'].index:
          if data_selection.loc[i,'dias_laborados'] == 30:
             data_selection.loc[i,'Alerta'] = "OK"
          else:
             data_selection.loc[i,'Alerta'] = "Revisar"
        
        #data_selection['Aprobado']=""
        #for i in data_selection['nombre_del_empleado'].index:
         #  if data_selection.loc[i,'dias_laborados'] == 0:
           #   data_selection.loc[i,'Aprobado'] = "Sin Aprobar"
          # else:
            #  data_selection.loc[i,'Aprobado'] = "Aprobados"                  
        
        
         #revisar=data['Alerta'].str.contains('Revisar').value_counts()[True]
         #ok=data['Alerta'].str.contains('OK').value_counts()[True]
        
         #c1,c2=st.columns(2)
         #c1.metric(label='REVISAR', value=revisar)
         #c2.metric(label='OK', value=ok)


        #data_selection[['nombre_del_empleado','documento_de_identificacion','centro_de_costos','dias_laborados','año_mes','tipo_de_novedad','Alerta']]
        
        #------------------------------------------------------------------------
         #fig = make_subplots()
         #fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_text='Control Asistencia',title_x=0.5)
                
         #fig.add_trace(
         #go.Bar(
          #x=data_selection.nombre_del_empleado,
          #y=data_selection['Por_tra'],
          #name='Asistencia',
          #text=data_selection['Por_tra'].map('{:,.2f}%'.format),
          #hovertemplate="<br>".join([
           # "nombre_del_empleado: %{x}",
            #"Porcentaje de trabajo: %{y}"
          #])
          #))
                
         #fig.update_traces(marker_color='rgba(112,110,111,255)',textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
         #fig.update_yaxes(range=[0,100])
         #fig.update_xaxes(title_text="Empleado")
         #st.plotly_chart(fig,use_container_width=True)
    
    #-----------------------------------------------------------------------------
        #fig = make_subplots()
        #fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        #colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(124, 144, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
        #data2=data[data['año_mes'] == mes]
        #for t,c in zip(data2.centro_de_costos.unique(),colors):
         # plot_df = data2[data2.centro_de_costos == t]
          #fig.add_trace(go.Bar(name=t, x=plot_df.dias_laborados, y=plot_df.nombre_del_empleado,orientation ='h',marker_color=c))
        
        #fig.update_layout(title_text='Empleados Por Centro de Costos',title_x=0.5,barmode="stack",xaxis_title='Dias') 
        #plt.title("Mince Pie Consumption Study Results")
        #st.plotly_chart(fig,use_container_width=True)
#-----------------------------------------------------------------------------
         st.header("Reporte Novedades")
         data['fecha_inicial_novedad'] = pd.to_datetime(data['fecha_inicial_novedad']) 
         data['fecha_inicial_novedad']=data['fecha_inicial_novedad'].dt.strftime('%Y-%m-%d')
         data['fecha_final_novedad'] = pd.to_datetime(dataf['fecha_final_novedad']) 
         data['fecha_final_novedad']=dataf['fecha_final_novedad'].dt.strftime('%Y-%m-%d')
         ms1=pd.unique(data['año_mes'])
         ms2=np.append(ms1,"Todos")
         formulario= st.multiselect(
                     "Fecha:",
                     ms2,
                     default='Todos'
                     )
         if "Todos" in formulario: 
            formulario = data['año_mes']
         else:
            formulario=formulario
         dataf1=data[(data.año_mes.isin(formulario))]
         st.write(dataf1)
         def to_excel(df):
             output = BytesIO()
             writer = pd.ExcelWriter(output, engine='xlsxwriter')
             df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
             #Indicate workbook and worksheet for formatting
             workbook = writer.book
             worksheet = writer.sheets['Hoja1']
             
             for i, col in enumerate(df.columns):
     # find length of column i
              column_len = df[col].astype(str).str.len().max()
              # Setting the length if the column header is larger
              # than the max column value length
              column_len = max(column_len, len(col)) + 2
              # set the column length
              worksheet.set_column(i, i, column_len)
              writer.save()
              processed_data = output.getvalue()
              return processed_data   

         Lab_xlsx = to_excel(dataf1)
         st.download_button(label='Resultados',
                                 data=Lab_xlsx ,
                                 file_name= 'df_test.xlsx') 
    #------------------------------------------------------------------------------    

    #-----------------------------------------------------------------------------
         #taps=st.selectbox("Aprobado:",pd.unique(data_selection['Aprobado']))
         #dataf=data_selection[(data_selection.Aprobado == taps)]
         #taps=st.selectbox("Aprobado:",pd.unique(tipo['Aprobado']))
         
         #dataf=tipo[(tipo.Aprobado == taps)]
         st.header("Tabla Sugeridos")
         tipo=data[(data.centro_de_costos.isin(cent_cost_filter)) & (data.año_mes==mes)]
         tipo['Alerta']=""
         for i in tipo['nombre_del_empleado'].index:
          if tipo.loc[i,'dias_laborados'] == 30:
             tipo.loc[i,'Alerta'] = "OK"
          else:
             tipo.loc[i,'Alerta'] = "Revisar"
         
         ms1=pd.unique(tipo['Alerta'])
         ms2=np.append(ms1,"Todos")
         tap=st.selectbox(
                     "Alerta:",
                     ms2,index=len(ms2)-1
                     )
        
         if "Todos" in tap:
             tap=tipo['Alerta']
         else:
             tap=[tap]
         dataf=tipo[(tipo.Alerta.isin(tap))]
         dataf[['nombre_del_empleado','documento_de_identificacion','centro_de_costos',
                'dias_laborados','año_mes','tipo_de_novedad','Alerta']]

         
         dataf=dataf.drop(["uuid","fecha","fecha_observacion","fecha_ingreso_nomina",
                           "empleado","tipo_observacion"],axis=1) 
         dataf.index = np.arange(1, len(dataf) + 1)
         
         dataf['fecha_final_novedad'] = pd.to_datetime(dataf['fecha_final_novedad']) 
         dataf['fecha_final_novedad']=dataf['fecha_final_novedad'].dt.strftime('%Y-%m-%d')
         dataf['fecha_final_novedad'] = pd.to_datetime(dataf['fecha_final_novedad']) 
         dataf['fecha_final_novedad']=dataf['fecha_final_novedad'].dt.strftime('%Y-%m-%d')
         dataf.rename(columns={'quien_reporta_la_novedad':'Quien reporta la novedad',
                        'nombre_del_empleado':'Nombre del Empleado','documento_de_identificacion':'Documento de Identificacion','centro_de_costos':'Centro de Costos',
                        'tipo_de_novedad':'Tipo de Novedad','año_mes':'Año-Mes','dias_a_facturar':'Dias a Facturar',
                        'dias_laborados':'Dias Laborados','fecha_inicial_novedad':'Fecha Inicial Novedad',
                        'fecha_final_novedad':'Fecha Final Novedad'},
               inplace=True)
         st.write(dataf)

         def to_excel(df):
             output = BytesIO()
             writer = pd.ExcelWriter(output, engine='xlsxwriter')
             df.to_excel(writer, index = False, sheet_name='Hoja1',encoding='utf-16')
             #Indicate workbook and worksheet for formatting
             workbook = writer.book
             worksheet = writer.sheets['Hoja1']

             #Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
             for i, col in enumerate(df.columns):
        # find length of column i
                 column_len = df[col].astype(str).str.len().max()
                 # Setting the length if the column header is larger
                 # than the max column value length
                 column_len = max(column_len, len(col)) + 2
                 # set the column length
                 worksheet.set_column(i, i, column_len)
             writer.save()
             processed_data = output.getvalue()
             return processed_data   
         
         Lab_xlsx = to_excel(dataf)
         st.download_button(label='Resultados en Excel',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')  
         
         
         a=list(dataf['Centro de Costos'].unique())
         c=list(cost_center['centro_de_costo'].unique())
         cen_sin=list(set(c)-set(a))
         
         cc_nulos=pd.DataFrame(cen_sin,columns=['Centros De Costo'])
         cc_nulos.index = np.arange(1, len(cc_nulos) + 1)
        
         d=list(dataf['Nombre del Empleado'].unique())
         e=list(employees['empleado'].unique())
         em_sin=list(set(e)-set(d))
         em_nulos=pd.DataFrame(em_sin,columns=['Empleados'])
         em_nulos.index = np.arange(1, len(em_nulos) + 1)
         
         
         st.header("Sin Reporte")
         cc1,cc2=st.columns(2)
         cc1.metric(label='CENTROS DE COSTOS', value=len(cen_sin))
         cc2.metric(label='EMPLEADOS', value=len(em_sin))
         
         tab1, tab2 = st.tabs(["Centros", "Empleados"])
         with tab1:
             st.write(cc_nulos)
         with tab2:
             st.write(em_nulos)
         #st.subheader("Reporte Novedades")         contandito=excel.iloc[:, 0].count()
         
    #-----------------------------------------------------------------------------
         #agru=data.groupby(['nombre_del_empleado','tipo_de_novedad'],as_index=False)['dias_laborados'].sum()
         #st.write(agru)
    #-----------------------------------------------------------------------------           
        def cal(Lab):
            
         st.header('HISTORICO')
         
         ms1=pd.unique(data['centro_de_costos'])
         ms2=np.append(ms1,"Todos")
         vc= st.sidebar.selectbox(
          "Centro de costos:",
          ms2,index=len(ms2)-1
          )
        
         if "Todos" in vc:
             vc=data['centro_de_costos']
         else:
             vc=[vc]
         dataf=data[(data.centro_de_costos.isin(vc))]
         
         dataf=data[(data.centro_de_costos == vc)]
         ms1=pd.unique(dataf['tipo_de_novedad'])
         nov= st.selectbox(
                     "Tipo De Novedad:",
                     ms1,
                     index=len(ms1)-1
                     )
         dataf=dataf[(dataf.tipo_de_novedad == nov)]
         #data_selection = dataf.query("centro_de_costos == @vc")
         data_selection=dataf[(dataf.centro_de_costos.isin(vc)) & (dataf.tipo_de_novedad==nov)]
         data_selection["Mes"] = (pd.to_datetime(data_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
                   .dt.month_name(locale='es_ES.utf8'))
        
         data_selection=data_selection.groupby(['Mes'],as_index=False)['tipo_de_novedad'].count()
         
         fig = make_subplots()
         fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
         colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
         fig.add_trace(go.Bar(x=data_selection['Mes'],
                              y=data_selection['tipo_de_novedad'],
                              marker_color=colors))
         fig.update_layout(title_text='Novedades',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
         fig.update_xaxes(
             title_text = "Mes")
         fig.update_yaxes(
             title_text = "Cantidad de Empleados")
         
         st.plotly_chart(fig,use_container_width=True)     
        
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
        #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
        def admi(Lab):
         st.subheader('Subir Excel Actualizado')
         uploaded_file = st.file_uploader("")
         if uploaded_file is not None:
           
             # To read file as bytes:
           bytes_data = uploaded_file.getvalue()
           #st.write(bytes_data)
                    
           files = {"file":(uploaded_file.name,bytes_data,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}      
           respuesta=cargar.cargar_excel(files)
         
         with st.form("my_form"):
             day_from=cale.loc[cale['format_code'] =='F-NOM-01',['day_from']]
             day_to=cale.loc[cale['format_code'] =='F-NOM-01',['day_to']]
             
 
             today=datetime.datetime.now()
             d = st.date_input(
             "Inserta fecha",
             value=(datetime.datetime(today.year, today.month, int(day_from.values[0])), datetime.datetime(today.year, today.month, int(day_to.values[0]))),
             min_value=datetime.datetime(today.year, today.month, 1),
             max_value=datetime.datetime(today.year, today.month, 28))
             
             submitted = st.form_submit_button("Guardar")
             if submitted:
              cargar.mod_cale(d[0].day, d[1].day)
              cargar.traer_cale.clear()
              st.success('Guardado', icon="✅")
         
         #files = {"file":bytes_data,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        
        subsub=st.sidebar.radio('',options=['Novedades','Historico','Administrador Novedades'])
        
        if subsub == 'Novedades':
            edu(Lab)
        elif subsub == 'Historico':
            cal(Lab)
        elif subsub== 'Administrador Novedades':
            admi(Lab)
    #------------------------------------------------------------------------------
        
        
        
        #st.write(data_selectionn)
    #------------------------------------------------------------------------------    
      
        
        
    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------REEMBOLSOS--------------------------------
    #------------------------------------------------------------------------------
    def re(Lab):
        st.header('')
        def edu(Lab):
            st.header('')  
            def empresa(Lab):
                st.header('')
                c1,c2,c3=st.columns(3)
                c1.metric(label='TOTAL', value='$'+format(df['valor_rembolso'].sum(),','))
                c2.metric(label='CANTIDAD', value=df['valor_rembolso'].count())
                c3.metric(label='PROMEDIO', value=SetMoneda(df['valor_rembolso'].mean(),"$",0))
        
                colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(211,212,21)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                nombres=['APROBADO','DENEGADO']
           
                fig = px.pie(vf, values='reembonsable_al_cliente', names=nombres, color_discrete_sequence=colors)
                fig.update_layout(title_text='Aprobación de reembolsos') 
                st.plotly_chart(fig,use_container_width=True)
           
                dfmes= st.sidebar.selectbox(
                    "Mes:",
                    pd.unique(df['año_mes'])
                    )
                dff=df[(df.año_mes == dfmes)]
                ms1=pd.unique(dff['nombre'])
                ms2=np.append(ms1,"Todos")
    
                df_filter= st.sidebar.selectbox(
                   "Centro Costos:",
                   ms2
                )
                if "Todos" in df_filter: 
                    df_filter = dff['cargar_a_centro_de_costos']
                else:
                    df_filter=[df_filter]
                dff=dff[(dff.nombre.isin(df_filter))]
                cd1=pd.unique(dff['nombres_y_apellidos'])
                cd2=np.append(cd1,"Todos")
                dfempleado = st.sidebar.selectbox(
                    "Empleado:",
                    cd2
                    ) 
                if "Todos" in dfempleado: 
                    dfempleado = dff['nombres_y_apellidos']
                else:
                    dfempleado=[dfempleado]
        
                data_selection=dff[(dff.nombres_y_apellidos.isin(dfempleado)) & (dff.año_mes==dfmes)]
        #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
                
                st.write(data_selection[['nombres_y_apellidos','numero_cc','nombre','valor_rembolso','año_mes']])
                def to_excel(df_selection):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    data_selection.to_excel(writer, index=False, sheet_name='Sheet1')
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    format1 = workbook.add_format({'num_format': '0.00'}) 
                    worksheet.set_column('A:A', None, format1)  
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data
                Lab_xlsx = to_excel(data_selection)
                st.download_button(label='Resultados en XLSX',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')
        
            def CCCGP(Lab):
                st.header('')
            
                centroc= st.sidebar.selectbox(
                    "Centro de costos:",
                    pd.unique(reem['nombre'])
                    )
                dataf3=reem[(reem.nombre == centroc)]
                data_selection3=dataf3.query("nombre== @centroc")    
        
                fig = make_subplots()
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                fig.add_trace(go.Bar(x=data_selection3['valor_rembolso'], y=data_selection3['nombres_y_apellidos'], orientation='h',marker_color=colors))
                fig.update_layout(title_text='Empleado Con Más Reembolsos Solicitados',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig,use_container_width=True)
    #------------------------------------------------------------------------------
                mes= st.sidebar.selectbox(
                    "Mes:",
                    pd.unique(cant['año_mes'])
                    )
                dataf4=cant[(cant.año_mes == mes)]
                data_selection4 = dataf4.query("año_mes == @mes")
        
                fig = make_subplots()
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                fig.add_trace(go.Bar(y=data_selection4['valor_rembolso'], x=data_selection4['nombre'],marker_color=colors))
                fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig,use_container_width=True)
                
            
        
      
            def FE(Lab):
                st.header((''))
            
                centro= st.sidebar.selectbox(
                    "Centro de costos:",
                    pd.unique(cant['nombre'])
                    )
                dataf=cant[(cant.nombre == centro)]
                dataf2=contar[(contar.nombre == centro)]
                data_selection = dataf.query("nombre == @centro")
                data_selection2 = dataf2.query("nombre == @centro")
                data_selection["Mes"] = (pd.to_datetime(data_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
                   .dt.month_name(locale='es_ES.utf8'))
        
                metrica=data_selection['valor_rembolso'].sum()
        #filtro=st.selectbox('Centro de costos',cant['cargar_a_centro_de_costos'].unique())
                d1,d2=st.columns(2)
                d1.metric(label='TOTAL', value='$'+'{:,}'.format(metrica))
                d2.metric(label='CANTIDAD',value=data_selection2['valor_rembolso'])
              
         
                fig = make_subplots()
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                fig.add_trace(go.Bar(y=data_selection['valor_rembolso'], x=data_selection['Mes'],marker_color=colors))
                fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig,use_container_width=True)
            
            
            subfiltro=st.sidebar.selectbox('Tipo de Prestamo', options=['Analisis General','Comparativo','Historico'])
        
            if subfiltro == 'Analisis General':
                empresa(Lab)
            elif subfiltro == 'Comparativo':
                CCCGP(Lab)
            elif subfiltro == 'Historico':
                FE(Lab)
        def cal(Lab):
                st.header('')
                def empresa(Lab):
                    st.header('')
                    c1,c2,c3=st.columns(3)
                    c1.metric(label='TOTAL', value='$'+format(cm['total'].sum(),','))
                    c2.metric(label='CANTIDAD', value=cm['total'].count())
                    c3.metric(label='PROMEDIO', value=SetMoneda(cm['total'].mean(),"$",0))
         
                    factura=cm['tipo_de_documento'].str.contains('factura').value_counts()[True]
                    vale=cm['tipo_de_documento'].str.contains('vale').value_counts()[True]
                    cuenta=cm['tipo_de_documento'].str.contains('cuenta').value_counts()[True]
                    
                    d1,d2,d3=st.columns(3)
                    d1.metric(label='FACTURA', value=factura)
                    d2.metric(label='VALE', value=vale)
                    d3.metric(label='CUENTA DE COBRO', value=cuenta)
         
            
         
                    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(211,212,21)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                    nombres=['APROBADO','DENEGADO']
                    
                    fig = px.pie(cmv, values='reembonsable_al_cliente', names=nombres, color_discrete_sequence=colors)
                    fig.update_layout(title_text='Aprobación de reembolsos') 
                    st.plotly_chart(fig,use_container_width=True)
           
                    dfmes= st.sidebar.selectbox(
                        "Mes:",
                        pd.unique(cm['año_mes'])
                        )
                    dff=cm[(cm.año_mes == dfmes)]
                    ms1=pd.unique(dff['cargar_a_centro_de_costos'])
                    ms2=np.append(ms1,"Todos")
    
                    df_filter= st.sidebar.selectbox(
                        "Centro Costos:",
                        ms2
                        )
                    if "Todos" in df_filter: 
                        df_filter = dff['cargar_a_centro_de_costos']
                    else:
                        df_filter=[df_filter]
                    dff=dff[(dff.cargar_a_centro_de_costos.isin(df_filter))]
                    cd1=pd.unique(dff['nombres_y_apellidos'])
                    cd2=np.append(cd1,"Todos")
                    dfempleado = st.sidebar.selectbox(
                        "Empleado:",
                        cd2
                        ) 
                    if "Todos" in dfempleado: 
                        dfempleado = dff['nombres_y_apellidos']
                    else:
                        dfempleado=[dfempleado]
                    datacm_selection=dff[(dff.nombres_y_apellidos.isin(dfempleado)) & (dff.año_mes==dfmes)]
                    
                    
                    
            
            
                     #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
       
                    st.write(datacm_selection[['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos','total','año_mes']])
                    def to_excel(df_selection):
                        output = BytesIO()
                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                        datacm_selection.to_excel(writer, index=False, sheet_name='Sheet1')
                        workbook = writer.book
                        worksheet = writer.sheets['Sheet1']
                        format1 = workbook.add_format({'num_format': '0.00'}) 
                        worksheet.set_column('A:A', None, format1)  
                        writer.save()
                        processed_data = output.getvalue()
                        return processed_data
                    Lab_xlsx = to_excel(datacm_selection)
                    st.download_button(label='Resultados en XLSX',
                                    data=Lab_xlsx ,
                                    file_name= 'df_test.xlsx')
        
                def CCCGP(Lab):
                    st.header('')
    
                    centroc= st.sidebar.selectbox(
                        "Centro de costos:",
                        pd.unique(reemcm['cargar_a_centro_de_costos'])
                        )
                    datafcm3=reemcm[(reemcm.cargar_a_centro_de_costos == centroc)]
                    datacm_selection3=datafcm3.query("cargar_a_centro_de_costos== @centroc")    
        
                    fig = make_subplots()
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(128, 162, 13)","rgb(147, 148, 132)","rgb(176,189, 133)","rgb(119,134,68)"]
                    fig.add_trace(go.Bar(x=datacm_selection3['total'], y=datacm_selection3['nombres_y_apellidos'], orientation='h',marker_color=colors))
                    fig.update_layout(title_text='Empleado Con Más Reembolsos Solicitados',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig,use_container_width=True)
    #------------------------------------------------------------------------------
                    mes= st.sidebar.selectbox(
                        "Mes:",
                        pd.unique(cantcm['año_mes'])
                        )
                    datafcm4=cantcm[(cantcm.año_mes == mes)]
                    datacm_selection4 = datafcm4.query("año_mes == @mes")
                    
                    fig = make_subplots()
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(128, 162, 13)","rgb(147, 148, 132)","rgb(176,189, 133)","rgb(119,134,68)"]
                    fig.add_trace(go.Bar(y=datacm_selection4['total'], x=datacm_selection4['cargar_a_centro_de_costos'],marker_color=colors))
                    fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig,use_container_width=True)
                
            
        
      
                def FE(Lab):
                    st.header((''))
                    
                    centro= st.sidebar.selectbox(
                        "Centro de costos:",
                        pd.unique(cantcm['cargar_a_centro_de_costos'])
                        )
                    datafcm=cantcm[(cantcm.cargar_a_centro_de_costos == centro)]
                    datafcm2=contarcm[(contarcm.cargar_a_centro_de_costos == centro)]
                    datacm_selection = datafcm.query("cargar_a_centro_de_costos == @centro")
                    datacm_selection2 = datafcm2.query("cargar_a_centro_de_costos == @centro")
                    datacm_selection["Mes"] = (pd.to_datetime(datacm_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
                                             .dt.month_name(locale='es_ES.utf8'))
                    datacm_selection['tipo_de_documento']=cm['tipo_de_documento']
                    metrica=datacm_selection['total'].sum()
                   
        #filtro=st.selectbox('Centro de costos',cant['cargar_a_centro_de_costos'].unique())
                    d1,d2=st.columns(2)
                    d1.metric(label='TOTAL', value='$'+'{:,}'.format(metrica))
                    d2.metric(label='CANTIDAD',value=datacm_selection2['total'])
              
                    
         
                    fig = make_subplots()
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
                    fig.add_trace(go.Bar(y=datacm_selection['total'],
                                         x=datacm_selection['Mes'],
                                         text=datacm_selection['total'].map('{:,}'.format),
                                         marker_color=colors))
                    fig.update_layout(title_text='Historico Mensual',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig,use_container_width=True)
                
                    fig = make_subplots()
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                    colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(128, 162, 13)","rgb(147, 148, 132)","rgb(176,189, 133)","rgb(119,134,68)"]
                    fig.add_trace(go.Bar(x=datacm_selection['tipo_de_documento'], y=datacm_selection['total'],marker_color=colors))
                    fig.update_layout(title_text='Documento Mas Solicitado',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig,use_container_width=True)
                    
                subfiltro=st.sidebar.selectbox('Tipo de Prestamo', options=['Analisis General','Comparativo','Historico'])
        
                if subfiltro == 'Analisis General':
                    empresa(Lab)
                elif subfiltro == 'Comparativo':
                    CCCGP(Lab)
                elif subfiltro == 'Historico':
                     FE(Lab)
        
        
        
        
        
        
        
        def con(Lab):
            st.header('')
                
        def fac(Lab):
            st.header((''))
            
        def cal(Lab):
            st.header((''))
        
        subsub=st.sidebar.radio('',options=['Reembolsos','F-AD-07 Caja Menor'])
        if subsub == 'Reembolsos':
            edu(Lab)
        elif subsub == 'F-AD-07 Caja Menor':
            cal(Lab)
        elif subsub == 'F-AD-31 Ingreso Contratistas':
            con(Lab)    
        elif subsub == 'F-AD-31 Revisión de Facturas Y/O CUENTAS DE COBRO':
            fac(Lab)
        #st.write(vf2)    
        #dataf3=vf2[(vf2.index == centro)]
        #data_selection3=dataf3.query("cargar_a_centro_de_costos == @centro")
        #st.write(data_selection3)
        #fig = px.pie(data_selection3, values=['False' & 'True'], names=nombres, color_discrete_sequence=colors)
        #fig.update_layout(title_text='Aprobación de reembolsos') 
        #st.plotly_chart(fig,use_container_width=True)
         
        #dataf3=df[(df.cargar_a_centro_de_costos==centro)]
        #fig=dataf3.plot(kind='pie',y=['reembonsable_al_cliente'])
        
    #-----------------------------------------------------------------------------    
     
    #------------------------------------------------------------------------------
       
        
    #-----------------------------------------------------------------------------    
    #-----------------------------------------------------------------------------
    #-------------------------------PRESTAMOS-------------------------------------
    #------------------------------------------------------------------------------    
    def prest(Lab):
        st.header('')
     
        def empresa(Lab):
            st.header('Empresa')
        
        
        def CCCGP(Lab):
            st.header('CCCGP')
            
            def edu(Lab):
                st.header('Educación')
                
            def cal(Lab):
                st.header('Calamidad')
                
            subsub=st.sidebar.radio('',options=['Educación','Calamidad'])
            if subsub == 'Educación':
                edu(Lab)
            elif subsub == 'Calamidad':
                cal(Lab)
            
        
      
        def FE(Lab):
            st.header(('Fondo Empleados'))
            
            centro= st.sidebar.selectbox(
            "Centro de costos:",
            pd.unique(cantpr['centro_de_costos'])
            )
            datapr=cantpr[(cantpr.centro_de_costos == centro)]
            datapr2=contarpr[(contarpr.centro_de_costos == centro)]
            datapr_selection = datapr.query("centro_de_costos == @centro")
            datapr_selection2 = datapr2.query("centro_de_costos == @centro")
            datapr_selection["Mes"] = (pd.to_datetime(datapr_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
                   .dt.month_name(locale='es_ES.utf8'))
        
            metrica=datapr_selection['valor_del_prestamo'].sum()
        #filtro=st.selectbox('Centro de costos',cant['cargar_a_centro_de_costos'].unique())
            d1,d2=st.columns(2)
            d1.metric(label='TOTAL', value='$'+'{:,}'.format(metrica))
            d2.metric(label='CANTIDAD',value=datapr_selection2['valor_del_prestamo'])
        
         
            fig = make_subplots()
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
            fig.add_trace(go.Bar(y=datapr_selection['valor_del_prestamo'], 
                                 x=datapr_selection['Mes'],
                                 marker_color=clors,
                                 text=pr.groupby(['centro_de_costos','año_mes'])['valor_del_prestamo'].sum(),
                                 textposition='outside'))
            #fig.update_traces(texttemplate='{valor_del_prestamo:.2s}', textposition='outside')
            fig.update_layout(
                title_text='Centro De Costos Con Más Reembolsos Por Mes',
                title_x=0.5,
                barmode='stack', 
                yaxis={'categoryorder':'total ascending'},
                )
            st.plotly_chart(fig,use_container_width=True)
            
            
        subfiltro=st.sidebar.selectbox('Tipo de Prestamo', options=['Empresas','CCCGP','Fondo Empleados'])
        
        if subfiltro == 'Empresas':
           empresa(Lab)
        elif subfiltro == 'CCCGP':
           CCCGP(Lab)
        elif subfiltro == 'Fondo Empleados':
           FE(Lab)
    
    
    options=st.sidebar.selectbox('',options=opt)
    
    
    
    
    
    if options == 'Nómina':
       tab(Lab)
    elif options == 'Administrativa':
       re(Lab)
    elif options == 'Prestamos':
       prest(Lab)
    elif options == 'PREVEO':
       preveo()
    
