#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


#Importing the datset
df=pd.read_excel('Book1.xlsx')
df_feat=pd.read_csv('active_features.csv')
df_pro_mum=pd.read_excel("procurement_mumbai.xlsx")
df_pro_del=pd.read_excel('procurement_delhi.xlsx')
df_pro_ban=pd.read_excel('procurement_bangalore.xlsx')


# In[ ]:


#Filling missing values and changing dtype to int
df_pro_mum['Website Listing Id']=df_pro_mum['Website Listing Id'].fillna(0)
df_pro_del['Website Listing Id']=df_pro_del['Website Listing Id'].fillna(0)
df_pro_ban['Website Listing Id']=df_pro_ban['Website Listing Id'].fillna(0)
df_pro_mum['Website Listing Id']=df_pro_mum['Website Listing Id'].apply(np.int)
df_pro_del['Website Listing Id']=df_pro_del['Website Listing Id'].apply(np.int)
df_pro_ban['Website Listing Id']=df_pro_ban['Website Listing Id'].apply(np.int)


# In[ ]:


df_variants=pd.read_csv('makes_inventory1.csv')
df_market_variants=pd.read_csv('marketplace_everything.csv')
df_variants['policy_validity']=df_variants['policy_validity'].fillna('0000-00-00')
df_market_variants['policy_validity']=df_market_variants['policy_validity'].fillna('0000-00-00')


# In[ ]:


colu=['policy_type', 'fuel_type_id_primary']
column1=['fuel_type_id_primary', 'fuel_type_id_secondary']
df_variants[colu]=df_variants[colu].apply(lambda x: x.astype(str).str.lower())
df_market_variants[column1]=df_market_variants[column1].apply(lambda x: x.astype(str).str.lower())


# In[ ]:


#Replacing '-' with blank_space
df_variants['registration_date'] = [x.replace('-', ' ') for x in df_variants['registration_date']]
df_market_variants['registration_date'] = [x.replace('-', ' ') for x in df_market_variants['registration_date']]
df_variants['policy_validity'] = [x.replace('-', ' ') for x in df_variants['policy_validity']]
df_market_variants['policy_validity'] = [x.replace('-', ' ') for x in df_market_variants['policy_validity']]


# In[ ]:


def year(reg_date): 
#     from datetime import datetime, date
#     d0 = datetime.strptime(reg_date, "%Y %m %d")
#     d1 = datetime.today()
#     delta = d1 - d0
#     return delta
    from datetime import datetime, date
    d2 = datetime.strptime(reg_date, "%Y %m %d")
    d1 = datetime.today()
    diff=d1.year-d2.year
#     difference = relativedelta.relativedelta(d1, d2)
#     years = difference.years
    return diff


# In[ ]:


def month(policy_date):  
    from datetime import datetime, date
    d2 = datetime.strptime(policy_date, "%Y %m %d")
    d3 = datetime.today()
    delta = d2.month - d3.month + 12*(d2.year - d3.year)
    return delta 


# In[ ]:


model1=[]
for h in range(len(df_variants['registration_date'])):
    reg_date=df_variants['registration_date'][h]
    him=year(reg_date)
    model1.append(him)
df_variants['age']=pd.DataFrame(model1)


# In[ ]:


model2=[]
for h in range(len(df_market_variants['registration_date'])):
    reg_date=df_market_variants['registration_date'][h]
    him=year(reg_date)
    model2.append(him)
df_market_variants['age']=pd.DataFrame(model2)


# # Processing(Giving ratings)

# In[ ]:


#Age_Gradient
## 57% ratings are higher than 4.0 and around 25% ratings are more than 4.5
##Truebil_Direct
model1=np.asarray(model1)
model1=np.interp(model1, (2, 10), (5, 3))
for i in range(len(df_variants['age'])):
    if df_variants['age'][i] == 0 or df_variants['age'][i]==1 or df_variants['age'][i]==2:
        df_variants['age_grad']=5
    if df_variants['age'][i] >10:
        df_variants['age_grad'][i]=3
df_variants['age_grad']=pd.DataFrame(model1)
df_variants['age_grad']=round(df_variants['age_grad'], 1)
##Market_Place
model2=np.asarray(model2)
model2=np.interp(model2, (2, 10), (5, 3))
for i in range(len(df_market_variants['age'])):
    if df_market_variants['age'][i] == 0 or df_market_variants['age'][i]==1 or df_market_variants['age'][i]==2:
        df_market_variants['age_grad']=5
    if df_market_variants['age'][i] > 10:
        df_market_variants['age_grad'][i]=3
