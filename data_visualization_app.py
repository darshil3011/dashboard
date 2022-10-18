import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Think In Graphs - Dashboard")
st.markdown('Powered by [Think In Bytes](https://www.thinkinbytes.in)')

# Add a sidebar
st.sidebar.subheader("Control Panel")

placeholder = st.empty()
image = Image.open('steps.png')
placeholder.image(image)

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
                        label="Upload your CSV or Excel file. (200MB max)",
                         type=['csv', 'xlsx'])

global df
if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
        df = df.dropna()
        if len(df) > 1000:
            st.error('Dataframe less than 1000 rows are supported in free version. Dataframe will be automatically sliced to first 1000 rows. For premium version, contact www.thinkinbytes.in')
            df = df[0:1000]
    except Exception as e:
        st.error('Currently, we only support csv files. Please upload relevant file format !')
        df = pd.read_excel(uploaded_file)

global numeric_columns
global non_numeric_columns
global all_columns
all_columns = []



#Select Data
st.sidebar.subheader("Limit Dataframe")


try:
    limit_boolean = st.sidebar.checkbox('Limit Data: ')
                                        
    if limit_boolean:
        data_length = len(df)
        limit_index = st.sidebar.slider('Limit data till row: ', 1, data_length, 1)
        df = df[0:limit_index]

except Exception as e:
    st.write("Please select appropriate row number till which you want to limit your dataframe")


#Split Date
st.sidebar.subheader("Split Date column")


try:
    date_boolean = st.sidebar.checkbox('Split Date: ')
    
    if date_boolean:
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        all_columns.insert(0, None)
        numeric_columns.insert(0, None)
        non_numeric_columns.insert(0, None)
        date_column = st.sidebar.selectbox(label="Split date ?",options=non_numeric_columns)
        df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y')
        df['month'] = pd.DatetimeIndex(df[date_column]).month
        df['year'] = pd.DatetimeIndex(df[date_column]).year
        df['day-date'] = pd.DatetimeIndex(df[date_column]).day
        df['month-year'] = pd.to_datetime(df[date_column]).dt.to_period('M') 
        placeholder.dataframe(df.astype('object'))
        
    
    else:
        placeholder.dataframe(df.astype('object'))
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        all_columns.insert(0, None)
        numeric_columns.insert(0, None)
        non_numeric_columns.insert(0, None)
        

except Exception as e:
    st.write("Please upload file to the application.")

#Filter Data     
st.sidebar.subheader("Filter data by conditions")
        

try:
    filter_boolean = st.sidebar.checkbox('Perform Filter')
    if filter_boolean:
        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        all_columns.insert(0, None)
        numeric_columns.insert(0, None)
        non_numeric_columns.insert(0, None)
        math = st.sidebar.selectbox(label = 'Choose relation', options = ['None','<', '>', '=', '*'])


        if math == '*':
            column_name = st.sidebar.selectbox('Column', options=numeric_columns)
            value1 = st.sidebar.text_input('enter upper bound:')
            value2 = st.sidebar.text_input('enter lower bound: ')
            df = df[(df[column_name] < float(value1)) & (df[column_name] > float(value2))]
            placeholder.dataframe(df.astype('object'))
        elif math == '<':
            column_name = st.sidebar.selectbox('Column', options=numeric_columns)
            value = st.sidebar.text_input('enter upper limit: ')
            df = df[df[column_name] < float(value)]
            placeholder.dataframe(df.astype('object'))
        elif math == '>':
            column_name = st.sidebar.selectbox('Column', options=numeric_columns)
            value = st.sidebar.text_input('enter lower limit: ')
            df = df[df[column_name] > float(value)]
            placeholder.dataframe(df.astype('object'))
        elif math == '=':
            column_name = st.sidebar.selectbox('Column', options=all_columns)
            value = st.sidebar.text_input('enter value that you want to match: ')
            if column_name in numeric_columns:
                df = df[df[column_name] == float(value)]
                placeholder.dataframe(df.astype('object'))
            elif column_name in non_numeric_columns:
                df = df[df[column_name] == str(value)]
                placeholder.dataframe(df.astype('object'))
            
except Exception as e:
    st.error('Please choose appropriate columns. less than, greater than and between conditions can be used with numerical columns only. Use split date feature if you want to filter data using dates')

