import requests
import subprocess

import pandas as pd
import numpy as np
import os
import json

import mysql.connector as sql
import sqlalchemy
from sqlalchemy import create_engine
import pymysql

import streamlit as st
import plotly.express as px
from PIL import Image
from git.repo.base import Repo

#Mysql Connection
mydb = sql.connect(
    host="127.0.0.1",
    user="root",
    password="Surya#1234")

mycursor = mydb.cursor()

mycursor.execute("USE phonepe_pulse")

#streamlit
icon = Image.open("C:/Users/THEBEST/Desktop/icon.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon = icon,
                   layout='wide')

#heading
st.header('Phonepe Pulse Data Visualization')
st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

#options
option = st.radio('Select any of the option for respective data visualization',('India Transaction Data','India User Data','State wise Transaction Data','State wise User Data','Top 10 Transaction','Top 10 User'))

if option == 'India Transaction Data':

        col1, col2, col3 = st.columns(3)
        with col1:
            
            trans_year_ind = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='trans_year_ind')
        with col2:
            trans_quarter_ind = st.selectbox('Quarter', ('1','2','3','4'),key='trans_quarter_ind')
        with col3:
            trans_type_ind= st.selectbox('Transaction Type', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='trans_type_ind')
            
        # Transaction Analysis bar chart query
        mycursor.execute(f"SELECT State, Transaction_amount FROM agg_trans WHERE Year = '{trans_year_ind}' AND Quarter = '{trans_quarter_ind}' AND Transaction_type = '{trans_type_ind}';")
        trans_res_ind = mycursor.fetchall()
        trans_res_ind_df = pd.DataFrame(np.array(trans_res_ind ), columns=['State', 'Transaction_amount'])
        trans_res2_ind_df = trans_res_ind_df.set_index(pd.Index(range(1, len(trans_res_ind_df)+1)))
        
        # Transaction Analysis table query
        mycursor.execute(f"SELECT State, Transaction_count, Transaction_amount FROM agg_trans WHERE Year = '{trans_year_ind}' AND Quarter = '{trans_quarter_ind}' AND Transaction_type = '{trans_type_ind}';")
        trans_res_ana_ind = mycursor.fetchall()
        trans_res_ana_ind_df = pd.DataFrame(np.array(trans_res_ana_ind), columns=['State','Transaction_count','Transaction_amount'])
        trans_res2_ana_ind_df = trans_res_ana_ind_df.set_index(pd.Index(range(1, len(trans_res_ana_ind_df)+1)))
        
        # Total Transaction Amount table query
        mycursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM agg_trans WHERE Year = '{trans_year_ind}' AND Quarter = '{trans_quarter_ind}' AND Transaction_type = '{trans_type_ind}';")
        trans_res_amount_ind = mycursor.fetchall()
        trans_res_amount_ind_df = pd.DataFrame(np.array(trans_res_amount_ind), columns=['Total','Average'])
        trans_res2_amount_ind_df = trans_res_amount_ind_df.set_index(['Average'])
        
        # Total Transaction Count table query
        mycursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM agg_trans WHERE Year = '{trans_year_ind}' AND Quarter = '{trans_quarter_ind}' AND Transaction_type = '{trans_type_ind}';")
        trans_res_count_ind= mycursor.fetchall()
        trans_res_count_ind_df = pd.DataFrame(np.array(trans_res_count_ind), columns=['Total','Average'])
        trans_res_count2_ind = trans_res_count_ind_df.set_index(['Average'])
        
        #visualization for Transaction
        # Drop a State column 
        trans_res_ind_df.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        # Create a DataFrame with the state names column
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        # Combine the Gio State name 
        df_state_names_tra['Transaction_amount']=trans_res_ind_df
        # convert dataframe to csv file
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        # Read csv
        df_tra = pd.read_csv('State_trans.csv')
        
        # Geo plot
        fig_tra = px.choropleth(
            df_tra,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='Edge',title = 'Transaction Analysis')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), height=800)
        st.plotly_chart(fig_tra,use_container_width=True)

        # All India Transaction Analysis Bar chart
        trans_res2_ind_df['State'] = trans_res2_ind_df['State'].astype(str)
        trans_res2_ind_df['Transaction_amount'] = trans_res2_ind_df['Transaction_amount'].astype(float)
        trans_res2_ind_df_fig= px.bar(trans_res2_ind_df , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'Magenta', title = 'Transaction Analysis Chart', height = 700,)
        trans_res2_ind_df_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(trans_res2_ind_df_fig,use_container_width=True)
        st.info('**:blue[Each state is represented by a different color in the India map. This visualization helps you compare the total transaction amounts across different states, allowing you to identify states with higher or lower transaction volumes]**')


        # All India Total Transaction calculation Table
        st.header('Total calculation')      
        col4, col5 = st.columns(2)        
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(trans_res2_ana_ind_df)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(trans_res2_amount_ind_df)
            st.subheader('Transaction Count')
            st.dataframe(trans_res_count2_ind)
            
