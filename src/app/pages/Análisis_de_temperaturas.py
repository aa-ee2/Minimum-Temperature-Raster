import streamlit as st
import pandas as pd
from pathlib import Path
import io

# Set page configuration (title and layout)
st.set_page_config(
    page_title="Análisis de Temperaturas",
    page_icon="🌡️",
    layout="wide"
)

# Define paths
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"
DATA = ROOT.parent / "data"

# Page title
st.title("🌡️ Análisis de Temperaturas Mínimas")
st.caption("Visualización de mapas y estadísticas zonales de Tmin.")

# File paths
choropleth_path = OUT / "choropleth_distritos.png"
hist_path = OUT / "hist_temperatura_minima.png"
zonal_path = DATA / "zonal_tmin_bandas.csv"

# Show images
if choropleth_path.exists():
    st.image(str(choropleth_path), width=700)
else:
    st.warning(f"No se encontró el archivo: {choropleth_path.name}")

if hist_path.exists():
    st.image(str(hist_path), width=700)
else:
    st.warning(f"No se encontró el archivo: {hist_path.name}")

# Load and show CSV
if zonal_path.exists():
    df = pd.read_csv(zonal_path)
    st.subheader("📋 Estadísticas Zonales de Temperatura Mínima")
    st.dataframe(df, use_container_width=True)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    st.download_button(
        label="⬇️ Descargar estadísticas zonales (CSV)",
        data=buffer.getvalue(),
        file_name="zonal_tmin_bandas.csv",
        mime="text/csv"
        )
else:
    st.warning("No se encontró el archivo: zonal_tmin_bandas.csv")