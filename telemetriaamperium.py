#Importar bibliotecas
import plotly.express as px
import pandas as pd
from mysql.connector import connect

#Estabelecer conexao com o banco de dados
def mysql_connection(host, port, user, passwd, database=None):
    connection = connect(
        host = host,
        port = port,
        user = user,
        passwd = passwd,
        database = database
    )
    return connection

connection = mysql_connection('sshproxy.cloudserver8.com', '33207', 'milhagem_trainee', 'Urban&DT2Campeoes2023', 'milhagem_mini_eco')

#Selecionar dados da tabela ina226
query = '''
    SELECT tensao, corrente FROM ina226
'''
cursor = connection.cursor()
cursor.execute(query)
result = cursor.fetchall()
for row in result:
  print(row)

columns = tuple([i[0] for i in cursor.description])
print(columns)

#Selecionar dados da tabela gps
query = '''
    SELECT latitude, longitude FROM gps
'''
cursor = connection.cursor()
cursor.execute(query)
result = cursor.fetchall()
for row in result:
  print(row)

columns = tuple([i[0] for i in cursor.description])
print(columns)

#Utilizar a tabela feita no excel para os dados do gráfico
print('Getting data...')
df = pd.read_excel("Dados.xlsx")
print(df.head(406))
print(df.tail(406))

#Criar e mostrar o mapa
fig = px.scatter_mapbox(df,
                        lon = df['longitude'],
                        lat = df['latitude'],
                        zoom = 15,
                        color = df['corrente'],
                        size = df['tensao'],
                        width = 1200,
                        height = 900,
                        title = 'Mapa Tensão e Corrente'
                    )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print('plot complete.')
