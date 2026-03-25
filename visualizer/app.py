import streamlit as st
import time
from src.data_loader import DataLoader

st.set_page_config(
    page_title="Method Name Miner",
    page_icon="📊",
    layout="wide"
)

loader = DataLoader()

st.title("📊 Ranking de Palabras en Métodos (Python & Java)")
st.markdown("Visualización en tiempo real de los datos extraídos desde GitHub.")

# Sidebar para configuración
st.sidebar.header("Configuración")
top_n = st.sidebar.slider("Top N palabras", min_value=5, max_value=50, value=15)
refresh_rate = st.sidebar.selectbox("Frecuencia de actualización (segundos)", [2, 5, 10, 30], index=0)

# Métricas principales
col1, col2 = st.columns(2)
unique_words, total_mentions = loader.get_stats()

with col1:
    st.metric("Palabras Únicas", unique_words)
with col2:
    st.metric("Total de Apariciones", total_mentions)

# Gráfico y Tabla
df = loader.get_top_words(limit=top_n)

if not df.empty:
    st.subheader(f"Top {top_n} Palabras más utilizadas")
    st.bar_chart(df.set_index('word'))
    
    st.subheader("Desglose de datos")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Esperando datos del Miner... Asegúrate de que el contenedor 'miner' esté corriendo y tenga conexión a GitHub.")

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()