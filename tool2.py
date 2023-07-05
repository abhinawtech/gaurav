
import requests
import json
import pandas as pd
import xlwings as xw
from datetime import datetime
import time as time
import numpy as np

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot

con = pd.read_excel('C:\\Users\\LENOVO\\Desktop\\Market Tool\\Continuation_doji.xlsx')
conso = pd.read_excel('C:\\Users\\LENOVO\\Desktop\\Market Tool\\Consolidation.xlsx')
last_day = pd.read_excel('C:\\Users\\LENOVO\\Desktop\\Market Tool\\Last_Day_Data.xlsx')

# # # ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
# series = st.sidebar.multiselect(
#     "Select the Stock:",
#     options=df["SERIES"].unique(),
#     default=df["SERIES"].unique()
# )
###### This header works for FnO stocks #####

# ---- MAINPAGE ----

st.set_page_config(page_title="Stock-o-Meter", layout="wide")
#st.set_page_config(layout="wide")
st.title(":bar_chart: Intraday Stocks")
st.markdown("##")

# --------------------------------------------------------
# Nifty 50

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%H:%M:%S")
print("date and time =", dt_string)

date_time_str = '09:15:00'
date_time_obj = datetime.strptime(dt_string, '%H:%M:%S')
date_time_obj2 = datetime.strptime(date_time_str, '%H:%M:%S')


date_dif_mins = (date_time_obj - date_time_obj2 ).total_seconds()/60.0

headers = {"accept-encoding" : "gzip, deflate, br",
           "accept-language" : "en-US,en;q=0.9",
           "referer" : "https://www.nseindia.com/option-chain",
           "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050", headers = headers )
d = response.json()


#Spurts - 5th column 
# response = requests.get(url = "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings",  headers = headers )
# d = response.json()

d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
nifty50 = pd.DataFrame.from_dict(d2).transpose()
nifty50 = nifty50[nifty50['priority'] == 0]
nifty50_2 = nifty50.drop(['priority'],axis = 1)
nifty50_3 = nifty50.drop(['meta'],axis = 1)
nifty50_4 = nifty50_3.drop(['chartTodayPath'],axis = 1)
nifty50_5 = nifty50_4.drop(['chart30dPath'],axis = 1)
#nifty50_5['+ve_per_ch'] = abs(nifty50_5['pChange'])

nifty50_5 = nifty50_5.sort_values(by=['pChange'], ascending=(False))


nifty50_green = nifty50_5[nifty50_5['pChange'] >0]
nifty50_red = nifty50_5[nifty50_5['pChange'] <0]
#niftyfno2 = niftyfno1.iloc[:50]
#niftyfno2 = niftyfno2.sort_values(by=['pChange'], ascending=(False))

symbol = nifty50_green['symbol']
per_change = nifty50_green['pChange']
value = nifty50_green['totalTradedValue']

green = px.treemap(nifty50_green,
                 path = [symbol, per_change],
                 color = per_change,
                 values = value,
                 color_continuous_scale='greens',
                 title = 'Long',
                 hover_name = 'pChange',
                 width=720, 
                 height=500,
                 
    )

green.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )
#plot(green)

nifty50_red = nifty50_5[nifty50_5['pChange'] <0]
symbol = nifty50_red['symbol']
per_change = nifty50_red['pChange']
value = nifty50_red['totalTradedValue']

red = px.treemap(nifty50_red,
                 path = [symbol, per_change],
                 color = per_change,
                 values = value,
                 color_continuous_scale='reds',
                 title = 'Short',
                 hover_name = 'pChange',
                 width=720, 
                 height=500,
                 
    )

red.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )
import plotly.graph_objects as go
Adv = nifty50_green['symbol'].nunique()
Dec = nifty50_red['symbol'].nunique()
adv = (Adv/50)*100
dec = (Dec/50)*100
if Adv > Dec:
    pe = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = adv,
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [None, 100]},
    'bar': {'color': "Green"}},
    title = {'text': "Advance ratio"}))
    pe.update_layout(height=600, width=400) 
    #st.plotly_chart(pe)
    
