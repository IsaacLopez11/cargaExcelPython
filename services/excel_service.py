import pandas as pd
from datetime import datetime


def calcular(df):
    """
    🔥 ESPACIO CLARO PARA CÁLCULOS FUTUROS
    """

    resultados = {}

    if df.empty:
        resultados["error"] = "El archivo está vacío."
        return resultados

    # ==========================
    # 🧹 NORMALIZAR COLUMNAS
    # ==========================

    df.columns = df.columns.str.strip().str.lower()

    columnas_necesarias = ["sueldo", "fechanac", "nombre"]

    for col in columnas_necesarias:
        if col not in df.columns:
            resultados["error"] = f"Falta la columna obligatoria: {col}"
            return resultados

    # ==========================
    # 🔄 CONVERSIÓN DE TIPOS
    # ==========================

    df["sueldo"] = pd.to_numeric(df["sueldo"], errors="coerce")
    df["fechanac"] = pd.to_datetime(df["fechanac"], errors="coerce")

    # Eliminar filas inválidas
    df = df.dropna(subset=["sueldo", "fechanac"])

    if df.empty:
        resultados["error"] = "No hay datos válidos para calcular."
        return resultados

    # ==========================
    # 📊 CÁLCULOS ACTUALES
    # ==========================

    # 💰 Sueldo más alto
    resultados["sueldo_max"] = float(df["sueldo"].max())

    # 👶 Persona más joven
    persona_joven = df.loc[df["fechanac"].idxmax()]
    resultados["persona_mas_joven"] = persona_joven["nombre"]

    # 📈 Edad promedio
    hoy = datetime.today()
    edades = (hoy - df["fechanac"]).dt.days / 365
    resultados["edad_promedio"] = round(edades.mean(), 1)

    # ==========================
    # 🔮 ESPACIO FUTURO
    # ==========================

    # resultados["sueldo_promedio"] = float(df["sueldo"].mean())
    # resultados["total_personas"] = len(df)
    # resultados["ciudad_mas_frecuente"] = df["ciudadres"].mode()[0]

    return resultados