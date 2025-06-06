import streamlit as st

import pandas as pd

import altair as alt

#Nome do site
st.set_page_config(page_title="O Último Habitat")

#Biomas
@st.cache_data
def carregar_dados_biomas():
    tabela_biomas = pd.read_csv("Ranking_de_Biomas.csv")
    return tabela_biomas

#Estados
@st.cache_data
def carregar_dados_estados():
    tabela_estados = pd.read_csv("Ranking_de_Estados.csv")
    return tabela_estados

#Evolução mensal
@st.cache_data
def carregar_dados_mensal():
    tabela_mensal = pd.read_csv("Evolução_mensal_da_área_de_desmatamento.csv")
    return tabela_mensal

#Total de Alertas
@st.cache_data
def carregar_dados_alertas():
    tabela_alertas = pd.read_csv("Evolução_do_total_de_alertas.csv")
    return tabela_alertas

#Caça Ilegal no brasil
@st.cache_data
def carregar_dados_caça():
    tabela_caça = pd.read_csv("dados_caça_brasil.csv")
    return tabela_caça


with st.container():
    st.title("O Impacto do Ser Humano na Vida Animal")
    st.markdown("## Dashboard Interativo")

    st.markdown("""
    Este projeto tem como objetivo **explorar visualmente os principais fatores que ameaçam a fauna brasileira**. 
    Por meio deste dashboard interativo, você poderá navegar por dados reais e atualizados sobre:
    
    - 🌳 Desmatamento nos biomas brasileiros  
    - 🐾 Caça e tráfico ilegal de animais  
    - 🛢️ Vazamentos causados por embarcações

    Ao selecionar um dos temas no menu lateral, você terá acesso a gráficos e análises que mostram como essas ações humanas estão alterando o equilíbrio ecológico.

    **Explore, analise e reflita:** A destruição é silenciosa, mas suas consequências gritam por gerações.
    """)


#--------------Desmatamento---------------

if "mostrar_dashboard" not in st.session_state:
    st.session_state.mostrar_dashboard = False

# Botão para exibir o dashboard
if st.sidebar.button("DESMATAMENTO"):
    st.session_state.mostrar_dashboard = not st.session_state.mostrar_dashboard

if st.session_state.mostrar_dashboard:

    #Inicio da pagina
    with st.container():
        st.write("Informações importantes")
        st.write("Desmatamento no Brasil [Clique aqui](https://plataforma.alerta.mapbiomas.org/mapa)")


    #Total de Alertas
    with st.container():
        st.write("---")

        st.title("Total de Alertas por Ano")

        dados_alertas = carregar_dados_alertas()

        sel_alertas = ["Todos os Anos"] + list(dados_alertas["Ano"].unique())

        alerta_area = st.selectbox("Selecione o Ano", sel_alertas)

        if alerta_area == "Todos os Anos":
            dados_alertas = dados_alertas

    
        else:
            dados_alertas = dados_alertas[dados_alertas["Ano"] == alerta_area]

    
        st.bar_chart(dados_alertas.set_index("Ano")["Alertas"])
        

    #Biomas 
    with st.container():
        st.write("---")

        st.title("O impacto nos biomas")


        dados_bio = carregar_dados_biomas()
        sel_bio = ["Todos os Biomas"] + list(dados_bio["Bioma"].unique())

        bio_area = st.selectbox("Selecione o Bioma", sel_bio)

        if bio_area == "Todos os Biomas":
            dados_bio = dados_bio

        else:
         dados_bio = dados_bio[dados_bio["Bioma"] == bio_area]    
    

        st.bar_chart(dados_bio.set_index("Bioma")["Área Total"])


    #Estados
    with st.container():
        st.write("---")


        st.title("Ranking de Desmantamento por Estados")

        dados_est = carregar_dados_estados()
        sel_est = ["Todos os Estados"] + list(dados_est["Estado"].unique())

        est_area = st.selectbox("Selecione o Estado", sel_est)

        if est_area == "Todos os Estados":
            dados_est = dados_est

        else:
         dados_est = dados_est[dados_est["Estado"] == est_area]

        st.bar_chart(dados_est.set_index("Estado")["Área Total"])


    #Evolução mensal 
    with st.container():
        st.write("---")
        st.title("Evolução Mensal da Área de Desmatamento")

        dados_mensal = carregar_dados_mensal()
        dados_mensal["Ano"] = dados_mensal["Ano"].astype(str)

        anos = list(dados_mensal["Ano"].unique())
        meses = list(dados_mensal.columns[2:]) 

        col1, col2 = st.columns(2)
        anos_selecionados = col1.multiselect("Selecione os Anos", anos, default=anos)
        meses_selecionados = col2.multiselect("Selecione os Meses", meses, default=meses)

        dados_filtrados = dados_mensal[dados_mensal["Ano"].isin(anos_selecionados)]

        if meses_selecionados:
    
            dados_long = pd.melt(
            dados_filtrados,
            id_vars=["Ano"],
            value_vars=meses_selecionados,
            var_name="Mês",
            value_name="Área de Desmatamento"
            )

            chart = alt.Chart(dados_long).mark_line(point=True).encode(
            x=alt.X("Mês", sort=meses), 
            y="Área de Desmatamento",
            color="Ano",
            tooltip=["Ano", "Mês", "Área de Desmatamento"]
            ).properties(
            width=800,
            height=400,
            title="Comparativo Interativo da Área de Desmatamento"
            ).interactive()

            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Selecione pelo menos um mês para visualizar o gráfico.")


 #---------------Caça_Ilegal------------   

if "mostrar_dashboard_caça" not in st.session_state:
    st.session_state.mostrar_dashboard_caça = False

# Botão para exibir o dashboard
if st.sidebar.button("CAÇA ILEGAL"):
    st.session_state.mostrar_dashboard_caça = not st.session_state.mostrar_dashboard_caça

if st.session_state.mostrar_dashboard_caça:

    #Inicio da pagina
    with st.container():
        st.write("Informações importantes")
        st.write("Caça Ilegal No Brasil [Clique aqui](https://conbio.onlinelibrary.wiley.com/doi/10.1111/cobi.14334)")


    #Caça Ilegal no Brasil
    with st.container():
        st.write("------")
        st.title("Caça Ilegal No Brasil")

        dados_caça = carregar_dados_caça()

        # Filtros
        with st.sidebar:
            st.subheader("Filtros - Caça")
            grupos = st.multiselect("Grupo Taxonômico", dados_caça["Grupo Taxonômico"].unique(), default=dados_caça["Grupo Taxonômico"].unique())
            

        dados_filtrados = dados_caça[
            (dados_caça["Grupo Taxonômico"].isin(grupos)) 
        ]

        # Gráfico 1 - Espécies mais caçadas
        st.subheader("Espécies Mais Caçadas")
        top_caça = dados_filtrados.sort_values("Indivíduos Caçados", ascending=False).head(10)
        st.bar_chart(top_caça.set_index("Espécie")["Indivíduos Caçados"])

        # Gráfico 2 - Barras empilhadas por grupo e região
        st.subheader("Total de Indivíduos Caçados por Grupo e Região")
        agrupado = dados_filtrados.groupby(["Grupo Taxonômico", "Região de Ocorrência"])["Indivíduos Caçados"].sum().reset_index()

        chart = alt.Chart(agrupado).mark_bar().encode(
            x=alt.X("Região de Ocorrência:N", title="Região"),
            y=alt.Y("Indivíduos Caçados:Q"),
            color="Grupo Taxonômico:N",
            tooltip=["Grupo Taxonômico", "Região de Ocorrência", "Indivíduos Caçados"]
        ).properties(width=800, height=400)

        st.altair_chart(chart, use_container_width=True)

        # Gráfico 3 - Categorias de ameaça
        st.subheader("Distribuição por Categoria de Ameaça")
        categoria_df = dados_filtrados["Categoria de Ameaça"].value_counts().reset_index()
        categoria_df.columns = ["Categoria de Ameaça", "Total"]

        donut = alt.Chart(categoria_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("Total:Q"),
            color=alt.Color("Categoria de Ameaça:N"),
            tooltip=["Categoria de Ameaça", "Total"]
        ).properties(width=500, height=400)

        st.altair_chart(donut, use_container_width=True)

        # Tabela final
        st.write("Dados filtrados:")
        st.dataframe(dados_filtrados)