elif option == 'India User Data':
        
        col1, col2 = st.columns(2)
        with col1:
            user_year_ind = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='user_year_ind')
        with col2:
            user_quarter_ind = st.selectbox('Quarter', ('1','2','3','4'),key='user_quarter_ind')
            
        # User Analysis Bar chart query
        mycursor.execute(f"SELECT State, SUM(Count) FROM agg_user WHERE Year = '{user_year_ind}' AND Quarter = '{user_quarter_ind}' GROUP BY State;")
        user_res_ind = mycursor.fetchall()
        user_res_ind_df = pd.DataFrame(np.array(user_res_ind), columns=['State', 'Count'])
        user_res2_ind_df = user_res_ind_df.set_index(pd.Index(range(1, len(user_res_ind_df)+1)))
        
         # Total User Count table query
        mycursor.execute(f"SELECT SUM(Count), AVG(Count) FROM agg_user WHERE Year = '{user_year_ind}' AND Quarter = '{user_quarter_ind}';")
        user_res_count_ind= mycursor.fetchall()
        user_res_count_ind_df = pd.DataFrame(np.array(user_res_count_ind), columns=['Total','Average'])
        user_res2_count_ind_df = user_res_count_ind_df.set_index(['Average'])
        
         #visualization for User
        # Drop a State column 
        user_res_ind_df.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data2 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        # Create a DataFrame with the state names column
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        # Combine the Gio State name with df_in_tr_tab_qry_rslt
        df_state_names_use['Count']=user_res_ind_df
        # convert dataframe to csv file
        df_state_names_use.to_csv('State_user.csv', index=False)
        # Read csv
        df_use = pd.read_csv('State_user.csv')
        # Geo plot
        fig_use = px.choropleth(
            df_use,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='Count',color_continuous_scale='thermal',title = 'User Analysis')
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33), height=800)
        st.plotly_chart(fig_use,use_container_width=True)
        
        # All India User Analysis Bar chart
        user_res2_ind_df['State'] = user_res2_ind_df['State'].astype(str)
        user_res2_ind_df['Count'] = user_res2_ind_df['Count'].astype(int)
        user_res2_ind_df_fig = px.bar(user_res2_ind_df , x = 'State', y ='Count', color ='Count', color_continuous_scale = 'Agsunset', title = 'User Analysis Chart', height = 700,)
        user_res2_ind_df_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(user_res2_ind_df_fig,use_container_width=True)
        st.info('**:green[This visualization helps you compare the total user counts across different states, allowing you to identify states with higher or lower user counts]**')

        
        # All India Total User calculation Table
        st.header('Total calculation')
        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(user_res2_ind_df)
        with col4:
            st.subheader('User Count')
            st.dataframe(user_res2_count_ind_df)
            
