import streamlit as st
import plotly_express as px
import pandas as pd

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Think In Graphs - Dashboard")
st.subheader('Powered by [Think In Bytes](https://www.thinkinbytes.in)')

# Add a sidebar
st.sidebar.subheader("Control Panel")

placeholder = st.empty()

placeholder.subheader("Perform Data Analysis in few clicks")
placeholder.markdown("**Step 1** Choose whether you want to split date into date, month and year for detailed analysis <br/> **Step 2** Filter data using conditions and limits. For eg, display products whose prices are between 1000 INR and 5000 INR <br/> **Step 3** Select chart type <br/> **Step 4** Choose relevant column features <br/> ** Begin with uploading a csv file **"

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
all_columns = []

try:
    get_date = st.sidebar.selectbox(
    label="Split date ?",
    options=['None', 'Yes', 'No'])
    
    if get_date == 'Yes':
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        date_column = st.sidebar.selectbox(label="Split date ?",options=non_numeric_columns)
        df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y')
        df['month'] = pd.DatetimeIndex(df[date_column]).month
        df['year'] = pd.DatetimeIndex(df[date_column]).year
        df['day-date'] = pd.DatetimeIndex(df[date_column]).day
        df['month-year'] = pd.to_datetime(df[date_column]).dt.to_period('M') 
        placeholder.dataframe(df.astype('object'))
        
    
    if get_date == 'No':
        placeholder.dataframe(df.astype('object'))
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)

except Exception as e:
    print(e)
    st.write("Please upload file to the application.")

    
try:
    group_by_boolean = st.sidebar.checkbox('Perform Groupby')
    if group_by_boolean:
        group_by = st.sidebar.selectbox('Group data by: ', options=all_columns)

        group_by_list = group_by.split()
        columns = list(df.columns)
        columns.remove(group_by)
        grouped_data = df.groupby(group_by_list)[columns].sum()
        df = grouped_data.reset_index()
        placeholder.dataframe(df.astype('object'))
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        

except Exception as e:
    print(e)
    st.write("Please upload file to the application. Groupby Error !")    

st.sidebar.subheader("Filter data by conditions")

try:
    math = st.sidebar.selectbox(label = 'Choose relation', options = ['None','<', '>', '=', '*'])
    column_name = st.sidebar.selectbox('Column', options=all_columns)

    if math == '*':
        value1 = st.sidebar.text_input('enter upper bound:')
        value2 = st.sidebar.text_input('enter lower bound: ')
        df = df[(df[column_name] < float(value1)) & (df[column_name] > float(value2))]
        placeholder.dataframe(df.astype('object'))
    elif math == '<':
        value = st.sidebar.text_input('enter upper limit: ')
        df = df[df[column_name] < float(value)]
        placeholder.dataframe(df.astype('object'))
    elif math == '>':
        value = st.sidebar.text_input('enter lower limit: ')
        df = df[df[column_name] > float(value)]
        placeholder.dataframe(df.astype('object'))
    elif math == '=':
        value = st.sidebar.text_input('enter value that you want to match: ')
        if column_name in numeric_columns:
            df = df[df[column_name] == float(value)]
            placeholder.dataframe(df.astype('object'))
        elif column_name in non_numeric_columns:
            df = df[df[column_name] == str(value)]
            placeholder.dataframe(df.astype('object'))
            
except Exception as e:
    st.write(e)
    st.write("Please upload file to the application. Condition Error !")
    
    
st.sidebar.subheader("Data visualisation")
# add a select widget to the side bar
chart_select = st.sidebar.selectbox(
    label="Select the chart type",
    options=['Select chart','Scatterplots', 'Lineplots', 'Histogram', 'Funnel', 'Boxplot', 'Gantt']
)


if chart_select == 'Scatterplots':
    st.sidebar.subheader("Scatterplot Settings")
    st.subheader("Scatterplot")
    
    st.markdown("A scatter plot uses dots to represent values for two different numeric variables. The position of each dot on the horizontal and vertical axis indicates values for an individual data point. Scatter plots are used to observe relationships between variables.")
    
    st.subheader("When to use scatterplots")            
    st.markdown("A scatter plot can also be useful for identifying other patterns in data. We can divide data points into groups based on how closely sets of points cluster together. Scatter plots can also show if there are any unexpected gaps in the data and if there are any outlier points. ")
    st.markdown("Ideal for : ML Data Analysis, Finding outliers, ")
    
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
        
if chart_select == 'Funnel':
    st.sidebar.subheader("Funnel Settings")
    try:
        x = st.sidebar.selectbox('X axis', options=numeric_columns)
        y = st.sidebar.selectbox('Y axis', options=non_numeric_columns)
        plot = px.funnel(df, x=x, y=y)
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
        
if chart_select == 'Gantt':
    st.sidebar.subheader("Funnel Settings")
    try:
        x_start = st.sidebar.selectbox('start date', options=all_columns)
        df[x_start] = pd.to_datetime(df[x_start])
        x_end = st.sidebar.selectbox('end date', options=all_columns)
        df[x_end] = pd.to_datetime(df[x_end])
        task = st.sidebar.selectbox('Tasks', options=all_columns)
        plot = px.timeline(df, x_start=x_start, x_end=x_end, y=task)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