else:
    pe = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = dec,
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [None, 100]},
    'bar': {'color': "Red"}},
    title = {'text': "Decline ratio"}))
    pe.update_layout(height=600, width=400) 
    #st.plotly_chart(pe)
    
#adv_dec = Adv/Dec
# All Indices 
headers = {"accept-encoding" : "gzip, deflate, br",
            "accept-language" : "en-US,en;q=0.9",
            #"cookie" : '_ga=GA1.1.1639296451.1668248767; defaultLang=en; AKA_A2=A; nsit=rHriXSCYEbHzGIk1WCinH8Q7; bm_mi=37094924FF4A0B5C5F2CF020E38618F5~YAAQTUo5Fwv04Z+HAQAAjaA2pBMNugY7EWXgONkQm+f6vPiji8Hfjp711Ke4IdH9zNy2D/gsV3G9U/IKqYINgUkyEMonXqKfvUrBFGFEt/v88TesTVRHMTsHnlYJNIbqXM9z7qGzEyrMnm7QZ9gn+wn46fBi4nXV+COD/viuwPyOM6HEpmA2FRx3JGSrQtTCj/KtgND3NO8ZAh8VDsqTrkioLMRCECpUj30JjdqffKbouDN7dtIjx91nfg4TNISy0JVUNuLECklrjUmt/g4Q5VS5REc9rRlgSpbNgHR3ncQTlqXggVRihOQi4DzGYrdc4n0kJtXVUrVm6sjXHpNbSA8P9Mq7n/0v1SDjI23p~1; ak_bmsc=27D8AF428D6F3A252945BBBDF206FC4B~000000000000000000000000000000~YAAQbG0/Fznj4p+HAQAAoqk2pBPDoKRTndgHwAZSvaiC34u1MEPCE9mVxctK5q8HxRu7T6bVR4KupYJRk3/HYIbwN3s+noglQMg4Uvbq1fD7IMerh9V5hxyg68nYl35Ei4wE9SmhGxf+t4qinAsdEcs8Ec9v8IQWU6pi93raUNyTFWqAR4Z/xlCeMGRbPiynW4NJYEUu2iFS9NFlijJcYvmsV5pymTGoE2USHUv0wtKk9NXaXRG/26yGxSeFD1lLIAX/2LiVxBWQN+NSGbU9dlIH1ZipumpFSGtCNz4YhRxIxPAfpOghJncvYCZL0JCNihxTSRqRfxQbUGDrEhofcNjVPVCH22s15g8MY86kTY4nga84pQkAE4fBTz1lX01dvlRAXtyC1KxJhDNTryo/+BLzkNW+jiml8nPicE7V0w2EBDbSr8y9DQWMCUDvqtNlTQA2NTWOveEhpuQD; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY4MjA4NzQ2NiwiZXhwIjoxNjgyMDk0NjY2fQ.k0SkEApqYOQaDdp7ubYmFm2xLPlbHOhLL5jONbYQaLo; RT="z=1&dm=nseindia.com&si=4492f034-3542-43d0-9a47-1c23f9376e4f&ss=lgq1eqil&sl=0&tt=0&bcn=%2F%2F684d0d44.akstat.io%2F',
            "referer" : "https://www.nseindia.com/option-chain",
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            #"x-requested-with" : "XMLHttpRequest"
            }

response = requests.get(url = "https://www.nseindia.com/api/allIndices", headers = headers )
d = response.json()


d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
indices = pd.DataFrame.from_dict(d2).transpose()
sectoral_indices = indices[indices['key'] == "SECTORAL INDICES"]
#nifty50 = nifty50[nifty50['priority'] == 0]
#nifty50_2 = nifty50.drop(['priority'],axis = 1)
sectoral_indices = sectoral_indices.drop(['key'],axis = 1)
sectoral_indices2 = sectoral_indices[['index','percentChange']]
sectoral_indices2 = sectoral_indices2.sort_values(by=['percentChange'], ascending=(False))

def func(row):
    if row['percentChange'] >=0:
        return "Green"
    elif row['percentChange'] == 0:
        return "No color"
    elif row['percentChange'] < 0:
        return "Red"
    else:
        return ""
sectoral_indices2['color']  = sectoral_indices2.apply(func, axis=1) 

sectors = px.bar(sectoral_indices2, x="index", y="percentChange",
             color='color',   # if values in column z = 'some_group' and 'some_other_group'
    color_discrete_map={
        'Green': 'Green',
        'Red': 'Red',
        'No color' : 'White',
    }, barmode='group',
    width = 700,
             height=600,)

left_column, right_column = st.columns(2)
left_column.plotly_chart(pe, use_container_width=False)
right_column.plotly_chart(sectors, use_container_width=False)

#title = st.text_input('Movie title', 'Life of Brian')
#st.write('Advanced', Adv)
#st.write('Declined', Dec)
#st.write('Advance_Decline_Ratio', adv_dec)

left_column, right_column = st.columns(2)
left_column.plotly_chart(green, use_container_width=False)
right_column.plotly_chart(red, use_container_width=False)




#st.plotly_chart(sectors)

# green_indices = sectoral_indices2[sectoral_indices2['percentChange'] >=0]
# red_indices = sectoral_indices2[sectoral_indices2['percentChange'] <0]


# fig2 = px.bar(green_indices, x=green_indices['index'], y=green_indices["percentChange"], color=green_indices["percentChange"],width=700, height=500)
# fig2.for_each_trace(
#     lambda trace: trace.update(marker_color=np.where(green_indices['percentChange'] > 0, 'Green', 'Green'))
# )
# fig2.update_layout(showlegend=False)  # Hide legend because there is no distinct group
# #plot(fig2)

# fig3 = px.bar(red_indices, x=red_indices['index'], y=red_indices["percentChange"], color=red_indices["percentChange"],width=700, height=500)
# fig3.for_each_trace(
#     lambda trace: trace.update(marker_color=np.where(red_indices['percentChange'] < 0, 'Red', 'Red'))
# )
# fig3.update_layout(showlegend=False) 
# #plot(fig3)
# #st.plotly_chart(fig2)

# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig2, use_container_width=False)
# right_column.plotly_chart(fig3, use_container_width=False)