elif option =='State wise Transaction Data':

        col1, col2,col3 = st.columns(3)
        with col1:
            state_list = st.selectbox('State',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachalpradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_list')
        with col2:
            state_year = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='state_year')
        with col3:
            state_quarter = st.selectbox('Quarter', ('1','2','3','4'),key='state_quarter')         
            
        # SQL Query
        # Transaction Analysis bar chart query
        mycursor.execute(f"SELECT Transaction_type, Transaction_amount FROM agg_trans WHERE State = '{state_list}' AND Year = '{state_year}' AND Quarter = '{state_quarter}';")
        state_trans_bar_res = mycursor.fetchall()
        state_trans_bar_res_df = pd.DataFrame(np.array(state_trans_bar_res), columns=['Transaction_type', 'Transaction_amount'])
        state_trans_bar_res2_df = state_trans_bar_res_df.set_index(pd.Index(range(1, len(state_trans_bar_res_df)+1)))

        # Transaction Analysis table query
        mycursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM agg_trans WHERE State = '{state_list}' AND Year = '{state_year}' AND Quarter = '{state_quarter}';")
        state_trans_ana_res= mycursor.fetchall()
        state_trans_ana_res_df = pd.DataFrame(np.array(state_trans_ana_res), columns=['Transaction_type','Transaction_count','Transaction_amount'])
        state_trans_ana_res2_df = state_trans_ana_res_df.set_index(pd.Index(range(1, len(state_trans_ana_res_df)+1)))

        # Total Transaction Amount table query
        mycursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM agg_trans WHERE State = '{state_list}' AND Year = '{state_year}' AND Quarter = '{state_quarter}';")
        state_trans_amount_res = mycursor.fetchall()
        state_trans_amount_res_df = pd.DataFrame(np.array(state_trans_amount_res), columns=['Total','Average'])
        state_trans_amount_res2_df = state_trans_amount_res_df.set_index(['Average'])
        
        # Total Transaction Count table query
        mycursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM agg_trans WHERE State = '{state_list}' AND Year ='{state_year}' AND Quarter = '{state_quarter}';")
        state_trans_amount_res = mycursor.fetchall()
        state_trans_amount_res_df = pd.DataFrame(np.array(state_trans_amount_res), columns=['Total','Average'])
        state_trans_amount_res2_df = state_trans_amount_res_df.set_index(['Average'])
        
        # State wise Transaction Analysis bar chart
        state_trans_ana_res2_df['Transaction_type'] = state_trans_ana_res2_df['Transaction_type'].astype(str)
        state_trans_ana_res2_df['Transaction_amount'] = state_trans_ana_res2_df['Transaction_amount'].astype(float)
        state_trans_ana_res2_df_fig = px.bar(state_trans_ana_res2_df , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount',color_continuous_scale = 'Sunsetdark', title = 'Transaction Analysis Chart', height = 500,)
        state_trans_ana_res2_df_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(state_trans_ana_res2_df_fig,use_container_width=True)
        st.info('**:Violet[The above bar chart showing the result of PhonePe Transactions according to the states of India, Here we can observe the different types of payments by looking at graph]**')
        
        # State wise Total Transaction calculation Table 
        st.header('Total calculation')
        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(state_trans_ana_res2_df)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(state_trans_amount_res2_df)
            st.subheader('Transaction Count')
            st.dataframe(state_trans_amount_res2_df)
            
elif option=='State wise User Data':
        
        col5, col6 = st.columns(2)
        with col5:
            state_user_list = st.selectbox('State',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_user_list')
        with col6:
            state_user_year = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='state_user_year')
            
        # User Analysis Bar chart query
        mycursor.execute(f"SELECT Quarter, SUM(Count) FROM agg_user WHERE State = '{state_user_list}' AND Year = '{state_user_year}' GROUP BY Quarter;")
        state_user_ana_res = mycursor.fetchall()
        state_user_ana_res_df = pd.DataFrame(np.array(state_user_ana_res), columns=['Quarter', 'Count'])
        state_user_ana_res2_df = state_user_ana_res_df.set_index(pd.Index(range(1, len(state_user_ana_res_df)+1)))

       # Total User Count table query
        mycursor.execute(f"SELECT SUM(Count), AVG(Count) FROM agg_user WHERE State = '{state_user_list}' AND Year = '{state_user_year}';")
        state_user_count_res = mycursor.fetchall()
        state_user_count_res_df = pd.DataFrame(np.array(state_user_count_res), columns=['Total','Average'])
        state_user_count_res2_df = state_user_count_res_df.set_index(['Average'])
        
        #All India User Analysis Bar chart
        state_user_ana_res2_df['Quarter'] = state_user_ana_res2_df['Quarter'].astype(int)
        state_user_ana_res2_df['Count'] = state_user_ana_res2_df['Count'].astype(int)
        state_user_ana_res2_df_fig = px.bar(state_user_ana_res2_df, x = 'Quarter', y ='Count', color ='Count', color_continuous_scale = 'Teal', title = 'User Analysis Chart', height = 500,)
        state_user_ana_res2_df_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(state_user_ana_res2_df_fig,use_container_width=True)
        st.info('**:pink[The above User Analysis bar chart showing the result of PhonePe users according to the states in a four different quarters by looking at graph]**')


        #State wise User Total User calculation Table
        st.header('Total calculation')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(state_user_ana_res2_df)
        with col4:
            st.subheader('User Count')
            st.dataframe(state_user_count_res2_df)

elif option== 'Top 10 Transaction':

        top_trans_year = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='top_trans_year')

        # Top Transaction Analysis bar chart query
        mycursor.execute(f"SELECT State, SUM(Transaction_amount) As Transaction_amount FROM top_trans WHERE Year = '{top_trans_year}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_trans_ana_res = mycursor.fetchall()
        top_trans_ana_res_df = pd.DataFrame(np.array(top_trans_ana_res), columns=['State', 'Top Transaction amount'])
        top_trans_ana_res2_df = top_trans_ana_res_df.set_index(pd.Index(range(1, len(top_trans_ana_res_df)+1)))

        # Top Transaction Analysis table query
        mycursor.execute(f"SELECT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_trans WHERE Year = '{top_trans_year}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_trans_tab_res = mycursor.fetchall()
        top_trans_tab_res_df = pd.DataFrame(np.array(top_trans_tab_res), columns=['State', 'Top Transaction amount','Total Transaction count'])
        top_trans_tab_res2_df = top_trans_tab_res_df.set_index(pd.Index(range(1, len(top_trans_tab_res_df)+1)))

        # All India Transaction Analysis Bar chart
        top_trans_ana_res2_df['State'] = top_trans_ana_res2_df['State'].astype(str)
        top_trans_ana_res2_df['Top Transaction amount'] = top_trans_ana_res2_df['Top Transaction amount'].astype(float)
        top_trans_ana_res2_df_fig = px.bar(top_trans_ana_res2_df , x = 'State', y ='Top Transaction amount', color ='Top Transaction amount', color_continuous_scale = 'Brwnyl', title = 'Top Transaction Analysis Chart', height = 600,)
        top_trans_ana_res2_df_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(top_trans_ana_res2_df_fig,use_container_width=True)
        st.info('**:blue[The above bar chart showing the result of Top 10 Transactions according to the Transaction amount, Here we can observe the top 10 states with highest Transaction by looking at graph]**')


        #All India Total Transaction calculation Table
        st.header('Total calculation')
        st.subheader('Top Transaction Analysis')
        st.dataframe(top_trans_tab_res2_df)        
            
#for Top Ten User Transaction
else:
        top_user_year = st.selectbox('Year', ('2018','2019','2020','2021','2022'),key='top_user_year')
        
        # Top User Analysis bar chart query
        mycursor.execute(f"SELECT State, SUM(Registered_users) AS Top_user FROM top_user WHERE Year='{top_user_year}' GROUP BY State ORDER BY Top_user DESC LIMIT 10;")
        top_user_ana_res= mycursor.fetchall()
        top_user_ana_res_df = pd.DataFrame(np.array(top_user_ana_res), columns=['State', 'Total User count'])
        top_user_ana_res2_df = top_user_ana_res_df.set_index(pd.Index(range(1, len(top_user_ana_res_df)+1)))

        
        #All India User Analysis Bar chart
        top_user_ana_res2_df['State'] = top_user_ana_res2_df['State'].astype(str)
        top_user_ana_res2_df['Total User count'] = top_user_ana_res2_df['Total User count'].astype(float)
        top_user_ana_res2_df_fig = px.bar(top_user_ana_res2_df , x = 'State', y ='Total User count', color ='Total User count', color_continuous_scale = 'Aggrnyl', title = 'Top User Analysis Chart', height = 600,)
        top_user_ana_res2_df_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(top_user_ana_res2_df_fig,use_container_width=True)
        st.info('**:green[The above bar chart showing the result of Top 10 users according to the Transaction amount and states, Here we can observe the top 10 states with highest users by looking at graph]**')


        #All India Total Transaction calculation Table
        st.header('Total calculation')
        st.subheader('Total User Analysis')
        st.dataframe(top_user_ana_res2_df)

