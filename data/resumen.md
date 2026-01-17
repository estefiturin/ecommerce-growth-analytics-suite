# VENTA MINORISTA EN LINEA

Un conjunto de datos reales de transacciones de ventas minoristas en linea de dos años. No tiene establecimiento físico y tiene
sede en Reino Unido. Las transacciones tienen fecha entre el 01/12/2009 y el 09/12/2011.
La empresa vende principalmente artículos de regalo únicos para cualquier ocasión. Muchos de sus clientes son mayoristas.

### Columnas de la tabla

- InvoiceNo: Número de factura. Nominal. Un número entero de 6 dígitos asignado de manera única a cada transacción. Si este código comienza con la letra “C”, indica una cancelación.
- StockCode: Código de producto (artículo). Nominal. Un número entero de 5 dígitos asignado de manera única a cada producto distinto.
- Description: Descripción del producto (artículo). Nominal. Nombre del producto.
- Quantity: Cantidad. Numérico. Número de unidades de cada producto (artículo) por transacción.
- InvoiceDate: Fecha y hora de la factura. Numérico. El día y la hora en que se generó la transacción.
- UnitPrice: Precio unitario. Numérico. Precio del producto por unidad en libras esterlinas (£).
- CustomerID: Identificador del cliente. Nominal. Un número entero de 5 dígitos asignado de manera única a cada cliente.
- Country: País. Nominal. Nombre del país donde reside el cliente.

## Librerias Instaladas

* **Pandas:** Manipulación de datos (como un Excel con esteroides).
* **NumPy:** Cálculo numérico matricial.
* **Matplotlib/Seaborn:** Visualización gráfica.
* **Scipy/Statsmodels:** El corazón estadístico (para tus pruebas Z, T, ANOVA).
* **Scikit-learn:** Para regresiones y algoritmos de ML.
