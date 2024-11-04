import pandas as pd
import sqlite3


data_url_ate_2021 = "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela992.xlsx&terr=N&rank=-&query=t/992/n3/all/v/707,1000707/p/all/c12762/117839,117844/c319/104029/c2703/117933/d/v1000707%202/l/v,p%2Bc12762%2Bc319,t%2Bc2703"
data_url_depois_2021 = "https://sidra.ibge.gov.br/geratabela?format=xlsx&name=tabela7528.xlsx&terr=N&rank=-&query=t/7528/n3/all/v/707,1000707/p/all/c12762/117839,117844/c319/104029/c2703/117933/d/v1000707%202/l/v,p%2Bc12762%2Bc319,t%2Bc2703"


data_ate_2021 = pd.read_excel(data_url_ate_2021, skiprows=5)
data_depois_2021 = pd.read_excel(data_url_depois_2021, skiprows=5)


print("Colunas da tabela até 2021:", data_ate_2021.columns.tolist())
print("Colunas da tabela depois de 2021:", data_depois_2021.columns.tolist())


colunas_relevantes_ate_2021 = ['Unnamed: 0', 'Unnamed: 1', 'Total', 'Total.1', 'Total.2']
colunas_relevantes_depois_2021 = ['Unnamed: 0', 'Unnamed: 1', 'Total', 'Total.1']


data_ate_2021 = data_ate_2021[colunas_relevantes_ate_2021].rename(columns={
    'Unnamed: 0': 'classificacao_atividade',
    'Unnamed: 1': 'ano',
    'Total': 'sigla_estado', 
    'Total.1': 'variavel',
    'Total.2': 'quantidade'
})

data_depois_2021 = data_depois_2021[colunas_relevantes_depois_2021].rename(columns={
    'Unnamed: 0': 'classificacao_atividade',
    'Unnamed: 1': 'ano',
    'Total': 'sigla_estado',
    'Total.1': 'quantidade'
})


data_depois_2021['variavel'] = pd.NA


data = pd.concat([data_ate_2021, data_depois_2021], ignore_index=True)


conn = sqlite3.connect('dados_sidra.db')
data.to_sql('tabela_sidra', conn, if_exists='replace', index=False)


query = "SELECT * FROM tabela_sidra"
data_from_db = pd.read_sql_query(query, conn)
print("Dados armazenados no banco de dados:\n", data_from_db)


conn.close()

print("Dados armazenados com sucesso no banco de dados 'dados_sidra.db'!")
