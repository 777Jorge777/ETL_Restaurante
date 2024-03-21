import pandas as pd

try:
    # Intenta leer el archivo CSV
    data = pd.read_csv('archivo.csv', nrows=3461)

    # Verifica la existencia de las columnas necesarias
    required_columns = ['Location', 'Price', 'Cuisine', 'Longitude', 'Latitude', 'Award', 'FacilitiesAndServices']
    missing_columns = [col for col in required_columns if col not in data.columns]

    if not missing_columns:
        # Selecciona solo las columnas necesarias
        selected_data = data[required_columns]
        
        
        
        # Modifica los valores de la columna 'Price'
        price_mapping = {'$': 'Muy Barato', '$$': 'Accesible', '$$$': 'Normal', '$$$$': 'Costoso', '$$$$$': 'Muy costoso'}
        selected_data['Price'] = selected_data['Price'].replace(price_mapping)
        
        price_mapping = {'¥': 'Muy Barato', '¥¥': 'Accesible', '¥¥¥': 'Normal', '¥¥¥¥': 'Costoso', '¥¥¥¥¥': 'Muy costoso'}
        selected_data['Price'] = selected_data['Price'].replace(price_mapping)
        
        price_mapping = {'€': 'Muy Barato', '€€': 'Accesible', '€€€': 'Normal', '€€€€': 'Costoso', '€€€€€': 'Muy costoso'}
        selected_data['Price'] = selected_data['Price'].replace(price_mapping)
        
        price_mapping = {'£': 'Muy Barato', '££': 'Accesible', '£££': 'Normal', '££££': 'Costoso', '£££££': 'Muy costoso'}
        selected_data['Price'] = selected_data['Price'].replace(price_mapping)

        
        

        # Crea la nueva columna 'Pais' y elimina la información de 'Location'
        selected_data.insert(0, 'Pais', selected_data['Location'].str.split(',').str[1].str.strip())
        selected_data['Location'] = selected_data['Location'].str.split(',').str[0].str.strip()

        # Crea las nuevas columnas 'Cuise1' y 'Cuise2' y elimina la información de 'Cuisine'
        selected_data.insert(3, 'Cuise1', selected_data['Cuisine'].str.split(',').str[0].str.strip())
        selected_data.insert(4, 'Cuise2', selected_data['Cuisine'].str.split(',').str[1].str.strip())
        
        # Elimina la columna 'Cuisine'
        selected_data.drop('Cuisine', axis=1, inplace=True)
        
        # Convierte las columnas 'Longitude' y 'Latitude' a tipo numérico
        selected_data['Longitude'] = pd.to_numeric(selected_data['Longitude'], errors='coerce')
        selected_data['Latitude'] = pd.to_numeric(selected_data['Latitude'], errors='coerce')

        # Divide la columna 'FacilitiesAndServices' en cinco nuevas columnas
        facilities_columns = selected_data['FacilitiesAndServices'].str.split(',', expand=True)
        for i in range(5):
            col_name = f'FacilitiesAndServices{i+1}'
            selected_data[col_name] = facilities_columns[i].str.strip()

        # Elimina la columna 'FacilitiesAndServices'
        selected_data.drop('FacilitiesAndServices', axis=1, inplace=True)

        print("Lectura exitosa, selección de columnas, creación de la columna 'Pais', modificación de 'Location' y división de 'FacilitiesAndServices' realizadas.")
        print("\nInformación del DataFrame resultante:\n")
        print(selected_data)

        # Guarda datos seleccionados en un nuevo archivo CSV
        selected_data.to_csv('nuevo_archivo.csv', index=False)

    else:
        print(f"Error: Faltan las siguientes columnas necesarias: {', '.join(missing_columns)}")

except FileNotFoundError:
    print("¡Error! Archivo no encontrado.")
except pd.errors.EmptyDataError:
    print("¡Error! El archivo está vacío.")
except pd.errors.ParserError:
    print("¡Error! Problema al analizar el archivo CSV.")
except Exception as e:
    print(f"¡Error inesperado! {e}")

