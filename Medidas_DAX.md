# Medidas DAX | E-Commerce Analytics

**Importante:** las medidas con FORMAT son solo para mostrar cifras en tarjetas. Para gráficos y cálculos usa siempre las medidas numéricas.

Importa salida/data_limpio.csv en Power BI y asigna a la tabla el nombre **Operaciones**. Si tu tabla tiene otro nombre, adapta las referencias en las fórmulas.

## Medidas numéricas base

~~~dax
Ingresos de ventas =
CALCULATE(
    SUM(Operaciones[TotalPrice]),
    Operaciones[TipoOperacion] = "Venta candidata"
)
~~~

~~~dax
Facturas distintas =
CALCULATE(
    DISTINCTCOUNT(Operaciones[InvoiceNo]),
    Operaciones[TipoOperacion] = "Venta candidata"
)
~~~

~~~dax
Ticket promedio por factura =
DIVIDE(
    [Ingresos de ventas],
    [Facturas distintas],
    0
)
~~~

~~~dax
Unidades vendidas =
CALCULATE(
    SUM(Operaciones[Quantity]),
    Operaciones[TipoOperacion] = "Venta candidata"
)
~~~

~~~dax
Lineas de venta =
CALCULATE(
    COUNTROWS(Operaciones),
    Operaciones[TipoOperacion] = "Venta candidata"
)
~~~

~~~dax
Unidades promedio por factura =
DIVIDE(
    [Unidades vendidas],
    [Facturas distintas],
    0
)
~~~

~~~dax
Productos distintos vendidos =
CALCULATE(
    DISTINCTCOUNT(Operaciones[StockCode]),
    Operaciones[TipoOperacion] = "Venta candidata"
)
~~~

~~~dax
Clientes identificados =
CALCULATE(
    DISTINCTCOUNT(Operaciones[CustomerID]),
    FILTER(
        Operaciones,
        Operaciones[TipoOperacion] = "Venta candidata"
            && NOT ISBLANK(Operaciones[CustomerID])
    )
)
~~~

## Medidas para excepciones operativas

Los textos deben coincidir exactamente con los valores que aparecen en TipoOperacion. El script limpieza_eda.py genera los siguientes:

~~~dax
Facturas canceladas =
CALCULATE(
    DISTINCTCOUNT(Operaciones[InvoiceNo]),
    Operaciones[TipoOperacion] = "Cancelación (factura C)"
)
~~~

~~~dax
Lineas de cancelacion =
CALCULATE(
    COUNTROWS(Operaciones),
    Operaciones[TipoOperacion] = "Cancelación (factura C)"
)
~~~

~~~dax
Devoluciones =
CALCULATE(
    COUNTROWS(Operaciones),
    Operaciones[TipoOperacion] = "Cantidad negativa / devolución"
)
~~~

~~~dax
Precios no positivos =
CALCULATE(
    COUNTROWS(Operaciones),
    Operaciones[TipoOperacion] = "Precio no positivo"
)
~~~

## Medidas de presentación para tarjetas

~~~dax
Ingresos tarjeta =
FORMAT([Ingresos de ventas], "£#,##0.00", "en-US")
~~~

~~~dax
Facturas tarjeta =
FORMAT([Facturas distintas], "#,##0", "en-US")
~~~

~~~dax
Ticket tarjeta =
FORMAT([Ticket promedio por factura], "£#,##0.00", "en-US")
~~~

## Visualizaciones propuestas

### Vista gerencial / administrativa
- Tarjetas: ingresos de ventas, facturas distintas y ticket promedio por factura.
- Línea: ingresos por mes.
- Barras: ingresos por país (Top 10).
- Barras: productos más vendidos por unidades (Top 10).
- Columnas: unidades vendidas por mes.
- Barras: ticket promedio por país (Top 10).
- Segmentadores: fecha y país.

### Vista operativa / empleados
- Tarjetas: unidades vendidas, líneas de venta, unidades promedio por factura y facturas canceladas.
- Línea: actividad diaria de ventas.
- Barras: productos con mayor movimiento (Top 10).
- Columnas: facturas canceladas por fecha.
- Barras: facturas por país (Top 10).
- Columnas: devoluciones por mes.
- Segmentadores: fecha y país.

## Limitaciones del dataset

El dataset contiene facturas, productos, cantidades, precios, fechas, clientes (cuando están identificados) y países. No contiene identificadores de empleados, turnos ni metas individuales. La vista operativa mide actividad y excepciones comerciales, no productividad individual del personal.

Si las categorías de tu archivo de Power BI aparecen en minúsculas o sin acentos, conserva en cada medida el texto exacto que aparece en Power Query.