df_market_variants['age_grad']=pd.DataFrame(model2)
df_market_variants['age_grad']=round(df_market_variants['age_grad'], 1)


# In[ ]:


#Mileage/age gradient
##Truebil_Direct
df_variants['mileage/age']=df_variants['mileage']/df_variants['age']
df_variants['mil/age_grad']=np.asarray(list(df_variants['mileage/age']))
df_variants['mil/age_grad']=np.interp(df_variants['mil/age_grad'], (df_variants['mil/age_grad'].min(), df_variants['mil/age_grad'].max()), (5, 3))
df_variants['mil/age_grad']=pd.DataFrame(df_variants['mil/age_grad'])
df_variants['mil/age_grad']=round(df_variants['mil/age_grad'], 1)
##Market_Place
for i in range(len(df_market_variants['age'])):
    if df_market_variants['age'][i] == 0:
        df_market_variants['age'][i]=1


# In[ ]:


df_market_variants


# In[ ]:


df_market_variants['mileage/age']=df_market_variants['mileage']/df_market_variants['age']
df_market_variants['mil/age_grad']=np.asarray(list(df_market_variants['mileage/age']))
df_market_variants['mil/age_grad']=np.interp(df_market_variants['mil/age_grad'], (df_market_variants['mil/age_grad'].min(), df_market_variants['mil/age_grad'].max()), (5, 3))
df_market_variants['mil/age_grad']=pd.DataFrame(df_market_variants['mil/age_grad'])
df_market_variants['mil/age_grad']=round(df_market_variants['mil/age_grad'], 1)


# In[ ]:


#Number_of_owners
df_variants['owners_rating'] = df_variants['owners'].map({1: 5, 2:4.5, 3 : 4.0})


# In[ ]:


#Inspection_Rating
df_variants['inspection_rating_upd']=round(df_variants['inspection_rating'], 1)


# In[ ]:


#Mileage_Gradient
df_variants['mil_grad']=np.asarray(list(df_variants['mileage']))
df_variants['mil_grad']=np.interp(df_variants['mil_grad'], (df_variants['mil_grad'].min(), df_variants['mil_grad'].max()), (5, 3))
df_variants['mil_grad']=pd.DataFrame(df_variants['mil_grad'])
df_variants['mil_grad']=round(df_variants['mil_grad'], 1)


# In[ ]:


#Fuel_Type
df_variants['fuel_rating'] = df_variants['fuel_type'].map({'petrol': 4.8, 'diesel':5.0})


# In[ ]:


#Insurance_Type_Grad
## making a new column of left months till policy validity from today
list1=[]
for i in range(len(df_variants['insurance_type'])):
    policy_date=df_variants['policy_validity'][i]
    if df_variants['insurance_type'][i] == 'lapsed':
        tmp= 0
        list1.append(tmp)
    else:
        tmp=month(policy_date)
        list1.append(tmp)
df_variants['policy_age']=pd.DataFrame(list1)

##################################
##Calculating_ratings
list2=[]
for i in range(237):
    pol_val=df_variants['policy_age'][i]
    if df_variants['insurance_type'][i] == 'lapsed':
        temp= 3.5
        list2.append(temp)
    if df_variants['insurance_type'][i]=='comprehensive':
        temp=5+0.05*(pol_val)
        round(temp, 1)
        list2.append(temp)
    if df_variants['insurance_type'][i]=='0 depreciation':
        temp=4.5+0.05*(pol_val)
        round(temp, 1)
        list2.append(temp)
    if df_variants['insurance_type'][i]=='third party':
        temp=3.5+0.1*(pol_val)
        round(temp, 1)
        list2.append(temp)
df_variants['policy_grad']=pd.DataFrame(list2)

######################################
##Capping the over-range values to desired range
for i in range(237):        
    if df_variants['insurance_type'][i]=='third party' and df_variants['policy_grad'][i]>=4.5:
        df_variants['policy_grad'][i]=4.5
    if df_variants['insurance_type'][i]=='comprehensive' and df_variants['policy_grad'][i]>=5.0:
        df_variants['policy_grad'][i]=5.0
    if df_variants['insurance_type'][i]=='0 depriciation' and df_variants['policy_grad'][i]>=5.0:
        df_variants['policy_grad'][i]=5.0
    else:
        df_variants['policy_grad'][i]


