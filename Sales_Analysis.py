#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ##### Merge 12 months of sales data into a single csv file 

# In[2]:


files =[file for file in os.listdir("D:\projects\sales\Sales_Data")]
for file in files:
    print(file)


# In[4]:


path = "D:\projects\sales\Sales_Data"

#blank dataframe
all_data = pd.DataFrame()

for file in files:
    current_df = pd.read_csv(path+"/"+file)
    all_data = pd.concat([all_data, current_df])
    
all_data.shape


# ##### convert it into dataset

# In[6]:


all_data.to_csv('D:\projects\sales\Sales_Data/all_data.csv',index=False)


# ##### Data cleaning and formatting

# In[7]:


all_data.dtypes


# In[8]:


all_data.head()


# In[26]:


all_data.isnull().sum()


# In[27]:


all_data = all_data.dropna(how='all')
all_data.shape


# ##### What is the best month for sale?

# In[28]:


'04/19/19 08:46'.split('/')[0]


# In[29]:


def month(x):
    return x.split('/')[0]


# ##### add month col

# In[30]:


all_data['Month']=all_data['Order Date'].apply(month)


# In[31]:


all_data.dtypes


# In[32]:


all_data['Month']=all_data['Month'].astype(int)


# In[33]:


all_data['Month'].unique()


# In[34]:


filter=all_data['Month']=='Order Date'
len(all_data[~filter])


# In[35]:


all_data=all_data[~filter]


# In[36]:


all_data.shape


# In[37]:


all_data.head()


# In[70]:


all_data['Month']=all_data['Month'].astype(int)


# In[39]:


all_data.dtypes


# In[40]:


all_data['Price Each']=all_data['Price Each'].astype(float)


# In[41]:


all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)


# In[42]:


all_data['sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head(5)


# In[43]:


all_data.groupby('Month')['sales'].sum()


# In[44]:


months=range(1,13)
plt.bar(months,all_data.groupby('Month')['sales'].sum())
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# ##### Which city has max order

# In[45]:


'917 1st St, Dallas, TX 75001'.split(',')[1]


# In[46]:


def city(x):
    return x.split(',')[1]


# In[47]:


all_data['city']=all_data['Purchase Address'].apply(city)


# In[48]:


all_data.groupby('city')['city'].count()


# In[49]:


plt.bar(all_data.groupby('city')['city'].count().index,all_data.groupby('city')['city'].count())
plt.xticks(rotation='vertical')
plt.ylabel('received orders')
plt.xlabel('city names')
plt.show()


# In[ ]:





# ##### What time should we display advertisements to maximise for product purchase?

# In[ ]:





# In[50]:


all_data['Order Date'][0].dtype


# In[69]:


all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour


# In[52]:


keys=[]
hour=[]
for key,hour_df in all_data.groupby('Hour'):
    keys.append(key)
    hour.append(len(hour_df))


# In[53]:


plt.grid()
plt.plot(keys,hour)


# ##### between 12pm and 7pm is probably the best time to advertise to maximise product purchase

# In[ ]:





# #### What product sold the most? &  Why?

# In[54]:


all_data.groupby('Product')['Quantity Ordered'].sum().plot(kind='bar')


# In[55]:


all_data.groupby('Product')['Price Each'].mean()


# In[56]:


products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
prices=all_data.groupby('Product')['Price Each'].mean()


# In[57]:


plt.figure(figsize=(40,24))
fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(products, quantity, color='g')
ax2.plot(products, prices, 'b-')
ax1.set_xticklabels(products, rotation='vertical', size=8)


# ##### The top selling product is 'AAA Batteries'. The top selling products seem to have a correlation with the price of the product. The cheaper the product higher the quantity ordered and vice versa.

# In[58]:


all_data.shape


# ##### What products are most often sold together?

# #### note: keep orders that have same order Id,are sold mostly together

# In[59]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df.head(20)


# In[60]:


#create grouped col 
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))


# In[61]:


df.head()


# In[62]:


df.shape


# In[63]:


#lets drop out all duplicate Order ID
df2 = df.drop_duplicates(subset=['Order ID'])


# In[64]:


df2['Grouped'].value_counts()[0:5].plot.pie()


# In[65]:


import plotly.graph_objs as go
from plotly.offline import iplot


# In[66]:


values=df2['Grouped'].value_counts()[0:5]
labels=df['Grouped'].value_counts()[0:5].index


# In[67]:


trace=go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value', 
               textfont=dict(size=25),
              pull=[0, 0, 0,0.2, 0]
               )


# In[68]:


iplot([trace])


# In[ ]:





# In[ ]:




