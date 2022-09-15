import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import datetime
#import matplotlib
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from PIL import Image
import os
import cargar
import datatable as dt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import markdown
from typing import List, Optional
#from tkinter import * from tkinter.ttk import *

cost_center, employees, data,tip_nov =cargar.cargar_info()
 
with open('styles.css') as f:
    
    st.markdown(f"""<style>
                {f.read()}
                </style>"""
    , unsafe_allow_html=True)


pr=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-NOM-02/find_query.xlsx")
pr2=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-NOM-02/find_query.xlsx")
pr['año_mes']=pd.to_datetime(pr['fecha'])
cantpr=pr.groupby(['centro_de_costos','año_mes'],as_index=False)['valor_del_prestamo'].sum()
contarpr=pr.groupby(['centro_de_costos'],as_index=False)['valor_del_prestamo'].count()


#------------------------------------------------------------------------------
df=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/F-AD-05/find_query.xlsx")
#df['valor_rembolso']=format(df['valor_rembolso'])
reem=df.groupby(['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos'],as_index=False)['valor_rembolso'].sum()
top=reem.head(5)
vf=df['reembonsable_al_cliente'].value_counts()
df['vf']=vf
vf2=df.groupby(['cargar_a_centro_de_costos','reembonsable_al_cliente']).size().unstack(fill_value=0)
df['año_mes']=df['pagado.0.recibo_o_factura.fecha'].dt.strftime('%Y-%m')
cant=df.groupby(['cargar_a_centro_de_costos','año_mes'],as_index=False)['valor_rembolso'].sum()
topcenter=cant.head(5)
contar=df.groupby(['cargar_a_centro_de_costos'],as_index=False)['valor_rembolso'].count()
men=df.groupby(['pagado.0.recibo_o_factura.fecha'],as_index=False)['valor_rembolso'].sum
#-----------------------------------------------------------------------------
#data = pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/LUCRO/prueba.xlsx")
data=data.drop(["codigo_centro_de_costos","observaciones"],axis=1) 
data.columns = data.columns.str.replace(' ', '_') 
data['fecha_inicial_novedad'] = pd.to_datetime(data['fecha_inicial_novedad'], errors='coerce')
data['fecha_final_novedad'] = pd.to_datetime(data['fecha_final_novedad'], errors='coerce')
data['documento_de_identificacion'] = data['documento_de_identificacion'].astype(str)
data['año_mes']=data['fecha_inicial_novedad'].dt.strftime('%Y-%m')
#graf=data.groupby(['nombre_del_empleado','centro_de_costos'])['dias_laborados']   
#Fac = data.groupby(['Nombre Del Empleado', 'Documento De Identificacion'])['Dias Laborados'].sum() 
data['empleado']=data['nombre_del_empleado']+ "-" +data["documento_de_identificacion"]

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


        
#-----------------------------------------------------------------------------
emplea=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/EMPLEADOS/em.xlsx")
emplea['salario']=emplea['salario'].replace({',':''}, regex=True)
emplea['salario']=emplea['salario'].astype(int)
sorteo=emplea.sort_values(by='salario')
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

# get current working directory
#cwd = os.getcwd()
#get files in directory
#files = os.listdir(cwd) 

#print(files)

with st.sidebar.container():
 image =Image.open('C:/Users/VALE/Dropbox/PC/Documents/LUCRO/PREVEO5.png') 
 new_image = image.resize((200, 175))
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
def preveo(Lab):
    st.header('')
    
    def cc(Lab):
        st.header('CENTROS DE COSTOS')
     
        cost_center=pd.read_excel("C:/Users/VALE/Dropbox/PC/Documents/PREVEO/preveo/COST_CENTER/cc.xlsx")
        cost_center=cost_center.fillna('No_Aplica')
        cost_center['vigencia_del_proyecto'] = cost_center['vigencia_del_proyecto'].replace(
         { "NO": 'NO_VIGENTE'})
        cost_center['vigencia_del_proyecto']=cost_center['vigencia_del_proyecto'].str.upper()
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
            
        
        
        
        
        
    def em(Lab):
        st.header('EMPLEADOS')
        
        
        mujer=emplea['sexo'].str.contains('F').value_counts()[True]
        man=emplea['sexo'].str.contains('M').value_counts()[True]
        
        a1,a2,a3=st.columns(3)
        a1.metric(label='TOTAL', value=emplea['empleado'].count())
        a2.metric(label='MUJERES', value=mujer)
        a3.metric(label='HOMBRES', value=man)
        
           
        maxi=emplea['salario'].astype(int).max()
        mini=emplea['salario'].astype(int).min()
        #nb_deputies = employees['salario']
        nb_mbrs = st.select_slider("salario",sorteo['salario'],value=(mini,maxi))
        mask_mbrs = emplea['salario'].between(nb_mbrs[0], nb_mbrs[1]).to_frame()
        df_dep_filtered =emplea[mask_mbrs]
        st.write(df_dep_filtered)
        st.write(emplea)
        
   
    filpre=st.sidebar.selectbox('',options=['Centros de Costos','Empleados'])
    if filpre == 'Centros de Costos':
        cc(Lab)
    elif filpre == 'Empleados':
        em(Lab)
    
    
    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------NOVEDADES---------------------------------
#-----------------------------------------------------------------------------    
def tab(Lab):
    st.header('')
    
    def edu(Lab):
     st.header('NOVEDADES')
     mes= st.sidebar.selectbox(
                 "Mes:",
                 pd.unique(data['año_mes'])
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
   
    #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
    
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
     
     fig2 = make_subplots()
     fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
     colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(211,212,21)","rgb(224, 231, 104)","rgb(124, 144, 132)","rgb(63, 140, 90, 1)"]
     
     tipo=data[(data.centro_de_costos.isin(cent_cost_filter)) & (data.año_mes==mes)]
     tipo['Alerta']=""
     for i in tipo['nombre_del_empleado'].index:
      if tipo.loc[i,'dias_laborados'] == 30:
         tipo.loc[i,'Alerta'] = "OK"
      else:
         tipo.loc[i,'Alerta'] = "Revisar"
     tap=st.selectbox(
                 "Alerta:",
                 pd.unique(tipo['Alerta'])
                 )
     dataf=tipo[(tipo.Alerta == tap)]
     for t,c in zip(dataf.tipo_de_novedad.unique(),colors):
        plot_df = dataf[dataf.tipo_de_novedad == t]
        fig2.add_trace(go.Bar(name=t,
                              x=plot_df.nombre_del_empleado,
                              y=plot_df.dias_laborados,
                              text=plot_df.dias_laborados,
                              marker_color=c))
                
     fig2.update_layout(title_text='Empleados Por Novedad',title_x=0.5,barmode="stack") 
     st.plotly_chart(fig2,use_container_width=True)
   
#------------------------------------------------------------------------------    
     colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(124, 144, 132)","rgb(224, 231, 104)"]
     fig3 = px.pie(tipo, values='dias_laborados', names='tipo_de_novedad', color_discrete_sequence=colors)
     fig3.update_layout(title_text='Novedad Mensual Por Centro De Costos',title_x=0.5) 
     st.plotly_chart(fig3,use_container_width=True)
#-----------------------------------------------------------------------------
     data_selection[['nombre_del_empleado','documento_de_identificacion','centro_de_costos','dias_laborados','año_mes','tipo_de_novedad','Alerta']]    
            
     def to_excel(data_selection):
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
#-----------------------------------------------------------------------------
     #agru=data.groupby(['nombre_del_empleado','tipo_de_novedad'],as_index=False)['dias_laborados'].sum()
     #st.write(agru)
#-----------------------------------------------------------------------------           
    def cal(Lab):
     st.header('HISTORICO')
   
     vc= st.sidebar.selectbox(
      "Centro de costos:",
      pd.unique(data['centro_de_costos'])
      )
     dataf=data[(data.centro_de_costos == vc)]
     ms1=pd.unique(dataf['tipo_de_novedad'])
                  
     nov= st.selectbox(
                 "Tipo De Novedad:",
                 ms1,
                 index=len(ms1)-1
                 )
     dataf=dataf[(dataf.tipo_de_novedad == nov)]
     data_selection = dataf.query("centro_de_costos == @vc")
     data_selection["Mes"] = (pd.to_datetime(data_selection['año_mes'], format='%Y.%m.%d', errors="coerce")
               .dt.month_name(locale='es_ES.utf8'))
    
     fig = make_subplots()
     fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
     colors=["rgb(211,212,21)","rgba(112,110,111,255)","rgb(164,164,164)","rgb(224, 231, 104)","rgb(224, 231, 104)","rgb(147, 148, 132)","rgb(224, 231, 104)","rgb(224, 231, 104)"]
     fig.add_trace(go.Bar(y=data_selection['tipo_de_novedad'].value_counts(), x=data_selection['Mes'],marker_color=colors))
     fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
     st.plotly_chart(fig,use_container_width=True)     
    
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    subsub=st.sidebar.radio('',options=['Novedades','Historico'])
    if subsub == 'Novedades':
        edu(Lab)
    elif subsub == 'Historico':
        cal(Lab)
    
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
        st.header('General')  
        def empresa(Lab):
            st.header('')
            c1,c2,c3=st.columns(3)
            c1.metric(label='TOTAL', value='$'+format(df['valor_rembolso'].sum(),','))
            c2.metric(label='CANTIDAD', value=df['valor_rembolso'].count())
            c3.metric(label='PROMEDIO', value=SetMoneda(df['valor_rembolso'].mean(),"$",2))
    
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
    
            data_selection=dff[(dff.nombres_y_apellidos.isin(dfempleado)) & (dff.año_mes==dfmes)]
    #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
   
            st.write(data_selection[['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos','valor_rembolso','año_mes']])
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
                pd.unique(reem['cargar_a_centro_de_costos'])
                )
            dataf3=reem[(reem.cargar_a_centro_de_costos == centroc)]
            data_selection3=dataf3.query("cargar_a_centro_de_costos== @centroc")    
    
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
            fig.add_trace(go.Bar(y=data_selection4['valor_rembolso'], x=data_selection4['cargar_a_centro_de_costos'],marker_color=colors))
            fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig,use_container_width=True)
            
        
    
  
        def FE(Lab):
            st.header((''))
        
            centro= st.sidebar.selectbox(
                "Centro de costos:",
                pd.unique(cant['cargar_a_centro_de_costos'])
                )
            dataf=cant[(cant.cargar_a_centro_de_costos == centro)]
            dataf2=contar[(contar.cargar_a_centro_de_costos == centro)]
            data_selection = dataf.query("cargar_a_centro_de_costos == @centro")
            data_selection2 = dataf2.query("cargar_a_centro_de_costos == @centro")
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
            st.header('Caja Menor')
            def empresa(Lab):
                st.header('')
                c1,c2,c3=st.columns(3)
                c1.metric(label='TOTAL', value='$'+format(df['valor_rembolso'].sum(),','))
                c2.metric(label='CANTIDAD', value=df['valor_rembolso'].count())
                c3.metric(label='PROMEDIO', value=SetMoneda(df['valor_rembolso'].mean(),"$",2))
    
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
    
                data_selection=dff[(dff.nombres_y_apellidos.isin(dfempleado)) & (dff.año_mes==dfmes)]
    #data_selection = dataf.query("centro_de_costos== @cent_cost_filter and nombre_del_empleado == @empleado ")
   
                st.write(data_selection[['nombres_y_apellidos','numero_cc','cargar_a_centro_de_costos','valor_rembolso','año_mes']])
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
                    pd.unique(reem['cargar_a_centro_de_costos'])
                    )
                dataf3=reem[(reem.cargar_a_centro_de_costos == centroc)]
                data_selection3=dataf3.query("cargar_a_centro_de_costos== @centroc")    
    
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
                fig.add_trace(go.Bar(y=data_selection4['valor_rembolso'], x=data_selection4['cargar_a_centro_de_costos'],marker_color=colors))
                fig.update_layout(title_text='Centro De Costos Con Más Reembolsos Por Mes',title_x=0.5,barmode='stack', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig,use_container_width=True)
            
        
    
  
            def FE(Lab):
                st.header((''))
                
                centro= st.sidebar.selectbox(
                    "Centro de costos:",
                    pd.unique(cant['cargar_a_centro_de_costos'])
                    )
                dataf=cant[(cant.cargar_a_centro_de_costos == centro)]
                dataf2=contar[(contar.cargar_a_centro_de_costos == centro)]
                data_selection = dataf.query("cargar_a_centro_de_costos == @centro")
                data_selection2 = dataf2.query("cargar_a_centro_de_costos == @centro")
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
    subsub=st.sidebar.radio('',options=['General','Caja Menor'])
    if subsub == 'General':
        edu(Lab)
    elif subsub == 'Caja Menor':
        cal(Lab)
    
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
                             marker_color=colors,
                             text=pr2.groupby(['centro_de_costos','año_mes'])['valor_del_prestamo'].sum(),
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


options=st.sidebar.selectbox('',options=['PREVEO','Novedades','Reembolsos','Prestamos'])





if options == 'Novedades':
   tab(Lab)
elif options == 'Reembolsos':
   re(Lab)
elif options == 'Prestamos':
   prest(Lab)
elif options == 'PREVEO':
   preveo(Lab)

