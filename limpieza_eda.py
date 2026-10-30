"""Limpieza y análisis exploratorio del dataset Online Retail.
Coloca data.csv junto a este script y ejecuta: python limpieza_eda.py
El archivo original no se modifica. Los resultados se guardan en ./salida/.
"""
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data.csv"
OUTPUT_DIR = BASE_DIR / "salida"
ENCODING = "ISO-8859-1"


def get_mode(series: pd.Series):
    modes = series.dropna().mode()
    return modes.iloc[0] if not modes.empty else np.nan


def descriptive_statistics(frame: pd.DataFrame, label: str) -> list[dict]:
    rows = []
    for column in ["Quantity", "UnitPrice", "TotalPrice"]:
        values = pd.to_numeric(frame[column], errors="coerce").dropna()
        rows.append({
            "Conjunto": label,
            "Variable": column,
            "N": int(values.count()),
            "Media": values.mean(),
            "Mediana": values.median(),
            "Moda": get_mode(values),
            "Desviacion_estandar_muestral": values.std(ddof=1),
            "Minimo": values.min(),
            "Maximo": values.max(),
        })
    return rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "No encontré data.csv. Colócalo junto a limpieza_eda.py y vuelve a ejecutar."
        )

    original = pd.read_csv(
        INPUT_FILE,
        encoding=ENCODING,
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "Description": "string",
            "Country": "string",
        },
    )
    expected = {
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    }
    missing = expected.difference(original.columns)
    if missing:
        raise ValueError(f"Faltan columnas esperadas en data.csv: {sorted(missing)}")

    total_original = len(original)
    original_columns = len(original.columns)
    exact_duplicates = int(original.duplicated().sum())
    invalid_dates = int(pd.to_datetime(original["InvoiceDate"], errors="coerce").isna().sum())
    blank_descriptions = int(
        original["Description"].isna().sum()
        + original["Description"].astype("string").str.strip().eq("").fillna(False).sum()
    )
    missing_customers = int(original["CustomerID"].isna().sum())
    negative_quantities = int((pd.to_numeric(original["Quantity"], errors="coerce") < 0).sum())
    nonpositive_prices = int((pd.to_numeric(original["UnitPrice"], errors="coerce") <= 0).sum())
    cancellation_rows = int(
        original["InvoiceNo"].astype("string").str.upper().str.startswith("C", na=False).sum()
    )

    clean = original.copy()
    for column in ["InvoiceNo", "StockCode", "Description", "Country"]:
        clean[column] = clean[column].astype("string").str.strip()
    clean["Description"] = clean["Description"].replace("", pd.NA)
    clean["InvoiceDate"] = pd.to_datetime(clean["InvoiceDate"], errors="coerce")
    clean["Quantity"] = pd.to_numeric(clean["Quantity"], errors="coerce")
    clean["UnitPrice"] = pd.to_numeric(clean["UnitPrice"], errors="coerce")
    clean["CustomerID"] = pd.to_numeric(clean["CustomerID"], errors="coerce").astype("Int64")

    # Se eliminan duplicados exactos; cancelaciones y devoluciones se conservan.
    clean = clean.drop_duplicates().copy()
    clean["TotalPrice"] = clean["Quantity"] * clean["UnitPrice"]

    is_cancellation = clean["InvoiceNo"].str.upper().str.startswith("C", na=False)
    clean["TipoOperacion"] = np.select(
        [
            is_cancellation,
            clean["Quantity"] < 0,
            clean["UnitPrice"] <= 0,
            clean["Description"].isna(),
            clean["InvoiceDate"].isna(),
        ],
        [
            "Cancelación (factura C)",
            "Cantidad negativa / devolución",
            "Precio no positivo",
            "Descripción faltante",
            "Fecha inválida",
        ],
        default="Venta candidata",
    )

    valid_sales = (
        ~is_cancellation
        & clean["Quantity"].gt(0)
        & clean["UnitPrice"].gt(0)
        & clean["Description"].notna()
        & clean["InvoiceDate"].notna()
    )
    sales = clean.loc[valid_sales].copy()

    clean["InvoiceDate"] = clean["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")
    sales["InvoiceDate"] = sales["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")
    clean.to_csv(OUTPUT_DIR / "data_limpio.csv", index=False, encoding="utf-8-sig")
    sales.to_csv(OUTPUT_DIR / "data_ventas.csv", index=False, encoding="utf-8-sig")

    quality_metrics = [
        ("Registros originales", total_original, "Filas leídas desde data.csv"),
        ("Columnas originales", original_columns, "Variables del archivo fuente"),
        ("Duplicados exactos detectados", exact_duplicates, "Se elimina una copia de cada fila duplicada exacta"),
        ("Registros tras eliminar duplicados", len(clean), "Se conservan devoluciones y cancelaciones"),
        ("Descripciones vacías en el original", blank_descriptions, "No se inventan nombres de productos"),
        ("CustomerID faltante en el original", missing_customers, "Se conserva como cliente no identificado"),
        ("Cantidad negativa en el original", negative_quantities, "Se conserva para documentar devoluciones/ajustes"),
        ("UnitPrice no positivo en el original", nonpositive_prices, "Se excluye del dataset de ventas válidas"),
        ("Facturas con prefijo C en el original", cancellation_rows, "Se excluyen del dataset de ventas válidas"),
        ("Fechas no interpretables en el original", invalid_dates, "Se excluyen del dataset de ventas válidas"),
        ("Filas del dataset para ventas", len(sales), "Cantidad y precio positivos, descripción y fecha válidas; no cancelación"),
        ("Facturas distintas en ventas", int(sales["InvoiceNo"].nunique()), "Una factura puede ocupar varias filas por producto"),
        ("Productos distintos en ventas", int(sales["StockCode"].nunique()), "Conteo distinto de StockCode"),
        ("Clientes identificados en ventas", int(sales["CustomerID"].nunique()), "No incluye identificadores faltantes"),
        ("Países distintos en ventas", int(sales["Country"].nunique()), "Conteo distinto de Country"),
        ("Ingresos de las ventas válidas", round(float(sales["TotalPrice"].sum()), 2), "Suma de Quantity × UnitPrice en data_ventas.csv"),
        ("Unidades de ventas válidas", int(sales["Quantity"].sum()), "Suma de Quantity en data_ventas.csv"),
    ]
    pd.DataFrame(
        quality_metrics, columns=["Indicador", "Valor", "Interpretación"]
    ).to_csv(OUTPUT_DIR / "reporte_calidad.csv", index=False, encoding="utf-8-sig")

    source_stats = original.copy()
    source_stats["TotalPrice"] = (
        pd.to_numeric(source_stats["Quantity"], errors="coerce")
        * pd.to_numeric(source_stats["UnitPrice"], errors="coerce")
    )
    stats = descriptive_statistics(
        source_stats, "Original (incluye duplicados, cancelaciones y devoluciones)"
    )
    stats += descriptive_statistics(sales, "Ventas válidas (tras limpieza)")
    pd.DataFrame(stats).to_csv(
        OUTPUT_DIR / "estadisticas_descriptivas.csv", index=False, encoding="utf-8-sig"
    )

    monthly = sales.copy()
    monthly["InvoiceDate"] = pd.to_datetime(monthly["InvoiceDate"])
    monthly["Mes"] = monthly["InvoiceDate"].dt.to_period("M").astype(str)
    monthly_summary = monthly.groupby("Mes", as_index=False).agg(
        Ingresos=("TotalPrice", "sum"),
        Unidades=("Quantity", "sum"),
        Lineas_de_venta=("InvoiceNo", "size"),
        Facturas_distintas=("InvoiceNo", "nunique"),
    )
    monthly_summary.to_csv(
        OUTPUT_DIR / "resumen_mensual.csv", index=False, encoding="utf-8-sig"
    )

    product_summary = sales.groupby("Description", as_index=False).agg(
        Unidades_vendidas=("Quantity", "sum"),
        Ingresos=("TotalPrice", "sum"),
        Facturas_distintas=("InvoiceNo", "nunique"),
    ).sort_values("Ingresos", ascending=False)
    product_summary.to_csv(
        OUTPUT_DIR / "productos_resumen.csv", index=False, encoding="utf-8-sig"
    )

    country_summary = sales.groupby("Country", as_index=False).agg(
        Ingresos=("TotalPrice", "sum"),
        Unidades=("Quantity", "sum"),
        Facturas_distintas=("InvoiceNo", "nunique"),
    ).sort_values("Ingresos", ascending=False)
    country_summary.to_csv(
        OUTPUT_DIR / "paises_resumen.csv", index=False, encoding="utf-8-sig"
    )

    print("Proceso terminado correctamente.")
    print(f"Registros originales: {total_original:,}")
    print(f"Duplicados exactos eliminados: {exact_duplicates:,}")
    print(f"Registros tras limpieza general: {len(clean):,}")
    print(f"Registros de ventas válidas: {len(sales):,}")
    print(f"Facturas distintas: {sales['InvoiceNo'].nunique():,}")
    print(f"Ingresos de ventas válidas: £{sales['TotalPrice'].sum():,.2f}")
    print(f"Archivos generados en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