# =============================================================================
# # NIFTY FNO
# =============================================================================
headers = {"accept-encoding" : "gzip, deflate, br",
            "accept-language" : "en-US,en;q=0.9",
            #"cookie" : '_ga=GA1.1.1639296451.1668248767; defaultLang=en; AKA_A2=A; nsit=rHriXSCYEbHzGIk1WCinH8Q7; bm_mi=37094924FF4A0B5C5F2CF020E38618F5~YAAQTUo5Fwv04Z+HAQAAjaA2pBMNugY7EWXgONkQm+f6vPiji8Hfjp711Ke4IdH9zNy2D/gsV3G9U/IKqYINgUkyEMonXqKfvUrBFGFEt/v88TesTVRHMTsHnlYJNIbqXM9z7qGzEyrMnm7QZ9gn+wn46fBi4nXV+COD/viuwPyOM6HEpmA2FRx3JGSrQtTCj/KtgND3NO8ZAh8VDsqTrkioLMRCECpUj30JjdqffKbouDN7dtIjx91nfg4TNISy0JVUNuLECklrjUmt/g4Q5VS5REc9rRlgSpbNgHR3ncQTlqXggVRihOQi4DzGYrdc4n0kJtXVUrVm6sjXHpNbSA8P9Mq7n/0v1SDjI23p~1; ak_bmsc=27D8AF428D6F3A252945BBBDF206FC4B~000000000000000000000000000000~YAAQbG0/Fznj4p+HAQAAoqk2pBPDoKRTndgHwAZSvaiC34u1MEPCE9mVxctK5q8HxRu7T6bVR4KupYJRk3/HYIbwN3s+noglQMg4Uvbq1fD7IMerh9V5hxyg68nYl35Ei4wE9SmhGxf+t4qinAsdEcs8Ec9v8IQWU6pi93raUNyTFWqAR4Z/xlCeMGRbPiynW4NJYEUu2iFS9NFlijJcYvmsV5pymTGoE2USHUv0wtKk9NXaXRG/26yGxSeFD1lLIAX/2LiVxBWQN+NSGbU9dlIH1ZipumpFSGtCNz4YhRxIxPAfpOghJncvYCZL0JCNihxTSRqRfxQbUGDrEhofcNjVPVCH22s15g8MY86kTY4nga84pQkAE4fBTz1lX01dvlRAXtyC1KxJhDNTryo/+BLzkNW+jiml8nPicE7V0w2EBDbSr8y9DQWMCUDvqtNlTQA2NTWOveEhpuQD; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY4MjA4NzQ2NiwiZXhwIjoxNjgyMDk0NjY2fQ.k0SkEApqYOQaDdp7ubYmFm2xLPlbHOhLL5jONbYQaLo; RT="z=1&dm=nseindia.com&si=4492f034-3542-43d0-9a47-1c23f9376e4f&ss=lgq1eqil&sl=0&tt=0&bcn=%2F%2F684d0d44.akstat.io%2F',
            "referer" : "https://www.nseindia.com/option-chain",
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            #"x-requested-with" : "XMLHttpRequest"
            }

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O", headers = headers )
d = response.json()



d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
nifty50 = pd.DataFrame.from_dict(d2).transpose()
#nifty50 = nifty50[nifty50['priority'] == 0]
#nifty50_2 = nifty50.drop(['priority'],axis = 1)
nifty50_3 = nifty50.drop(['meta'],axis = 1)
niftyfno = nifty50_3.drop(['chartTodayPath'],axis = 1)
niftyfno1 = niftyfno.drop(['chart30dPath'],axis = 1)
niftyfno1['+ve_per_ch'] = abs(niftyfno1['pChange'])

niftyfno1 = niftyfno1.sort_values(by=['+ve_per_ch'], ascending=(False))



niftyfno2 = niftyfno1.iloc[:50]
niftyfno2 = niftyfno2.sort_values(by=['pChange'], ascending=(False))

symbol = niftyfno2['symbol']
per_change = niftyfno2['pChange']
value = niftyfno2['totalTradedValue']

fig = px.treemap(niftyfno2,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Moneyflux',
                  hover_name = 'pChange',
                  width=1450, 
                  height=700
    )

fig.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )
#plot(fig)
st.plotly_chart(fig)

niftyfno1['Traded_value_per_min'] =  niftyfno1['totalTradedValue']/abs(date_dif_mins)

niftyfno1_1= pd.merge(niftyfno1,last_day, how='left',left_on=['symbol'],right_on=['Symbol'])
niftyfno1_1['Volume_factor'] = niftyfno1_1['Traded_value_per_min_x']/niftyfno1_1['Traded_value_per_min_y']
niftyfno1_1 = niftyfno1_1.sort_values(by=['Volume_factor'], ascending=(False))
niftyfno1_1['row_num2'] = np.arange(len(niftyfno1_1))
niftyfno1_1 = niftyfno1_1[niftyfno1_1['row_num2'] <= 14]

fig2 = px.bar(niftyfno1_1, x=niftyfno1_1['symbol'], y=niftyfno1_1["Volume_factor"], color=niftyfno1_1["Volume_factor"],width=1400, height=500)
fig2.for_each_trace(
    lambda trace: trace.update(marker_color=np.where(niftyfno1_1['Volume_factor'] > 0, 'Green', 'Green'))
)
fig2.update_layout(showlegend=False)  # Hide legend because there is no distinct group
#plot(fig2)
st.plotly_chart(fig2)


