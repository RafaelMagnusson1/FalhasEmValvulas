import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando as variáveis:

fer_L3 = ["4530","4631","4632","4633","13530"]
fer_L4 = ["4540","4641","4642","4643","13540"]
fer_L5 = ["4550","4651","4652","4653","13550"]
fer = ["4530","4631","4632","4633","4540","4641","4642","4643","4550","4651","4642","4653","13530","13540","13550"]
linhas = ["L3","L4","L5"]
valvula_procurada = ""


#Configurações do Dashboard:

st.set_page_config(page_title = "Falhas em válvulas Amyris")
st.title("Falhas em válvulas - Amyris")

st.header("Falhas em válvulas")


uploaded_file = st.file_uploader("Upload do arquivo csv do SQL")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    df = pd.read_csv(uploaded_file)

    columns = ["Date","Active","SourceName","GroupPath"]
    df.columns = columns
    df['SourceName'] = df['SourceName'].str.split('@').str[0]
    df["SourceName"] = df["SourceName"].str.replace(r'\[.*?\]','')
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y %H:%M')

df_mes = df[["Date","SourceName"]]

aba1, aba2, aba3 = st.tabs(["Geral","Dashboard","Consultas"])

with aba1:

    coluna1,coluna2,coluna3 = st.columns(3)

    with coluna1:
        st.header("Linha #3")
        df_L3_fer = df_mes[df_mes["SourceName"].str.contains('|'.join(fer_L3), regex=True)]
        st.write(df_L3_fer.head())

    with coluna2:
        st.header("Linha #4")
        df_L4_fer = df_mes[df_mes["SourceName"].str.contains('|'.join(fer_L4), regex=True)]
        st.write(df_L4_fer.head())

    with coluna3:
        st.header("Linha #5")
        df_L5_fer = df_mes[df_mes["SourceName"].str.contains('|'.join(fer_L5), regex=True)]
        st.write(df_L5_fer.head())


with aba2:

    coluna1, coluna2 = st.columns(2)

    with coluna1:

        Total_flvlv_df = df_mes[df_mes["SourceName"].str.contains('|'.join(fer), regex=True)] #Falhas em válvulas totais
        Total_flvlv = Total_flvlv_df.shape[0]    
        Total_L3_fer = df_L3_fer.shape[0]
        Total_L4_fer = df_L4_fer.shape[0]
        Total_L5_fer = df_L5_fer.shape[0]

        data = {"Área":["Total","Linha 3","Linha 4", "Linha 5"],"Num_Falhas":[Total_flvlv,Total_L3_fer,Total_L4_fer,Total_L5_fer]}
        Num_Falhas_Lin = pd.DataFrame(data)
        cores = ["plum","purple","black","grey"]

        fig_falhavalv = px.bar(Num_Falhas_Lin, x="Área", y="Num_Falhas", color="Área", text="Num_Falhas", color_discrete_sequence=cores)
        fig_falhavalv.update_layout(title="Contagem falhas em válvulas", yaxis_title="# Falhas")

        st.header("Falhas em válvulas totais por linha")
        st.plotly_chart(fig_falhavalv)

        contagemL3 = df_L3_fer["SourceName"].value_counts()
        contagemL4 = df_L4_fer["SourceName"].value_counts()
        contagemL5 = df_L5_fer["SourceName"].value_counts()

        VlvsL3 = contagemL3.index
        FreqL3 = contagemL3.values
        VlvsL4 = contagemL4.index
        FreqL4 = contagemL4.values
        VlvsL5 = contagemL5.index
        FreqL5 = contagemL5.values



    with coluna2:

                
        num_valvs = st.number_input("Número de válvulas no gráfico", min_value=0, max_value=50, value=25, step=1)

        VlvsL3_subset = VlvsL3[:num_valvs]
        FreqL3_subset = FreqL3[:num_valvs]
        VlvsL4_subset = VlvsL4[:num_valvs]
        FreqL4_subset = FreqL4[:num_valvs]
        VlvsL5_subset = VlvsL5[:num_valvs]
        FreqL5_subset = FreqL5[:num_valvs]

        fig_paretto_L3f = px.bar(x=VlvsL3_subset, y=FreqL3_subset)
        fig_paretto_L3f.update_layout(title="Pareto de Falhas em válvulas - Linha #3", xaxis_title="Válvulas", yaxis_title="# Falhas")
        fig_paretto_L3f.update_traces(marker_color='purple')

        fig_paretto_L4f = px.bar(x=VlvsL4_subset, y=FreqL4_subset)
        fig_paretto_L4f.update_layout(title="Pareto de Falhas em válvulas - Linha #4", xaxis_title="Válvulas", yaxis_title="# Falhas")
        fig_paretto_L4f.update_traces(marker_color='black')

        fig_paretto_L5f = px.bar(x=VlvsL5_subset, y=FreqL5_subset)
        fig_paretto_L5f.update_layout(title="Pareto de Falhas em válvulas - Linha #5", xaxis_title="Válvulas", yaxis_title="# Falhas")
        fig_paretto_L5f.update_traces(marker_color='gray')

        st.plotly_chart(fig_paretto_L3f)
        st.plotly_chart(fig_paretto_L4f)
        st.plotly_chart(fig_paretto_L5f)

with aba3:

    linha_escolhida = st.selectbox("Linha de Fermentação", linhas)
    filtrar_valvula = st.checkbox("Filtrar por válvula", value = True)

    st.write(valvula_procurada)

    if linha_escolhida == "L3":
        
        df_exibido = df_L3_fer

    elif linha_escolhida == "L4":

        df_exibido = df_L4_fer

    else:

        df_exibido = df_L5_fer



    if filtrar_valvula:

        valvula_procurada = st.text_input("Válvula selecionada")


    if not filtrar_valvula:
        st.write(df_exibido)

    else:

        st.write(df_exibido.query("SourceName == @valvula_procurada"))