# In[ ]:


##Price_Procurement_Mumbai'
# df_variants['cp']=np.zeros_like(0, dtype=float)
# df_variants['procure']=np.zeros_like(0, dtype=float)
# df_variants['esp']=np.zeros_like(0, dtype=float)
df_variants['cp']=np.nan
df_variants['procure']=np.nan
df_variants['esp']=np.nan
for i in range(len(df_pro_mum['Website Listing Id'])):
    for j in range(len(df_variants['id'])):
        if df_pro_mum['Website Listing Id'][i]==df_variants['id'][j] and (df_pro_mum['Status'][i]=='Live' or df_pro_mum['Backend Status'][i]=='active'):
            df_variants['cp'][j]=df_pro_mum['Total CP'][i]
            df_variants['esp'][j]=df_pro_mum['ESP'][i]
            df_variants['procure'][j]=df_pro_mum['Procurement price'][i]    


# In[ ]:


#price_procurement_delhi
for i in range(len(df_pro_del['Website Listing Id'])):
    for j in range(len(df_variants['id'])):
        if df_pro_del['Website Listing Id'][i]==df_variants['id'][j] and (df_pro_del['Status'][i]=='Live' or df_pro_del['Backend Status'][i]=='active'):
            df_variants['cp'][j]=df_pro_del['Total CP'][i]
            df_variants['esp'][j]=df_pro_del['ESP'][i]
            df_variants['procure'][j]=df_pro_del['Procurement Price'][i]


# In[ ]:


#price_procurement_bangalore
for i in range(len(df_pro_ban['Website Listing Id'])):
    for j in range(len(df_variants['id'])):
        if df_pro_ban['Website Listing Id'][i]==df_variants['id'][j] and (df_pro_ban['Status'][i]=='Live' or df_pro_ban['Backend Status'][i]=='active'):
            df_variants['cp'][j]=df_pro_ban['Total CP'][i]
            df_variants['esp'][j]=df_pro_ban['ESP'][i]
            df_variants['procure'][j]=df_pro_ban['Procurement price'][i]  


# In[ ]:


#price_grad
df_variants=df_variants.dropna()
df_variants=df_variants.reset_index(drop=True)
df_variants['procure_price']=(df_variants['esp']-df_variants['cp'])/df_variants['esp']
df_variants['price_grad']=np.asarray(list(df_variants['procure_price']))
df_variants['price_grad']=np.interp(df_variants['price_grad'], (df_variants['price_grad'].min(), df_variants['price_grad'].max()), (3, 5))
df_variants['price_grad']=pd.DataFrame(df_variants['price_grad'])
df_variants['price_grad']=round(df_variants['price_grad'], 1)


# In[ ]:


#Colour_Gradient
df_variants['colour_grad']=np.nan
for i in range(len(df_variants['colour'])):
    if df_variants['colour'][i]=='white' or df_variants['colour'][i]=='silver' or df_variants['colour'][i]=='grey':
        df_variants['colour_grad'][i] = 5
    if df_variants['colour'][i]=='black' or df_variants['colour'][i]=='others':
        df_variants['colour_grad'][i] = 4.5
    else:
        df_variants['colour_grad'][i] = 4.0


# In[ ]:


##Price and ORP
df_variants['selling_orp']=(df_variants['orp'] - df_variants['procure'])/df_variants['orp']


# In[ ]:


arr=[]
li = []
mx = len(df_feat['listing_id'])-1
for i in range(len(df_feat['listing_id'])):
    li.append(df_feat['name'].iloc[i])
    if(i<mx and (df_feat['listing_id'][i] != df_feat['listing_id'][i+1])):
        dict1 = {
            'listing_id' : df_feat['listing_id'][i],
            'features' : li
        }
        arr.append(dict1)
        li = []


# In[ ]:


df_feat


# In[ ]:


sns.distplot(df_feat[df_feat['name']=='Airbags']['listing_id'])


# In[ ]:


df_variants['features']=np.nan


# In[ ]:


df1=pd.DataFrame(arr)


# In[ ]:


#Merging the two datasets
for i in range(len(df1['listing_id'])):
    for j in range(len(df_variants['id'])):
        if df1['listing_id'][i] == df_variants['id'][j]:
#             print(df1['features'][i])
            
            df_variants['features'][j]=df1['features'][i]
