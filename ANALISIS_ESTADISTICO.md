# Análisis estadístico y calidad de datos

**Proyecto:** E-Commerce Analytics  
**Dataset:** Online Retail  
**Archivo fuente:** `data.csv`  
**Tamaño del archivo analizado:** 541,909 registros y 8 columnas.

## 1. Calidad del conjunto de datos

| Indicador | Resultado |
|---|---:|
| Registros originales | 541,909 |
| Columnas originales | 8 |
| Duplicados exactos detectados | 5,268 |
| Registros después de eliminar duplicados exactos | 536,641 |
| Descripciones vacías en el archivo original | 1,454 |
| CustomerID faltante en el archivo original | 135,080 |
| Cantidades negativas en el archivo original | 10,624 |
| Precios unitarios no positivos en el archivo original | 2,517 |
| Facturas cuyo número comienza con C | 9,288 |
| Fechas no interpretables | 0 |

Los identificadores de cliente faltantes se conservan como no identificados. Las cancelaciones, las cantidades negativas y los precios no positivos se conservan en el conjunto limpio para que puedan analizarse como excepciones. No se eliminan todas las líneas de una factura solo porque compartan el mismo InvoiceNo: cada fila puede representar un producto distinto de una misma factura.

## 2. Criterios para las ventas analizadas

Para construir los KPI comerciales se seleccionan filas con estas condiciones:

- La factura no comienza con C.
- Quantity es mayor que cero.
- UnitPrice es mayor que cero.
- Description no está vacía.
- InvoiceDate es válida.

El resultado es un conjunto de **524,878 líneas de venta candidatas**, con **19,960 facturas distintas**, **5,572,420 unidades** e ingresos por **£10,642,110.80**. Una factura puede contener varias líneas de producto; por eso las líneas de venta y las facturas distintas no son el mismo indicador.

## 3. Estadística descriptiva del dataset original

Los estadísticos se calcularon sobre los 541,909 registros originales, incluyendo duplicados, cancelaciones y devoluciones. La desviación estándar es muestral (ddof = 1).

| Variable | Media | Mediana | Moda | Desviación estándar |
|---|---:|---:|---:|---:|
| Quantity | 9.55225 | 3.00 | 1.00 | 218.08116 |
| UnitPrice (£) | 4.61111 | 2.08 | 1.25 | 96.75985 |
| TotalPrice (£) | 17.98779 | 9.75 | 15.00 | 378.81082 |

## 4. Estadística descriptiva de las ventas válidas

Se aplicaron los criterios de selección de ventas descritos anteriormente.

| Variable | Media | Mediana | Moda | Desviación estándar |
|---|---:|---:|---:|---:|
| Quantity | 10.61660 | 4.00 | 1.00 | 156.28003 |
| UnitPrice (£) | 3.92257 | 2.08 | 1.25 | 36.09303 |
| TotalPrice (£) | 20.27540 | 9.92 | 15.00 | 271.69357 |

## 5. Interpretación

- En ambos conjuntos, la media es superior a la mediana para las tres variables. Esto indica distribuciones asimétricas a la derecha, influidas por operaciones de importe o cantidad elevados.
- La desviación estándar de Quantity y TotalPrice es alta debido a valores extremos. Por ello, la mediana complementa a la media para describir una operación típica.
- La moda de Quantity es 1 unidad y la moda de UnitPrice es £1.25 en ambos conjuntos.
- Los valores negativos y los precios no positivos deben revisarse como devoluciones, cancelaciones o anomalías; no deben sumarse a los ingresos de ventas válidas.

## 6. Reproducibilidad

Las cifras se obtienen ejecutando `limpieza_eda.py` con el archivo fuente completo `data.csv`. El script conserva el archivo original y escribe los archivos derivados en `salida/`. Para repetir el proceso, consulta las instrucciones de instalación y ejecución en `README.md`.

**Nota:** `Venta candidata` es una etiqueta analítica definida por las reglas de limpieza; no equivale necesariamente a una factura completa o a una orden independiente.
