import streamlit as st
import plotly_express as px
import pandas as pd

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Data Visualization App")

# Add a sidebar
st.sidebar.subheader("Visualization Settings")

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
                        label="Upload your CSV or Excel file. (200MB max)",
                         type=['csv', 'xlsx'])

global df
if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)

global numeric_columns
global non_numeric_columns
global all_columns

try:
    get_date = st.sidebar.selectbox(
    label="Split date ?",
    options=['None', 'Yes', 'No'])
    
    if get_date == 'Yes':
        df['date'] = pd.to_datetime(df['date'])
        df['month_ex'] = pd.DatetimeIndex(df['date']).month
        df['year_ex'] = pd.DatetimeIndex(df['date']).year
        df['date_ex'] = pd.DatetimeIndex(df['date']).day
        df['month_year_ex'] = pd.to_datetime(df['date']).dt.to_period('M') 
        st.write(df.astype('object'))
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
    
    if get_date == 'No':
        st.write(df.astype('object'))
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)

except Exception as e:
    print(e)
    st.write("Please upload file to the application.")

    
try:
    group_by = st.sidebar.selectbox('Group data by: ', options=all_columns)
  
    group_by_list = group_by.split()
    columns = list(df.columns)
    columns.remove(group_by)
    grouped_data = df.groupby(group_by_list)[columns].sum()
    df = grouped_data.reset_index()
    st.write(df.astype('object'))

except Exception as e:
    print(e)
    st.write("Please upload file to the application. Groupby Error !")    
    

try:
    math = st.sidebar.selectbox(label = 'Choose relation', options = ['None','<', '>', '=', '*'])
    column_name = st.sidebar.selectbox('Column', options=all_columns)

    if math == '*':
        value1 = st.sidebar.text_input('enter upper bound:')
        value2 = st.sidebar.text_input('enter lower bound: ')
        df = df[(df[column_name] < int(value1)) & (df[column_name] > int(value2))]
    elif math == '<':
        value = st.sidebar.text_input('enter value that you want to match: ')
        df = df[df[column_name] < int(value)]
    elif math == '>':
        value = st.sidebar.text_input('enter value that you want to match: ')
        df = df[df[column_name] > int(value)]
    elif math == '=':
        value = st.sidebar.text_input('enter value that you want to match: ')
        if column_name in numeric_columns:
            df = df[df[column_name] == int(value)]
        elif column_name in non_numeric_columns:
            df = df[df[column_name] == str(value)]
            
except Exception as e:
    st.write(e)
    st.write("Please upload file to the application. Condition Error !")
    
    

# add a select widget to the side bar
chart_select = st.sidebar.selectbox(
    label="Select the chart type",
    options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
)


if chart_select == 'Scatterplots':
    st.sidebar.subheader("Scatterplot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=all_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value)
        # display the chart
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Lineplots':
    st.sidebar.subheader("Line Plot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=all_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        df = df.sort_values(by=y_values, ascending=True)
        plot = px.line(data_frame=df, x=x_values, y=y_values, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Histogram':
    st.sidebar.subheader("Histogram Settings")
    try:
        x = st.sidebar.selectbox('Feature', options=numeric_columns)
        bin_size = st.sidebar.slider("Number of Bins", min_value=10,
                                     max_value=100, value=40)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        plot = px.histogram(x=x, data_frame=df, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Boxplot':
    st.sidebar.subheader("Boxplot Settings")
    try:
        y = st.sidebar.selectbox("Y axis", options=numeric_columns)
        x = st.sidebar.selectbox("X axis", options=all_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        plot = px.box(data_frame=df, y=y, x=x, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