#             print(df_variants['features'][j][0])


# In[ ]:





# In[ ]:


df_variants=df_variants.dropna()
df_variants=df_variants.reset_index(drop=True)


# In[ ]:


df_variants['safety']=np.zeros_like(0, dtype=float)
df_variants['comfort']=np.zeros_like(0, dtype=float)


# In[ ]:


dict1={}
dict1={
    'Central locking' : 0.075,
    'ABS' : 0.30,
    'Airbags' : 0.30,
    'Rear parking sensor' : 0.075,
    'Seat belt warning' : 0.033,
    'Rear camera' : .075,
    'Anti-theft alarm' : 0.075,
    'Door ajar warning' : 0.033,
    'Child safety locks' : 0.034
}


# In[ ]:


dict2={
    'Power windows' : 0.1,
'Power steering' : 0.1,
'Air Conditioner': 0.1,
"Keyless start": 0.1,
'Audio controls on steering': 0.1,
'Remote trunk opener': 0.1,
'Remote fuel lid opener': 0.1,
'Rear AC vent': 0.1,
'Rear wiper': 0.1,
'Power Folding ORVM': 0.1,
'Cruise Control': 0.1,
'Sun Roof': 0.1,
'Tilt steering': 0.1,
'Rear Defogger': 0.1,
'Power Window Front': 0.1,
'Power Window Back': 0.1,
'Automatic Adjustable seats': 0.1,
}


# In[ ]:


count=0
for i in df_variants['features']:
    for j in i:
        try:
            df_variants['safety'][count]=dict1[j]+df_variants['safety'][count]
        except KeyError:
            pass
    count=count+1


# In[ ]:


count1=0
for i in df_variants['features']:
    for j in i:
        try:
            df_variants['comfort'][count1]=dict2[j]+df_variants['comfort'][count1]
        except KeyError:
            pass
    count1=count1+1


# In[ ]:


#Features_Rating
##Safety
df_variants['safety_grad']=np.asarray(list(df_variants['safety']))
df_variants['safety_grad']=np.interp(df_variants['safety_grad'], (df_variants['safety_grad'].min(), df_variants['safety_grad'].max()), (2.5, 5))
df_variants['safety_grad']=pd.DataFrame(df_variants['safety_grad'])
df_variants['safety_grad']=round(df_variants['safety_grad'], 1)
##Comfort
df_variants['comfort_grad']=np.asarray(list(df_variants['comfort']))
df_variants['comfort_grad']=np.interp(df_variants['comfort_grad'], (df_variants['comfort_grad'].min(), df_variants['comfort_grad'].max()), (2.5, 5))
df_variants['comfort_grad']=pd.DataFrame(df_variants['comfort_grad'])
df_variants['comfort_grad']=round(df_variants['comfort_grad'], 1)


# In[ ]:


df_variants


# In[ ]:


df_variants['age']


# In[ ]:


count = 0
for i in df_variants['policy_grad'] : 
    if i==5: 
        count = count + 1
print (count)


# # Testing 

# In[ ]:


n2=sns.distplot(df_variants['mil/age_grad']


# In[ ]:


n3=sns.distplot(df_variants['inspection_rating'])


# In[ ]:


n3=sns.distplot(df_variants['price'])


# In[ ]:


list1=[]
for i in list(df_variants['inspection_rating']):
    if i >4.3:
        list1.append(i)
len(list1)


# In[ ]:


for i in range(len(arr)):
    if df_variants['colour'][i] =='17':
        print ('haai')


# In[ ]:


for i in df_variants['features']:
    if 'Central locking' in i:
        print (i)


# # Old_Price_Calculation_Direct_Cars

# In[ ]:


df_dp_initial=pd.read_csv('price_dp_initial.csv')


# In[ ]:


df_dy=pd.read_csv('price_dynamic_price.csv')
df_sheet=pd.read_csv('price_sheet.csv')
df_cron=pd.read_csv('price_cron.csv')


# In[ ]:


df_dy['dp_initial']=np.nan
for i in range(len(df_dp_initial['id'])):
    for j in range(len(df_dy['id'])):
        if df_dp_initial['id'][i] == df_dy['id'][j]:            
            df_dy['dp_initial'][j]=df_dp_initial['updated_price'][i]


# In[ ]:


for i in range(len(df_cron['id'])):
    for j in range(len(df_dy['id'])):
        if df_cron['id'][i] == df_dy['id'][j]:            
            df_dy['dp_initial'][j]=df_cron['updated_price'][i]


# In[ ]:


for i in range(len(df_sheet['id'])):
    for j in range(len(df_dy['id'])):
        if df_sheet['id'][i] == df_dy['id'][j]:            
            df_dy['dp_initial'][j]=df_sheet['updated_price'][i]


# In[ ]:


df_variants=df_dy
df_variants['policy_validity']=df_variants['policy_validity'].fillna('0000-00-00')


# In[ ]:


df_dy.isnull().sum()


# In[ ]:


df_dy['policy_validity']=df_dy['policy_validity'].fillna('0000-00-00')


# In[ ]:


df_dy=df_dy.dropna()
df_dy=df_dy.reset_index(drop=True)


# In[ ]:


df_variants['dp_initial']=df_variants['dp_initial'].fillna(0)


# In[ ]:


df_dy1=df_dy


# In[ ]:


#price_old_grad
df_dy1['x']=np.zeros_like(0, dtype=float)
for i in range(len(df_dy1['dp_initial'])):
    if df_dy1['dp_initial'][i]==0:
        df_dy1['x'][i]=0
    if df_dy1['dp_initial'][i] != 0.0:
        df_dy1['x'][i]=(df_dy1['dp_initial'][i]-df_dy1['updated_price'][i])/df_dy1['dp_initial'][i]


# In[ ]:


for i in range(len(df_dy1['x'])):
    if df_dy1['x'][i]>0.00 and df_dy1['x'][i]<0.15:
        df_dy1['x'][i]=0.1
    if df_dy1['x'][i]>=.15 and df_dy1['x'][i]<=0.2:
        df_dy1['x'][i]=0.2


# In[ ]:


df_dy1['x'].max()


# In[ ]:


#delta(x)
df_dy1['delta_x'] = 6.48*df_dy1['x']**3+11.75*df_dy1['x']**2+0.5*df_dy1['x']
df_dy1['old_price']=5+df_dy1['delta_x']


# In[ ]:


df_dy1['old_price_grad']=np.asarray(list(df_dy1['old_price']))
df_dy1['old_price_grad']=np.interp(df_dy1['old_price_grad'], (df_dy1['old_price_grad'].min(), df_dy1['old_price_grad'].max()), (3, 5))
df_dy1['old_price_grad']=pd.DataFrame(df_dy1['old_price_grad'])
df_dy1['old_price_grad']=round(df_dy1['old_price_grad'], 1)


# In[ ]:


n3=sns.distplot(df_dy1['old_price'])


# In[ ]:


df_dy1['delta_x'].min()


# In[ ]:


count = 0
for i in range(len(df_variants['age_grad'])): 
    if df_variants['age_grad'][i]==5.0: 
        count = count + 1
print (count)
# print (df_variants['age_grad'][i])


# In[ ]:


for i in range(len(df_variants['age_grad'])):
    if df_variants['age_grad'][i]==.0:
        print (df_variants['registration_date'][i], df_variants['age_grad'][i])


# In[ ]:


df_variants['age_grad'].max()


# In[ ]:


count = 0
for i in df_variants['selling_orp']: 
    if i<=0.0: 
        count = count + 1
print (count)


# # Price_Marketplace

# In[ ]:


df_market=pd.read_csv('market_price.csv')


# In[ ]:


#price_old_grad
df_market['x']=np.zeros_like(0, dtype=float)
for i in range(len(df_market['carwale_price'])):
#     if df_market['carwale_price'][i]==0:
#         df_market['x'][i]=0
#     if df_market['carwale_price'][i] != 0.0:
    df_market['x'][i]=(df_market['price'][i]-df_market['carwale_price'][i])/df_market['carwale_price'][i]


# In[ ]:


for i in range(len(df_market['x'])):
    if df_market['x'][i]>=0.00 and df_market['x'][i]<=0.10:
        df_market['x'][i]=0.1
    if df_market['x'][i]>.10 and df_market['x'][i]<=0.2:
        df_market['x'][i]=0.2
    if df_market['x'][i]>.2 and df_market['x'][i]<=0.3:
        df_market['x'][i]=0.3
    if df_market['x'][i]>.4 and df_market['x'][i]<=0.5:
        df_market['x'][i]=0.4
    else:
        df_market['x'][i]=0.6


# In[ ]:


count = 0
for i in df_market['x']: 
    if i<0:
        count = count + 1
print (count)


# In[ ]:


df_market['delta_x'] = 6.48*df_market['x']**3+11.75*df_market['x']**2+0.5*df_market['x']
for i in range(len(df_market['delta_x'])):
    if df_market['delta_x'][i]>=2.0:
        df_market['delta_x'][i]=2.0
    


# In[ ]:


df_market['market_price_rating']=5-df_market['delta_x']


# In[ ]:


for i in range(len(df_market['market_price_rating'])):
    if df_market['x'][i]==4.0:
        print (df_market['carwale_price'][i], df_market['price'][i], df_market['id'][i])


# In[ ]:


df_market['delta_x'].max()


# In[ ]:


##OR
df_market=pd.read_csv('market_price.csv')

df_market['x']=np.zeros_like(0, dtype=float)
for i in range(len(df_market['carwale_price'])):
    df_market['x'][i]=(df_market['price'][i]-df_market['carwale_price'][i])/df_market['carwale_price'][i]

for i in range(len(df_market['x'])):
    if df_market['x'][i]<0:
        df_market['x'][i]=0
    if df_market['x'][i]>0.5:
        df_market['x'][i]=0.5

df_market['del_x']=np.zeros_like(0, dtype=float)
for i in range(len(df_market['x'])):
    x = df_market['x'][i]
    df_market['del_x'][i]=eqn2(x)

def eqn9(x):
     '''
    0 =   5
    0.05  =  4.9
    0.1  =  4.8
    0.15  =  4.4
    0.2  =  4
    0.25  =  3.5
    0.3  =  3
    0.35  =  2.4
    0.4  =  1.8
    0.45  =  1.4
    0.5  =  1
    '''
    y = 0.007-0.21*x+28*x**2-4.66*x**3-37.3*x**4
    return 5-y


# In[ ]:


sns.distplot(df_market['delta_x'])


# # Market_Inspection

# In[ ]:


df_market_ins=pd.read_csv('bangalore_mp.csv')


# In[ ]:


df_market_ins['registration_date'] = [x.replace('-', ' ') for x in df_market_ins['registration_date']]


# In[ ]:


def date2(reg_date):
    from datetime import datetime, date
    d0 = datetime.strptime(reg_date, "%Y %m %d")
    d1 = datetime.today()
    delta = d1.year - d0.year
    return delta


# In[ ]:


model2=[]
for h in range(len(df_market_ins['registration_date'])):
    reg_date=df_market_ins['registration_date'][h]
    him=date2(reg_date)
    model2.append(him)
df_market_ins['age']=pd.DataFrame(model2)


# In[ ]:


for i in range(len(df_market_ins['age'])):
    if df_market_ins['age'][i] ==0:
        df_market_ins['age'][i]=1


# In[ ]:


df_market_ins['mil/age']=df_market_ins['mileage']/df_market_ins['age']


# In[ ]:


count = 0
for i in df_market_ins[df_market_ins['fuel_type_id_primary']=='Diesel']['mil/age']: 
    if i >0 :
        count = count + 1
print (count)


# In[ ]:


df_market_ins[['age', 'registration_date']].shape


# In[ ]:


sns.distplot(df_market_ins1[df_market_ins1['fuel_type_id_primary']=='Petrol']['mil/age'])


# In[ ]:


sns.distplot(df_market_ins1[df_market_ins1['fuel_type_id_primary']=='Diesel']['mil/age'])


# In[ ]:


df_market_ins1=df_market_ins[df_market_ins['mil/age']<25000]


# In[ ]:


count = 0
for i in df_market_ins1[df_market_ins1['fuel_type_id_primary']=='Diesel']['mil/age']: 
    if i >=9000 and i<=10000:
        count = count + 1
print (count)


# In[ ]:


df_market_ins1[df_market_ins1['fuel_type_id_primary']=='Diesel']['mil/age'].mean(axis=0)


# In[ ]:


86/815


# In[ ]:


''' For market place cars
For Petrol - 802
5k - 6k = 88 (11%)
**6k - 7k = 110 (13%)**
7k - 8k = 82 (10%)
8k - 9k = 74
9k - 10k = 54

For Diesel - 815
8k - 9k = 75
**9k - 10k = 86 (10%)**
10k - 11k = 82 (9%)
11k - 12k = 65
'''


# In[ ]:


'''
For Petrol Cars - 802
**20 - 25 = 145 (18%)**
25 - 30 = 104 (13%)
30 - 35 = 58 (7%)
35 - 40 = 27 
40 - 45 = 11

0 - 10 = 104 (13%)
10 - 20 = 321 (40%)
20 - 30 = 249 (31%)
30 - 40 = 85
40 - 50 = 20

For Diesel Cars - 815
20 - 25 = 131 (16%)
**25 - 30 = 156 (19%) **
30 - 35 = 126 (15%)
35 - 40 = 88
40 - 45 = 53

10 - 20 = 130 (16%)
20 - 30 = 287 (35%)
30 - 40 = 214 (30%)
40 - 50 = 93
'''


# # Correlation Matrix

# In[ ]:


column_test= ['age_grad', 'mil/age_grad', 'owners_rating', 'inspection_rating_upd', 'mil_grad', 
          'fuel_rating', 'policy_grad', 'colour_grad', 'price_grad', 'safety_grad', 'comfort_grad']
df_test=df_variants[column_test]


# # Basic and Advance features

# In[ ]:


df_feat_one=pd.read_csv('features_one.csv')
df_feat_zero=pd.read_csv('features_zero.csv')


# In[ ]:


count=0
for i in df_feat['name']:
    if i =='Rear Defogger':
        count=count+1
print(count)


# In[ ]:


'''Features
Out of 3690 Truebil Direct entries
Central locking = 305 (8.2%)
ABS = 145 (4%)
Airbags = 143 (4%)
Rear parking sensor = 155 (4%)
Seat belt warning = 225 (7%)
Rear camera = 78 (2%)
Anti-theft alarm = 140 (3.7%)
Door ajar warning = 239 (6.5%)
Child safety locks = 317 (8.5%)

Power steering = 319 (8.5%)
Air Conditioner =  323 (8.5%)
Keyless start = 36 (1%)
Audio controls on steering = 129 (3.4%)
Remote trunk opener = 0
Remote fuel lid opener = 0
Rear AC vent = 75 (2%)
Rear wiper = 74 (2%)
Power Folding ORVM = 80 (2.1%)
Cruise Control = 12 (.3%)
Sun Roof = 3 (0.1%)
Tilt steering = 213 (6%)
Rear Defogger = 140 (4%)
Power Window Front = 305 (8%)
Power Window Back = 222 (7%)
Automatic Adjustable seats = 12 (0.3%)
'''


# In[ ]:


'''Features
Out of 21954 MarketPlace Cars:
Central locking = 1500 (6.8%)
ABS = 1044 (4.7%)
Airbags = 1016 (4.5%)
Rear parking sensor = 985 (4.4%)
Seat belt warning = 1279 (6%)
Rear camera = 629 (3%)
Anti-theft alarm = 692 (3%)
Door ajar warning = 1371 (6.2%)
Child safety locks = 1549 (7%)

Power steering = 1544 (7%)
Air Conditioner =  1581 (7%)
Keyless start = 316 (1.5%)
Audio controls on steering = 902 (4%)
Remote trunk opener = 0
Remote fuel lid opener = 0
Rear AC vent = 604 (3%)
Rear wiper = 522 (2.3%)
Power Folding ORVM = 603 (3%)
Cruise Control = 249 (1%)
Sun Roof = 161 (0.7%)
Tilt steering = 1257 (6%)
Rear Defogger = 1061 (5%)
Power Window Front = 1501 (7%)
Power Window Back = 1354 (6%)
Automatic Adjustable seats = 234 (1%)
'''


# # New_Polynomial_Equation

# In[ ]:


from scipy.interpolate import *


# In[ ]:


p4=polyint(df_market['price'], df_market['carwale_price'], 4)


# In[ ]:


import operator

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

# x = df_market[['price', 'carwale_price']]
y = df_market['carwale_price']
polynomial_features= PolynomialFeatures(degree=2)
x_poly = polynomial_features.fit_transform(x)

# model = LinearRegression()
# model.fit(x_poly, y)
# y_poly_pred = model.predict(x_poly)

# rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
# r2 = r2_score(y,y_poly_pred)
# print(rmse)
# print(r2)

plt.scatter(x, y, s=10)
# sort the values of x before line plot
sort_axis = operator.itemgetter(0)
sorted_zip = sorted(zip(x,y_poly_pred), key=sort_axis)
x, y_poly_pred = zip(*sorted_zip)
plt.plot(x, y_poly_pred, color='m')
plt.show()


# In[ ]:


x.shape, y.shape


# In[ ]:


colu=['price']
x = df_market[colu]
y = df_market['carwale_price']


# In[ ]:


count=0
for i in df_market1['carwale_price']:
    if i >=3500000:
        count=count+1
print(count)


# In[ ]:


for i in range(len(df_market['carwale_price'])):
    if df_market['carwale_price'][i] >=3500000:
        df_market.drop(df_market['carwale_price'][i], axis=0)


# In[ ]:


df_market1=df_market[df_market['carwale_price']<3500000]


# In[ ]:


df_market1=df_market[df_market['price']<3500000]


# In[ ]:


df_market1.plot(x='carwale_price', y='price')


# In[ ]:


import matplotlib.pyplot as plt
plt.scatter(df_market1['carwale_price'], df_market1['price'])
plt.show()


# In[ ]:


df_test


# In[ ]:


def plot_corr(df_test,size=15):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df_test: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df_test.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);


