import streamlit as st

st.title("🎈 Analiador de CNPJ MEI")

pip install streamlit requests beautifulsoup4

import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Analisador de CNPJ MEI")

cnpj = st.text_input("Digite o CNPJ (apenas números):")

if st.button("Analisar"):
    if not cnpj or len(cnpj) != 14:
        st.error("CNPJ inválido.")
    else:
        resultado = {}

        # 1. Consulta Optante
        url_optante = f"https://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=21"
        opt_response = requests.post(url_optante, data={"cnpj": cnpj})
        if "Não optante" in opt_response.text:
            resultado["Status MEI"] = "Desenquadrado do MEI"
        elif "Optante" in opt_response.text:
            resultado["Status MEI"] = "Optante pelo MEI"
        else:
            resultado["Status MEI"] = "Não foi possível determinar"

        # 2. DASN
        dasn_url = "https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/dasnsimei.app/Identificacao"
        dasn_res = requests.post(dasn_url, data={"cnpj": cnpj})
        if "Declarada" in dasn_res.text:
            resultado["Declaração Anual"] = "Entregue"
        elif "não entregue" in dasn_res.text.lower():
            resultado["Declaração Anual"] = "Não entregue"
        else:
            resultado["Declaração Anual"] = "Não foi possível verificar"

        # 3. PGMEI - Débito/Dívida Ativa
        pgmei_url = "https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao"
        pgmei_res = requests.post(pgmei_url, data={"cnpj": cnpj})
        if "Dívida Ativa" in pgmei_res.text or "Regularize" in pgmei_res.text:
            resultado["Dívida Ativa"] = "Sim, há inscrição"
        elif "não possui débitos" in pgmei_res.text.lower():
            resultado["Dívida Ativa"] = "Não possui"
        else:
            resultado["Dívida Ativa"] = "Não foi possível verificar"

        # Resultado final
        st.subheader("Resultado da Análise:")
        for chave, valor in resultado.items():
            st.write(f"**{chave}**: {valor}")
