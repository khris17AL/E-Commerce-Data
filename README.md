# E-Commerce Analytics

Proyecto académico de análisis de datos de comercio electrónico con Python, Power BI, Visual Studio Code y GitHub.

## Objetivo

Analizar el conjunto Online Retail, documentar limpieza y análisis exploratorio (EDA), y construir dos vistas de Power BI a partir del mismo conjunto de datos:

- **Vista gerencial / administrativa:** ingresos, facturas, ticket promedio, tendencias, productos y mercados.
- **Vista operativa / empleados:** actividad de ventas, unidades, productos con mayor movimiento y seguimiento de cancelaciones y devoluciones.

> **Limitación del dataset:** no incluye identificadores de empleados, turnos ni metas individuales. La vista operativa permite monitorear operaciones comerciales, pero no atribuir productividad a trabajadores concretos.

## Tecnologías

- Python 3, pandas y NumPy.
- Power BI Desktop y DAX.
- Visual Studio Code.
- Git y GitHub.

## Dataset

El archivo fuente debe llamarse `data.csv` y contener: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

El archivo original utilizado contiene **541,909 registros y 8 columnas**. Por tamaño y licencia/origen, el CSV no se versiona en este repositorio: colócalo localmente junto a `limpieza_eda.py` antes de ejecutar el análisis.

## Archivos del repositorio

- `limpieza_eda.py`: proceso reproducible de limpieza y EDA.
- `requirements.txt`: dependencias de Python.
- `Medidas_DAX.md`: medidas DAX, propuestas de visualización y limitaciones.
- `E-Commerce Data.PY`: ejercicio inicial de estadística descriptiva.
- `E-Commerce Data.pbix`: archivo de Power BI actualmente versionado.
- `index.html`: prototipo web complementario.

Los resultados de ejecución se crean localmente en `salida/` y se excluyen de Git mediante `.gitignore`.

## Preparar y ejecutar en Visual Studio Code

1. Clona el repositorio y abre la carpeta en VS Code.
2. Copia el archivo original `data.csv` en la raíz del proyecto.
3. Abre **Terminal → Nueva terminal**.
4. Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

5. Ejecuta:

```bash
python limpieza_eda.py
```

El script no modifica el CSV original. Genera estos archivos en `salida/`:

| Archivo | Contenido |
|---|---|
| `data_limpio.csv` | Registros sin duplicados exactos; conserva cancelaciones y devoluciones clasificadas |
| `data_ventas.csv` | Filas seleccionadas para KPI de ventas |
| `reporte_calidad.csv` | Recuentos de calidad y decisiones de limpieza |
| `estadisticas_descriptivas.csv` | Media, mediana, moda, desviación estándar muestral, mínimo y máximo |
| `resumen_mensual.csv` | Ingresos, unidades, líneas y facturas por mes |
| `productos_resumen.csv` | Ingresos, unidades y facturas por producto |
| `paises_resumen.csv` | Ingresos, unidades y facturas por país |

## Criterios de limpieza

- Normaliza espacios en texto y convierte fechas y variables numéricas.
- Elimina duplicados exactos; no elimina todas las líneas que comparten una factura.
- Conserva cancelaciones, cantidades negativas/devoluciones y precios no positivos en `data_limpio.csv`, clasificándolos mediante `TipoOperacion`.
- Conserva `CustomerID` faltantes como clientes no identificados; no inventa identificadores.
- Calcula `TotalPrice = Quantity × UnitPrice`.
- `data_ventas.csv` incluye facturas que no comienzan con C, cantidad y precio positivos, descripción disponible y fecha válida.

La etiqueta **Venta candidata** es una clasificación analítica según esos criterios, no una garantía de que cada fila represente una orden comercial independiente. Una factura puede contener varias líneas de producto.

## Valores de referencia verificados

Al ejecutar el proceso sobre el CSV fuente completo con los criterios incluidos en el script, se esperan:

- Registros originales: **541,909**.
- Registros después de eliminar duplicados exactos: **536,641**.
- Filas seleccionadas para ventas válidas: **524,878**.
- Facturas distintas en ventas válidas: **19,960**.
- Unidades de ventas válidas: **5,572,420**.
- Ingresos de ventas válidas: **£10,642,110.80**.

Si tus resultados difieren, verifica que utilizas el archivo fuente completo y que no cambiaste los criterios de limpieza.

## Power BI y DAX

Importa `salida/data_limpio.csv` en Power BI y asigna a la tabla el nombre `Operaciones` (o adapta el nombre en las fórmulas). Revisa estos tipos:

- `InvoiceNo`: texto, para conservar facturas con prefijo C.
- `InvoiceDate`: fecha/hora.
- `Quantity`: número entero.
- `UnitPrice` y `TotalPrice`: número decimal.

Consulta [Medidas_DAX.md](Medidas_DAX.md) para las medidas numéricas, medidas de presentación y visualizaciones sugeridas. Las medidas que usan `FORMAT` son solo para tarjetas; utiliza las medidas numéricas originales en gráficos y cálculos.

## Control de versiones

Después de guardar y validar la versión final del PBIX:

```bash
git status
git add README.md Medidas_DAX.md limpieza_eda.py requirements.txt .gitignore
git commit -m "Documenta limpieza, EDA y medidas DAX"
git push
```

Sube el PBIX final en un commit separado si lo modificaste. No subas `data.csv` ni `salida/`: los archivos generados pueden reconstruirse ejecutando el script.

## Lista de verificación para entrega

- [ ] El script se ejecuta sin errores y genera los archivos de `salida/`.
- [ ] El reporte estadístico incluye media, mediana, moda y desviación estándar.
- [ ] Cada página de Power BI contiene al menos cinco visualizaciones.
- [ ] Las tarjetas y gráficos utilizan medidas DAX adecuadas.
- [ ] Los segmentadores de fecha y país filtran los visuales esperados.
- [ ] El PBIX final local coincide con el que está en GitHub.
- [ ] README y evidencias están actualizados.