symbol = niftyfno1_1['symbol']
per_change = niftyfno1_1['pChange']
value = niftyfno1_1['Volume_factor']

VF = px.treemap(niftyfno1_1,
                 path = [symbol, per_change],
                 color = per_change,
                 values = value,
                 color_continuous_scale='RdYlGn',
                 title = 'Volume_Factor',
                 hover_name = 'pChange',
                 width=1450, 
                 height=700,
                 
    )

VF.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(VF)
st.plotly_chart(VF)


######
#CON DOJI

con_symbol = pd.DataFrame(con['Symbol'])
nifty_con = niftyfno1.merge(con_symbol, left_on='symbol', right_on = 'Symbol')

symbol = nifty_con['symbol']
per_change = nifty_con['pChange']
value = nifty_con['totalTradedValue']

con = px.treemap(nifty_con,
                 path = [symbol, per_change],
                 color = per_change,
                 values = value,
                 color_continuous_scale='RdYlGn',
                 title = 'Con Doji',
                 hover_name = 'pChange',
                 width=1450, 
                 height=700,
                 
    )

con.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )
#plot(con)
st.plotly_chart(con)

#####


######
#Consolidation

conso_symbol = pd.DataFrame(conso['Symbol']).drop_duplicates()
nifty_con = niftyfno1.merge(conso_symbol, left_on='symbol', right_on = 'Symbol')

symbol = nifty_con['symbol']
per_change = nifty_con['pChange']
value = nifty_con['totalTradedValue']

conso = px.treemap(nifty_con,
                 path = [symbol, per_change],
                 color = per_change,
                 values = value,
                 color_continuous_scale='RdYlGn',
                 title = 'Consolidation',
                 hover_name = 'pChange',
                 width=1450, 
                 height=700,
                 
    )

conso.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )
#plot(con)
st.plotly_chart(conso)

# # =============================================================================
# # #### Nifty Bank #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftybank = pd.DataFrame.from_dict(d2).transpose()
niftybank = niftybank[niftybank['priority'] == 0]
niftybank_2 = niftybank.drop(['priority'],axis = 1)
niftybank_3 = niftybank_2.drop(['meta'],axis = 1)


symbol = niftybank_3['symbol']
per_change = niftybank_3['pChange']
value = niftybank_3['totalTradedValue']