# In[ ]:


plot_corr(df_test)


# In[ ]:


size=10
rs = np.random.RandomState(0)
df_test = pd.DataFrame(rs.rand(12, 12))
corr = df_test.corr()
corr.style.background_gradient(cmap='coolwarm')
# 'RdBu_r' & 'BrBG' are other good diverging colormaps


# In[ ]:


n3=sns.distplot(df_variants['pr'])


# In[ ]:


df_test.dtypes


# In[ ]:


sns.pairplot(df_test)
pd.scatter_matrix(df_test, alpha = 0.3, figsize = (14,8), diagonal = 'kde')
f, ax = pl.subplots(figsize=(10, 8))
corr = df_test.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True), square=True, ax=ax)


# In[ ]:


#create numeric plots
num = [f for f in df_test.columns if df_test.dtypes[f] != 'object']
nd = pd.melt(df_test, value_vars = num)
n1 = sns.FacetGrid (nd, col='variable', col_wrap=4, sharex=False, sharey = False)
n1 = n1.map(sns.distplot, 'value')
n1


# In[ ]:


from string import ascii_letters
sns.set(style="white")

# Generate a large random dataset
rs = np.random.RandomState(33)
# d = pd.DataFrame(data=rs.normal(size=(100, 26)),
#                  columns=list(ascii_letters[26:]))

