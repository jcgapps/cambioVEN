import streamlit as st
from scraper import get_rates

st.set_page_config(page_title="Tasas BCV", page_icon="💱")

st.title("💱 Tasas de Cambio - BCV Venezuela")

rates = get_rates()

if rates:
    for divisa, valor in rates.items():
        st.metric(label=divisa, value=f"{valor} Bs")
else:
    st.error("No se pudieron obtener las tasas del BCV.")
