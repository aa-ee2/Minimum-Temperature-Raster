
import streamlit as st
import pandas as pd
from pathlib import Path
import io

st.set_page_config(page_title="Tmin · Propuestas y Focalización", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
DATA = ROOT / "data"

@st.cache_data
def load_csv(path: Path):
    return pd.read_csv(path) if path.exists() else None

propuestas = load_csv(OUT / "policy_proposals.csv")
targets_andes = load_csv(OUT / "targets_andes.csv")
targets_amaz = load_csv(OUT / "targets_amazonia.csv")
costos_totales = load_csv(OUT / "costos_totales.csv")
costos_por_distrito = load_csv(OUT / "costos_por_distrito.csv")

st.title("Propuestas frente a heladas (Andes) y friajes (Amazonía)")
st.caption("Distritos objetivo: Tmin ≤ p10 (según tus estadísticas zonales).")

if propuestas is None:
    st.error("Falta outputs/policy_proposals.csv. Genera este archivo desde tu notebook.")
    st.stop()

colf1, colf2, colf3 = st.columns([1,1,2])
with colf1:
    region = st.selectbox("Filtrar por región", ["Todas","Andes altos","Amazonía"])
with colf2:
    buscar = st.text_input("Buscar en targets (departamento/distrito)", "").strip()

df_view = propuestas.copy()
if region != "Todas":
    df_view = df_view[df_view["Región"] == region]
if buscar:
    df_view = df_view[df_view["Target (distritos ≤ p10)"].fillna("").str.lower().str.contains(buscar.lower())]

st.subheader("Propuestas")
st.dataframe(df_view, use_container_width=True)

buf = io.BytesIO()
df_view.to_csv(buf, index=False, encoding="utf-8-sig")
st.download_button("⬇️ Descargar propuestas (CSV)", buf.getvalue(), file_name="propuestas_filtradas.csv", mime="text/csv")

st.divider()
st.subheader("Distritos objetivo (≤ p10)")
tabs = st.tabs(["Andes altos", "Amazonía"])

with tabs[0]:
    if targets_andes is None:
        st.info("Falta outputs/targets_andes.csv")
    else:
        cols = [c for c in ["DEPARTAMEN","DEPARTAMENTO","PROVINCIA","DISTRITO","TMIN_MEAN"] if c in targets_andes.columns]
        ta = targets_andes[cols].copy()
        st.dataframe(ta, use_container_width=True, height=350)
        bio = io.BytesIO(); ta.to_csv(bio, index=False, encoding="utf-8-sig")
        st.download_button("⬇️ Descargar targets Andes (CSV)", bio.getvalue(), file_name="targets_andes.csv", mime="text/csv")

with tabs[1]:
    if targets_amaz is None:
        st.info("Falta outputs/targets_amazonia.csv")
    else:
        cols = [c for c in ["DEPARTAMEN","DEPARTAMENTO","PROVINCIA","DISTRITO","TMIN_MEAN"] if c in targets_amaz.columns]
        tm = targets_amaz[cols].copy()
        st.dataframe(tm, use_container_width=True, height=350)
        bio2 = io.BytesIO(); tm.to_csv(bio2, index=False, encoding="utf-8-sig")
        st.download_button("⬇️ Descargar targets Amazonía (CSV)", bio2.getvalue(), file_name="targets_amazonia.csv", mime="text/csv")

st.divider()
st.subheader("Costos estimados")

if costos_totales is not None and "Soles" in costos_totales.columns:
    st.write("**Totales por propuesta**")
    st.dataframe(costos_totales, use_container_width=True)
    try:
        import altair as alt
        c = alt.Chart(costos_totales.reset_index(names="Propuesta")).mark_bar().encode(
            x="Propuesta:N", y="Soles:Q", tooltip=["Propuesta","Soles"]
        ).properties(height=300)
        st.altair_chart(c, use_container_width=True)
    except Exception as e:
        st.info(f"Altair no disponible para gráfico: {e}")
else:
    st.info("Genera outputs/costos_totales.csv para ver totales y gráfico.")

if costos_por_distrito is not None:
    st.write("**Detalle por distrito:**")
    st.dataframe(costos_por_distrito, use_container_width=True, height=300)
    bio3 = io.BytesIO(); costos_por_distrito.to_csv(bio3, index=False, encoding="utf-8-sig")
    st.download_button("⬇️ Descargar costos por distrito (CSV)", bio3.getvalue(), file_name="costos_por_distrito.csv", mime="text/csv")

st.caption("Nota: Documenta si usaste p10 global o por grupo (Andes/Amazonía) en el README.")

#ho