fig_bank = px.treemap(niftybank_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty Bank',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_bank.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)


# # =============================================================================
# # #### Nifty IT #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20IT", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftyIT = pd.DataFrame.from_dict(d2).transpose()
niftyIT = niftyIT[niftyIT['priority'] == 0]
niftyIT_2 = niftyIT.drop(['priority'],axis = 1)
niftyIT_3 = niftyIT_2.drop(['meta'],axis = 1)


symbol = niftyIT_3['symbol']
per_change = niftyIT_3['pChange']
value = niftyIT_3['totalTradedValue']

fig_IT = px.treemap(niftyIT_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty IT',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_IT.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_bank, use_container_width=False)
right_column.plotly_chart(fig_IT, use_container_width=False)

# # =============================================================================
# # #### Nifty Metal #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20METAL", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftymetal = pd.DataFrame.from_dict(d2).transpose()
niftymetal = niftymetal[niftymetal['priority'] == 0]
niftymetal_2 = niftymetal.drop(['priority'],axis = 1)
niftymetal_3 = niftymetal_2.drop(['meta'],axis = 1)


symbol = niftymetal_3['symbol']
per_change = niftymetal_3['pChange']
value = niftymetal_3['totalTradedValue']

fig_metal = px.treemap(niftymetal_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty Metal',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_metal.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)


# # =============================================================================
# # #### Nifty AUTO #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20AUTO", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftyauto = pd.DataFrame.from_dict(d2).transpose()
niftyauto = niftyauto[niftyauto['priority'] == 0]
niftyauto_2 = niftyauto.drop(['priority'],axis = 1)
niftyauto_3 = niftyauto_2.drop(['meta'],axis = 1)


symbol = niftyauto_3['symbol']
per_change = niftyauto_3['pChange']
value = niftyauto_3['totalTradedValue']

fig_auto = px.treemap(niftyauto_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty Auto',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_auto.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_metal, use_container_width=False)
right_column.plotly_chart(fig_auto, use_container_width=False)




# # =============================================================================
# # #### Nifty FMCG #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FMCG", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftyfmcg = pd.DataFrame.from_dict(d2).transpose()
niftyfmcg = niftyfmcg[niftyfmcg['priority'] == 0]
niftyfmcg_2 = niftyfmcg.drop(['priority'],axis = 1)
niftyfmcg_3 = niftyfmcg_2.drop(['meta'],axis = 1)


symbol = niftyfmcg_3['symbol']
per_change = niftyfmcg_3['pChange']
value = niftyfmcg_3['totalTradedValue']

fig_fmcg = px.treemap(niftyfmcg_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty FMCG',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_fmcg.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)


# # =============================================================================
# # #### Nifty REALTY #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20REALTY", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftyrealty = pd.DataFrame.from_dict(d2).transpose()
niftyrealty = niftyrealty[niftyrealty['priority'] == 0]
niftyrealty_2 = niftyrealty.drop(['priority'],axis = 1)
niftyrealty_3 = niftyrealty_2.drop(['meta'],axis = 1)


symbol = niftyrealty_3['symbol']
per_change = niftyrealty_3['pChange']
value = niftyrealty_3['totalTradedValue']

fig_realty = px.treemap(niftyrealty_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty Realty',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_realty.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_fmcg, use_container_width=False)
right_column.plotly_chart(fig_realty, use_container_width=False)






# # =============================================================================
# # #### Nifty PHARMA #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20PHARMA", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftypharma = pd.DataFrame.from_dict(d2).transpose()
niftypharma = niftypharma[niftypharma['priority'] == 0]
niftypharma_2 = niftypharma.drop(['priority'],axis = 1)
niftypharma_3 = niftypharma_2.drop(['meta'],axis = 1)


symbol = niftypharma_3['symbol']
per_change = niftypharma_3['pChange']
value = niftypharma_3['totalTradedValue']

fig_pharma = px.treemap(niftypharma_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty PHARMA',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_pharma.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)


# # =============================================================================
# # #### Nifty Fin SERVICES #####
# # =============================================================================

response = requests.get(url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES", headers = headers )
d = response.json()
d1 = d['data']
d2 = {}
n = 0
for i in d1 :
    try:
        d2[n] = i
        n = n+1
    except:
        pass
niftyfinancial = pd.DataFrame.from_dict(d2).transpose()
niftyfinancial = niftyfinancial[niftyfinancial['priority'] == 0]
niftyfinancial_2 = niftyfinancial.drop(['priority'],axis = 1)
niftyfinancial_3 = niftyfinancial_2.drop(['meta'],axis = 1)


symbol = niftyfinancial_3['symbol']
per_change = niftyfinancial_3['pChange']
value = niftyfinancial_3['totalTradedValue']

fig_fin = px.treemap(niftyfinancial_3,
                  path = [symbol, per_change],
                  color = per_change,
                  values = value,
                  color_continuous_scale='RdYlGn',
                  title = 'Nifty Fin Services',
                  hover_name = 'pChange',
                  width=720, 
                  height=500
    )

fig_fin.update_layout(
    title_font_size = 42,
    title_font_family = 'Arial'
    )

#plot(fig_bank)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pharma, use_container_width=False)
right_column.plotly_chart(fig_fin, use_container_width=False)