# Compute the correlation matrix
corr = df_test.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[ ]:


plt.figure(figsize=(10,9))
sns.heatmap(df_test.corr())


# In[ ]:


df_feat


# # Check

# In[ ]:


for i in range(len(df_variants['year'])):
    if df_variants['registration_date'][i]<0:
        print (df_variants['procure'][i], df_variants['orp'][i], df_variants['id'][i])


# In[ ]:


df_variants['selling_orp'].min()


# In[ ]:


count = 0
for i in df_variants['age']: 
    if i==12:
        count = count + 1
print (count)


# In[ ]:


df_variants


# In[ ]:


plt.
plt.plot(df_variants['age'], df_variants['age_grad'])


# In[ ]:


colu=['age_grad', 'age', 'registration_date']


# In[ ]:


df_variants[colu]


# In[ ]:





# In[ ]:


df_variants.columns


# In[ ]:


df_market.shape


# In[ ]:


sns.distplot(df_variants['mileage/age'])


# In[ ]:


df_variants.shape


# In[ ]:





# In[ ]:


count = 0
for i in df_variants[df_variants['fuel_type']=='diesel']['mileage/age']: 
    if i>=10500 and i<=11000:
        count = count + 1
print (count)


# In[ ]:


##Direct
'''For petrol: 139
8k - 8.5k = 5
8.5k - 9k = 8
9k - 9.5k = 6
9.5k - 10k = 11
10k - 10.5k = 3
**8.5k - 9.5k = 14**

For Diesel - 37
8k - 9k = 1
9k - 10k = 6
*9.5k - 10.5k = 7*
10k - 11k = 6
11k - 12k = 1
11k - 12k = 1

'''


# In[ ]:


sns.distplot(df_variants[df_variants['fuel_type']=='petrol']['mileage/age'])


# In[ ]:


sns.distplot(df_variants[df_variants['age_grad']])


# In[ ]:


sns.distplot(df_variants['inspection_rating'])


# In[ ]:


df_variants.shape


# In[ ]:




