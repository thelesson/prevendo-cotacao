# -*- coding: utf-8 -*-
"""Prevendocotacao.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zw-F1Gf-LVINV9HYwquWRTqGvpV-mLvL

# Rede Neural Recorrente(LSTM) para prever o fechamento das ações de uma empresa, com base no preço das ações nos últimos 60 dias

**Importando as bibliotecas**
"""

import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = web.DataReader('WDOFUT', data_source='yahoo', start='2012-01-01', end='2020-11-18') 
#Exibindo os dados 
df

df.shape

"""**Criando gráfico para visualizar as datas**"""

plt.figure(figsize=(16,8))
plt.title('histórico de Fechamento de Preço')
plt.plot(df['Close'])
plt.xlabel('Data',fontsize=18)
plt.ylabel('Preço de Fechamento (R$)',fontsize=18)
plt.show()

"""**Criando um novo dataframe**"""

#Criando um novo dataframe com somente a coluna 'Close' 
data = df.filter(['Close'])
#Convertendo  o dataframe para um numpy array
dataset = data.values
#obter o número de linhas para conseguir treinar o modelo
training_data_len = math.ceil( len(dataset) *.8)

"""**Dimensionando o conjunto de dados**

Dimensionando o conjunto de dados para valores binários(0 e 1) antes de utilizar a rede neural
"""

scaler = MinMaxScaler(feature_range=(0, 1)) 
scaled_data = scaler.fit_transform(dataset)

"""**Criando um novo conjunto de dados que contenha os últimos 60 dias para conseguir prever o 61 dia**"""

#Criando o conjunto de dados de treinamento em escala 
train_data = scaled_data[0:training_data_len  , : ]
#Dividindo os dados em conjuntos de dados x_train e y_train
x_train=[]
y_train = []
for i in range(60,len(train_data)):
    x_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])

"""**Conversão**

Convertendo e matizes numpy para que possam ser usados no LSTM
"""

x_train, y_train = np.array(x_train), np.array(y_train)

"""Remodelando os dados para a forma tridimensional """

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

"""**MOdelo LSTM**

Construindo um modelo LSTM com 50 neurônios e duas camadas densas, uma com 25 neurônios e outra com 1 neurônio
"""

model = Sequential()
model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))

"""**Compilando o modelo**"""

model.compile(optimizer='adam', loss='mean_squared_error')

"""**Treinamento do Modelo**"""

model.fit(x_train, y_train, batch_size=1, epochs=1)

"""**Criando um conjunto de dados para teste**"""

#Testando o dataset
test_data = scaled_data[training_data_len - 60: , : ]
#Creiando o conjunto de dados x_test e  y_test 
x_test = []
y_test =  dataset[training_data_len : , : ] 
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])

"""**Convertendo o conjunto de dados em numpy array**"""

x_test = np.array(x_test)

"""**Remodelando**

Remodelando os dados para serem tridimensionais para que o LSTM possa executar
"""

x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

"""**Obtendo os valores previstos, usando dados de teste**"""

predictions = model.predict(x_test) 
predictions = scaler.inverse_transform(predictions)

"""**Obtendo o erro médio da raiz (RMsE)**

Quanto menor o valor, melhor o modelo
"""

rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
rmse

"""# **Traçando e visualizando os dados**"""

#Plotando os dados para o gráfico
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#Visualizando os dados
plt.figure(figsize=(16,8))
plt.title('Modelo')
plt.xlabel('Data', fontsize=18)
plt.ylabel('Preço de Fechamento ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Treinamento', 'Val', 'Predições'], loc='lower right')
plt.show()

"""# **Mostrando os preços válidos previstos**"""

valid

"""# **Prevendo o próximo dia**"""

#Pegando a cotação
apple_quote = web.DataReader('PETR4.SA', data_source='yahoo', start='2012-01-01', end='2020-11-18')
#Ciando um novo dataframe
new_df = apple_quote.filter(['Close'])
#Pegando os ultimos 60 dias 
last_60_days = new_df[-60:].values
#Escalando os dados para 0 e 1 
last_60_days_scaled = scaler.transform(last_60_days)
#Criando uma nova lista vazia
X_test = []
#AInserindo os 60 dias na lista
X_test.append(last_60_days_scaled)
#Convertendo o dataset X_test para numpy array 
X_test = np.array(X_test)
#Reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#Pegando o preço previsto
pred_price = model.predict(X_test)
#Revertendo a escala
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

"""verificando o valor real da cotação """

apple_quote2 = web.DataReader('PETR4.SA', data_source='yahoo', start='2020-11-19', end='2020-11-19')
print(apple_quote2['Close'])