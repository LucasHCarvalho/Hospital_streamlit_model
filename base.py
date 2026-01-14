import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Definindo parâmetros de simulação
np.random.seed(42)
local_hospital = ['Ala Norte', 'Ala Sul', 'Centro Cirúrgico', 'Pronto Socorro']
procedimentos = ['Cirurgia Geral', 'Exames de Imagem', 'Consultas', 'Tratamentos']
cids = ['A00-A09', 'B20-B24', 'C00-C14', 'D50-D53', 'E00-E07']

# Gerando dados simulados
n = 3000  # Número de registros
data = [datetime.now() - timedelta(days=random.randint(0, 865)) for _ in range(n)]
faturamento = [random.uniform(100, 10000) for _ in range(n)]
local = [random.choice(local_hospital) for _ in range(n)]
procedimento = [random.choice(procedimentos) for _ in range(n)]
idade = [random.randint(18, 90) for _ in range(n)]
cid = [random.choice(cids) for _ in range(n)]

# Criando o DataFrame
df = pd.DataFrame({
    'Data': data,
    'Faturamento': faturamento,
    'Local': local,
    'Procedimento': procedimento,
    'Idade': idade,
    'CID': cid
})

# Convertendo a coluna 'Data' para datetime
df['Data'] = pd.to_datetime(df['Data'])

# Exibindo as primeiras linhas da base de dados
df.head()

df.to_csv("hospital_data.csv", index=False)