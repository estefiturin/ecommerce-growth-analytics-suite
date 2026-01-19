import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

# 1. Configuración de la Página
st.set_page_config(page_title="Dashboard Retail Analytics", page_icon="🛒", layout="wide")

# 2. Función de Carga de Datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/datos_limpios.csv")
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

# Título Principal
st.title("📊 Tablero de Control: E-Commerce Intelligence")
st.markdown("---")

# --- CREACIÓN DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📊 Visión General", "🧠 Relación de Productos (Bayes)", "🧪 Laboratorio de Pruebas"])

# ==============================================================================
# TAB 1: VISIÓN GENERAL (Lo que ya tenías)
# ==============================================================================
with tab1:
    st.header("Panorama del Negocio")
    
    # Filtros solo para esta pestaña
    paises = st.multiselect("Filtrar por País:", options=df['Country'].unique(), default=df['Country'].unique())
    df_selection = df.query("Country == @paises")

    # KPIs
    total_ventas = df_selection['Total_Venta'].sum()
    promedio_ticket = df_selection.groupby('Invoice')['Total_Venta'].sum().mean()
    
    col_kpi1, col_kpi2 = st.columns(2)
    col_kpi1.metric("Ventas Totales", f"${total_ventas:,.2f}")
    col_kpi2.metric("Ticket Promedio", f"${promedio_ticket:,.2f}")
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        ventas_por_fecha = df_selection.set_index('InvoiceDate').resample('M')['Total_Venta'].sum().reset_index()
        fig_time = px.line(ventas_por_fecha, x='InvoiceDate', y='Total_Venta', title="Tendencia Mensual")
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        top_products = df_selection.groupby('Description')['Total_Venta'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_prod = px.bar(top_products, x='Total_Venta', y='Description', orientation='h', title="Top 10 Productos")
        fig_prod.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_prod, use_container_width=True)

# ==============================================================================
# TAB 2: INTELIGENCIA DE PRODUCTOS (Bayes & Lift)
# ==============================================================================
with tab2:
    st.header("Análisis de Asociación (Cross-Selling)")
    st.markdown("Descubre qué productos impulsan la venta de otros (Probabilidad Condicional).")

    # Interfaz para que el usuario elija productos (Simplificada para el demo)
    # Nota: Calcular todas las combinaciones en vivo es lento, así que usaremos el ejemplo que descubrimos
    
    st.info("💡 Insight Descubierto: Analizando el 'REGENCY CAKESTAND 3 TIER'")
    
    producto_A = 'REGENCY CAKESTAND 3 TIER'
    producto_B = 'WHITE HANGING HEART T-LIGHT HOLDER'
    
    # Cálculos en vivo (Lógica traída de tu notebook)
    facturas_con_A = set(df[df['Description'] == producto_A]['Invoice'])
    facturas_con_B = set(df[df['Description'] == producto_B]['Invoice'])
    facturas_con_ambos = facturas_con_A & facturas_con_B
    
    n_A = len(facturas_con_A)
    n_ambos = len(facturas_con_ambos)
    prob_B_dado_A = (n_ambos / n_A) * 100
    
    # Probabilidad Base
    total_facturas = df['Invoice'].nunique()
    prob_base_B = (len(facturas_con_B) / total_facturas) * 100
    
    # Lift
    lift = prob_B_dado_A / prob_base_B
    
    # Visualización de Métricas
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("Probabilidad Base (Solo Portavelas)", f"{prob_base_B:.2f}%")
    col_b2.metric("Probabilidad Condicional (Si compró Soporte)", f"{prob_B_dado_A:.2f}%")
    col_b3.metric("LIFT (Atracción)", f"{lift:.2f}x", delta="Positivo" if lift > 1 else "Negativo")
    
    if lift > 1:
        st.success(f"✅ **Recomendación:** Existe una atracción de {lift:.2f}x. ¡Crear un bundle con estos dos productos aumentará las ventas!")

# ==============================================================================
# TAB 3: LABORATORIO DE PRUEBAS (Estadística Avanzada)
# ==============================================================================
with tab3:
    st.header("Laboratorio de Experimentación")
    
    # SECCIÓN A: Prueba de Hipótesis (T-Test) Comparación de Países
    st.subheader("1. Comparación de Mercados (Prueba T)")
    st.markdown("¿Gasta más un país que otro por ticket promedio?")
    
    col_t1, col_t2 = st.columns(2)
    pais_1 = col_t1.selectbox("País A", df['Country'].unique(), index=0) # UK
    pais_2 = col_t2.selectbox("País B", df['Country'].unique(), index=1) # France
    
    if st.button("Ejecutar Prueba T"):
        data_p1 = df[df['Country'] == pais_1].groupby('Invoice')['Total_Venta'].sum()
        data_p2 = df[df['Country'] == pais_2].groupby('Invoice')['Total_Venta'].sum()
        
        t_stat, p_val = stats.ttest_ind(data_p1, data_p2, equal_var=False)
        
        st.write(f"**Media {pais_1}:** ${data_p1.mean():.2f}")
        st.write(f"**Media {pais_2}:** ${data_p2.mean():.2f}")
        st.metric("P-Value", f"{p_val:.4f}")
        
        if p_val < 0.05:
            st.success("¡Diferencia Significativa! Los promedios son estadísticamente diferentes.")
        else:
            st.warning("No hay evidencia suficiente para decir que son diferentes (Podría ser casualidad).")

    st.markdown("---")
    
    # SECCIÓN B: Simulador A/B Testing
    st.subheader("2. Simulador de Campañas (A/B Testing)")
    st.markdown("Simula el lanzamiento de un cupón y verifica si el aumento de conversión es real.")
    
    col_sim1, col_sim2 = st.columns(2)
    tasa_base = col_sim1.slider("Tasa de Conversión Base (%)", 5, 50, 15) / 100
    efecto_real = col_sim2.slider("Efecto Real del Cupón (+%)", 0, 10, 2) / 100
    
    if st.button("Simular Experimento A/B"):
        # Simulación en vivo
        n_muestras = 5000
        # Grupo A (Control)
        conversiones_A = np.random.binomial(n_muestras, tasa_base)
        # Grupo B (Tratamiento)
        conversiones_B = np.random.binomial(n_muestras, tasa_base + efecto_real)
        
        # Z-Test
        stat, pval_z = proportions_ztest([conversiones_B, conversiones_A], [n_muestras, n_muestras])
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Tasa Grupo A", f"{(conversiones_A/n_muestras)*100:.2f}%")
        col_res2.metric("Tasa Grupo B", f"{(conversiones_B/n_muestras)*100:.2f}%")
        
        st.write(f"**P-Value del Z-Test:** {pval_z:.4f}")
        if pval_z < 0.05:
            st.success(f"✅ Éxito: Detectamos la mejora del {efecto_real*100}% con significancia estadística.")
        else:
            st.error("❌ No concluyente: Aunque hubo mejora, el test estadístico no pudo confirmarla (necesitamos más muestra o el efecto es muy pequeño).")