#Groupby  
st.sidebar.subheader("Group data by column")


try:
    group_by_boolean = st.sidebar.checkbox('Perform Groupby')
    
    if group_by_boolean:
        all_columns = list(df.columns)
        
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
        all_columns.insert(0, None)
        numeric_columns.insert(0, None)
        non_numeric_columns.insert(0, None)
        
        

except Exception as e:
    print(e)
    st.write("Please upload file to the application. Groupby Error !")    

#Data viz   
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
    st.subheader("Line plot")
    
    st.markdown("A line graph is a type of chart or graph that is used to show information that changes over time. A line graph can be plotted using several points connected by straight lines.")
    
    st.subheader("When to use Lineplots")            
    st.markdown("A line plot can be used to visualise financial commodities or instruments and observe their trend over time function.")
    st.markdown("Ideal for : Time-series analyses, comparison of two quantities")
    
    try:
        x_values = st.sidebar.selectbox('X axis', options=all_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        #df = df.sort_values(by=y_values, ascending=True)
        plot = px.line(data_frame=df, x=x_values, y=y_values, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Histogram':
    st.sidebar.subheader("Histogram Settings")
    st.subheader("Histogram")
    
    st.markdown("A histogram is representation of the distribution of numerical data, where the data are binned and the count for each bin is represented. ")
    
    st.subheader("When to use Histogram")            
    st.markdown("A histogram can be used to visualise distribution of a numeric data column. In case of non-numeric column, it helps to visualise count of each value.")
    st.markdown("Ideal for : visualise occurence of an event, visualise data distriution")
    try:
        x = st.sidebar.selectbox('Feature', options=all_columns)
        bin_size = st.sidebar.slider("Number of Bins", min_value=10,
                                     max_value=100, value=20)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        plot = px.histogram(x=x, data_frame=df, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
        
if chart_select == 'Funnel':
    st.sidebar.subheader("Funnel Settings")
    st.subheader("Funnel Chart")
    
    st.markdown("A funnel chart is a specialized chart type that demonstrates the flow of data through different levels or tasks. The chart takes its name from its shape, which starts from a broad head and ends in a narrow neck")
    
    st.subheader("When to use Funnel chart")            
    st.markdown("Funnel charts are most often seen in business or sales contexts, where we need to track how a starting set of visitors or users drop out of a process or flow. This chart type shows how the starting whole breaks down into progressive parts.")
    st.markdown("Ideal for : web-traffic analysis, sales conversion")
    try:
        x = st.sidebar.selectbox('X axis', options=numeric_columns)
        y = st.sidebar.selectbox('Y axis', options=non_numeric_columns)
        plot = px.funnel(df, x=x, y=y)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Boxplot':
    st.sidebar.subheader("Boxplot Settings")
    st.subheader("Box Plot")
   
    st.markdown("Box plot represents statistical data on a plot in which a rectangle is drawn to represent the second and third quartiles, usually with a vertical line inside to indicate the median value. The lower and upper quartiles are shown as horizontal lines either side of the rectangle.")
    st.subheader("When to use Box Plot")            
    st.markdown("Box plots provide a visual summary of the data enabling researchers to quickly identify mean values, the dispersion of the data set, and signs of skewness.")
    st.markdown("Ideal for : Identifying Inter-Quartile Ranges, Mean, Median and Outliers")
    try:
        y = st.sidebar.selectbox("Y axis", options=numeric_columns)
        x = st.sidebar.selectbox("X axis", options=all_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        plot = px.box(data_frame=df, y=y, x=x, color=color_value)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
        
if chart_select == 'Gantt':
    st.sidebar.subheader("Gantt Chart Settings")
    st.subheader("Gantt Chart")
   
    st.markdown("Gantt Chart is uses a series of horizontal lines shows the amount of work done or production completed in certain periods of time in relation to the amount planned for those periods.")
    st.subheader("When to use Gantt Chart")            
    st.markdown("Gantt charts are useful for planning and scheduling projects. They help you assess how long a project should take, determine the resources needed, and plan the order in which you'll complete tasks. They're also helpful for managing the dependencies between tasks.")
    st.markdown("Ideal for : Project Management, Timeline overview")
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
        
st.sidebar.markdown('[Reset](https://thinkingraphs.streamlitapp.com/)')
