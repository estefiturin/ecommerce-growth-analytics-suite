import pandas as pd
import numpy as np 

class DataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
    
    def cargar_datos(self):
        """Carga el Excel original"""
        print("Cargando datos... esto puede tardar un poco.")
        # Usamos engine='openpyxl' para leer xlsx
        self.df = pd.read_excel(self.file_path, sheet_name="Year 2009-2010")
        print(f"Datos cargados: {self.df.shape}")

    def limpiar_datos(self):
        """Ejecuta todo el pipeline de limpieza que diseñamos en el notebook"""
        if self.df is None:
            raise Exception("Primero debes cargar los datos.")

        # 1. Copia independiente
        df_clean = self.df.copy()

        # 2. Filtrado básico (Quantity y Price > 0)
        df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Price'] > 0)]

        # 3. Casteo de tipos
        df_clean['Customer ID'] = df_clean['Customer ID'].astype(str)
        df_clean['Invoice'] = df_clean['Invoice'].astype(str)

        # 4. Imputación de Nulos (Guest)
        df_clean['Customer ID'] = df_clean['Customer ID'].replace('nan', 'Guest')
        df_clean['Customer ID'] = df_clean['Customer ID'].fillna('Guest')

        # 5. Columna Total Venta
        df_clean['Total_Venta'] = df_clean['Quantity'] * df_clean['Price']

        # 6. Lista Negra (Eliminar gastos no-producto)
        black_list = ['Manual', 'POST', 'DOTCOM POSTAGE', 'AMAZON FEE', 'BANK CHARGES', 'CRUK Commission', 'Discount']
        
        df_clean = df_clean[
            (~df_clean['Description'].isin(black_list)) & 
            (df_clean['StockCode'] != 'POST') & 
            (df_clean['StockCode'] != 'D') &
            (df_clean['Price'] < 3000)
        ]

        print(f"Limpieza completada. Filas finales: {df_clean.shape}")
        return df_clean

# Bloque de prueba (solo se ejecuta si corres este archivo directamente)
if __name__ == "__main__":
    # Asegúrate de que el nombre del archivo coincida con el tuyo
    cleaner = DataCleaner("data/online_retail_II.xlsx") 
    cleaner.cargar_datos()
    df_final = cleaner.limpiar_datos()
    
    # Guardamos el resultado limpio en un CSV ligero para que la App cargue rápido
    df_final.to_csv("datos_limpios.csv", index=False)
    print("Archivo 'datos_limpios.csv' guardado con éxito.")
    