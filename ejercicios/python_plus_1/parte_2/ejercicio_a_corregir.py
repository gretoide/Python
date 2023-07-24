import pandas as pd


def usuarios_not_entrega1(log_file_path, case='none'):
    usuarios = pd.read_csv(log_file_path)

    # Desde el archivo reader de csv, crea una lista de comprension de los datos que visualizaron la entrega
    entrega_uno = usuarios[(usuarios['Contexto del evento'].str.contains('Tarea: Entrega 1')) &
                         (usuarios['Nombre evento'].str.contains('Se ha visualizado el estado de la entrega.'))]
    
    # Genera una lista con el nombre del usuario que vio la entrega, sin repeticiones en los datos
    usuarios_entrega = entrega_uno['Nombre completo del usuario'].unique()


    if case == 'a':
        usuarios['Nombre completo del usuario'] = usuarios['Nombre completo del usuario'].apply(lambda x: x.lower())
        usuarios_entrega= [user.lower() for user in usuarios_entrega]

    elif case == 'A':
        usuarios['Nombre completo del usuario'] = usuarios['Nombre completo del usuario'].apply(lambda x: x.upper())
        usuarios_entrega = [user.upper() for user in usuarios_entrega]
    
    usuarios_not_entrega = usuarios.groupby('Nombre completo del usuario').apply(lambda x: 'Tarea: Entrega 1' not in x['Contexto del evento'].values or 'Se ha visualizado el estado de la entrega.' not in x['Nombre evento'].values)
    usuarios_not_entrega = usuarios_not_entrega[usuarios_not_entrega].index.values

    return usuarios_not_entrega

# No utiliza os, el archivo podría no estar en la misma carpeta
log_file_path = 'log_catedras.csv'
case = 'none'  # Opciones: 'none', 'a', 'A'

with open(log_file_path, 'r') as f:
    users_no_entrega1 = usuarios_not_entrega1(f, case=case)

text='Usuario en el sistema'
print('-----------------------------------------')
print(text.center(30))
print('-----------------------------------------')
for user in users_no_entrega1:
    print(user.center(30,'-'))