# ----------Poluição por Embarcações----------


@st.cache_data
def carregar_poluicao_embarcacoes():
    df = pd.read_csv("Relatório de poluição causada por Embarcações e Plataformas.xlsx - 1DN.csv")
    df.columns = [col.strip().replace("\n", " ").replace("  ", " ") for col in df.columns]
    df["Data do Incidente"] = pd.to_datetime(df["DATA DO INCIDENTE"], errors='coerce', dayfirst=True)
    df["Volume Derramado (litros)"] = (
        df["VOLUME DERRAMADO (em litros)"]
        .astype(str)
        .str.replace(",", ".")
        .str.extract(r'([\d.]+)')
        .astype(float)
    )
    return df

if "mostrar_dashboard_embarcacoes" not in st.session_state:
    st.session_state.mostrar_dashboard_embarcacoes = False

if st.sidebar.button("POLUIÇÃO POR EMBARCAÇÕES"):
    st.session_state.mostrar_dashboard_embarcacoes = not st.session_state.mostrar_dashboard_embarcacoes

if st.session_state.mostrar_dashboard_embarcacoes:
    st.title("Poluição Marinha Causada por Embarcações e Plataformas")
    dados_embarcacoes = carregar_poluicao_embarcacoes()


    #Inicio da pagina
    with st.container():
        st.write("Informações importantes")
        st.write("Poluição Marinha [Clique aqui](https://news.fiquemsabendo.com.br/p/poluicao-marinha-dados-de-embarcacoes?utm_source=chatgpt.com)")



    # Gráfico de barras: volume por tipo de óleo
    st.subheader("Volume Total Derramado por Tipo de Óleo")
    volume_por_tipo = dados_embarcacoes.groupby("TIPO DE ÓLEO MÃE")["Volume Derramado (litros)"].sum().reset_index()
    chart_oleo = alt.Chart(volume_por_tipo).mark_bar().encode(
        x=alt.X("Volume Derramado (litros):Q"),
        y=alt.Y("TIPO DE ÓLEO MÃE:N", sort='-x'),
        tooltip=["TIPO DE ÓLEO MÃE", "Volume Derramado (litros)"]
    ).properties(width=700, height=400)
    st.altair_chart(chart_oleo, use_container_width=True)

    # Linha do tempo de incidentes
    st.subheader("Incidentes ao Longo do Tempo")
    incidentes_por_mes = dados_embarcacoes.dropna(subset=["Data do Incidente"]).copy()
    incidentes_por_mes["Ano-Mês"] = incidentes_por_mes["Data do Incidente"].dt.to_period("M").astype(str)
    evolucao = incidentes_por_mes.groupby("Ano-Mês").size().reset_index(name="Incidentes")

    chart_tempo = alt.Chart(evolucao).mark_line(point=True).encode(
        x="Ano-Mês",
        y="Incidentes",
        tooltip=["Ano-Mês", "Incidentes"]
    ).properties(width=700, height=350)
    st.altair_chart(chart_tempo, use_container_width=True)

    # Tabela de dados
    st.subheader("Tabela de Ocorrências")
    colunas_visiveis = [
        "DATA DO INCIDENTE", "LOCALIZAÇÃO", "EMBARCAÇÃO", "TIPO DE ÓLEO MÃE",
        "Volume Derramado (litros)", "INFRATOR", "NÍVEL DE IMPACTO AMBIENTAL", 
        "Valor da Multa (1º instância)", "Andamento do processo no SISAUTO"
    ]
    st.dataframe(dados_embarcacoes[colunas_visiveis])
