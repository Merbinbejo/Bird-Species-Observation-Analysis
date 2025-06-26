import mysql.connector
import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt


def get_data(query, params=None):
    # Establish connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",        # Replace with your host
        user="root",    # Replace with your username
        password="Prabhudhas@1",# Replace with your password
        database="bird_monitoring_data_db"    # Replace with your database name
    )
    
    # Execute the query with or without parameters
    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)
    # Close the connection
    conn.close()
    
    return df
def show_area_chart():
    graph_query2 = """
        SELECT Location_type, Temperature, Humidity 
        FROM forest
        UNION
        SELECT Location_type, Temperature, Humidity 
        FROM grassland;
    """
    df = get_data(graph_query2)

    if df.empty:
        st.warning("No data available to display.")
        return

    df['Index'] = df.index

    df_melted = df.melt(id_vars=['Index', 'Location_type'], 
                    value_vars=['Temperature', 'Humidity'], 
                    var_name='Metric', value_name='Value')

    df_melted['Metric'] = df_melted['Metric'].replace({
        'Temperature': 'Temperature (°C)',
        'Humidity': 'Humidity (%)'
    })
    highlight_df = df_melted.loc[df_melted.groupby("Metric")["Value"].idxmax()]

    area = alt.Chart(df_melted).mark_area(opacity=0.5).encode(
        x=alt.X('Index:O', title='Record Index'),
        y=alt.Y('Value:Q', title='Environmental Values'),
        color=alt.Color('Metric:N', title='Environmental Metric')
    ).properties(title="Temperature and Humidity with Max Highlights")

    points = alt.Chart(highlight_df).mark_point(color='red', size=100).encode(
        x='Index:O',
        y='Value:Q',
        tooltip=['Metric:N', 'Value:Q', 'Location_type:N']
    )

    chart = area + points

    st.title("Variation of Humidity and Temperature by Location")
    st.altair_chart(chart, use_container_width=True)
    st.divider()

# Sidebar for navigation

st.set_page_config(page_title="Bird Monitering Data Analysis", layout="wide")
st.markdown("""
    <style>
    /* Tabs container */
    .stTabs {
        display: flex;
        justify-content: center;
    }

    /* All tab styles */
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 6px;
        padding: 30px 80px;
        margin-right: 8px;
        font-size: 18px;
        font-weight: 600;              /* Bold */
        font-style: italic;            /* Italic */
        font-family: 'Segoe UI', sans-serif;  /* Font family */
        text-transform: uppercase;     /* Make text uppercase */
        color: #333333;
    }

    /* Selected tab style */
    .stTabs [aria-selected="true"] {
        background-color: #2c7be5;
        color: white;
        font-weight: 700;
        font-style: normal;
    }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏚️Home", "🔍 Search", "📊 Species at Risk", "👤 Search by Code"])    
with tab1:
    st.sidebar.title("Navigation")
    st.sidebar.title("Filter Options")
    species="""SELECT DISTINCT Common_Name FROM forest"""
    Interval_length="""SELECT DISTINCT Interval_Length FROM forest"""
    ID_method="""SELECT DISTINCT ID_Method FROM forest"""
    selected_location=st.sidebar.radio("Select Location ",["Forest","Grassland"])
    selected_species=st.sidebar.selectbox("Select Species ",get_data(species))
    selected_length=st.sidebar.selectbox("Interval Length",get_data(Interval_length))
    selected_ID=st.sidebar.selectbox("ID Method",get_data(ID_method))

    clicked_button=st.sidebar.button("search")
    if clicked_button:
        get_details=f"""SELECT Common_Name,Observer,Interval_Length,ID_Method,Sky,Wind,Disturbance,PIF_Watchlist_Status
                        FROM {selected_location}
                        WHERE Common_Name=%s AND Interval_Length=%s AND ID_Method=%s"""
        filter_data=get_data(get_details,params=(selected_species,selected_length,selected_ID))
        if not filter_data.empty:
            st.table(filter_data)
        else:
            st.write("No Data Found")
        
    st.subheader("📊 Bird Species Monitoring")
    st.markdown(f"""<h6>Bird species monitoring commonly include establishing baselines of bird presence, tracking population trends, assessing species' responses to environmental changes, and supporting conservation efforts.These  are crucial for understanding ecosystem health, guiding conservation strategies, and informing policy decisions. </h6>
                        <ul>
                              <li>Baseline Establishment and Trend Monitoring</li>
                              <li>Understanding Species' Responses</li>
                              <li>Supporting Conservation</li>
                              <li>Broader Ecological Insights</li>
                        </ul>
                        """, unsafe_allow_html=True)
    st.subheader("SPECIES COUNT")
    with st.container():
        a,b=st.columns(2)
        with a:
            query1="""SELECT COUNT(DISTINCT Common_Name) AS "Total Number Of Species Observer in forest"
                        FROM forest"""
            df1=get_data(query1)
            str_df1=str(df1["Total Number Of Species Observer in forest"][0])
            st.markdown(f"""<div style="background-color:#f9f9f9; padding:20px; border-radius:10px;
                        border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);">
                        <h4>No Of Species Observer in Forest <br>{str_df1}</h4>
                        """, unsafe_allow_html=True)
        with b:
            query2="""SELECT COUNT(DISTINCT Common_Name) AS "Total Number Of Species Observer in grassland"
            FROM grassland"""
            df2=get_data(query2)
            str_df2=str(df2["Total Number Of Species Observer in grassland"][0])
            st.markdown(f"""<div style="background-color:#f9f9f9; padding:20px; border-radius:10px;
                        border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);">
                        <h4>No Of Species Observer in Grassland <br>{str_df2}</h4>
                        """, unsafe_allow_html=True)


    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        graph_query="""SELECT Observer, COUNT(Common_Name) AS Observation_Count
                    FROM forest
                    GROUP BY Observer
                    ORDER BY Observation_Count DESC;"""
        graph_df=get_data(graph_query)
        color=["red","green","skyblue"]
        fig1, ax1 = plt.subplots()
        ax1.pie(graph_df['Observation_Count'],labels=graph_df['Observer'], autopct='%1.1f%%', startangle=90,colors=color)
        ax1.axis('equal')
        ax1.set_title('No of Species Observed By Observor in Forest')
        st.pyplot(fig1)

# Second pie chart in right column
    with col2:
        graph_query1="""SELECT Observer, COUNT(Common_Name) AS Observation_Count
                    FROM grassland
                    GROUP BY Observer
                    ORDER BY Observation_Count DESC;"""
        graph_df1=get_data(graph_query1)
        fig2, ax2 = plt.subplots()
        color=["red","green","blue"]
        ax2.pie(graph_df1['Observation_Count'],labels=graph_df1['Observer'], autopct='%1.1f%%', startangle=90,colors=color)
        ax2.axis('equal')
        ax2.set_title('No of Species Observed By Observor in Grassland')
        st.pyplot(fig2)
        st.divider()

    graph_query2 = """
        SELECT Location_type, Temperature, Humidity 
        FROM forest
        UNION
        SELECT Location_type, Temperature, Humidity 
        FROM grassland;
    """
    df = get_data(graph_query2)

    if df.empty:
        st.warning("No data available to display.")

    df['Index'] = df.index

    df_melted = df.melt(id_vars=['Index', 'Location_type'], 
                    value_vars=['Temperature', 'Humidity'], 
                    var_name='Metric', value_name='Value')

    df_melted['Metric'] = df_melted['Metric'].replace({
        'Temperature': 'Temperature (°C)',
        'Humidity': 'Humidity (%)'
    })
    highlight_df = df_melted.loc[df_melted.groupby("Metric")["Value"].idxmax()]

    area = alt.Chart(df_melted).mark_area(opacity=0.5).encode(
        x=alt.X('Index:O', title='Record Index'),
        y=alt.Y('Value:Q', title='Environmental Values'),
        color=alt.Color('Metric:N', title='Environmental Metric')
    ).properties(title="Temperature and Humidity with Max Highlights")

    points = alt.Chart(highlight_df).mark_point(color='red', size=100).encode(
        x='Index:O',
        y='Value:Q',
        tooltip=['Metric:N', 'Value:Q', 'Location_type:N']
    )

    chart = area + points

    st.title("Variation of Humidity and Temperature by Location")
    st.altair_chart(chart, use_container_width=True)
    st.divider()

with tab2:
    col1,col2,col3=st.columns(3)
    Location = get_data("""SELECT Location_type FROM forest
                        UNION
                        SELECT Location_type FROM grassland;""")["Location_type"].tolist()
    
    # Filters
    location = st.selectbox("Select Location Type", Location)
    date_option = st.selectbox("Filter By:", ["Specific Day", "Entire Month"])
    if date_option == "Specific Day":
        selected_date = st.date_input("Choose a Date")
        st.markdown(
                """
                <style>
                /* Fix width */
                div.stDateInput > div {
                    width: 300px !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        
        a=st.button("Search")
        if a:
            
            query ="""SELECT Plot_Name,Common_Name,Date,Scientific_Name,Location_Type,Sex FROM forest WHERE Location_Type=%s AND Date =%s
                        UNION
                       SELECT Plot_Name,Common_Name,Date,Scientific_Name,Location_Type,Sex FROM Grassland WHERE Location_Type=%s AND Date =%s"""
            df = get_data(query, params=(location, selected_date.strftime("%y-%m-%d"),location, selected_date.strftime("%y-%m-%d"),))
            st.table(df)
            st.write(len(df))
            

    else:
        selected_month = st.selectbox("Select Month", range(1, 13))
        query = "SELECT Plot_Name,Common_Name,Date,Scientific_Name,Location_Type FROM forest WHERE Location_Type =%s AND month(Date) = %s"
        df1 = get_data(query, params=(location, f"{selected_month:02d}"))
        st.table(df1)

    if df.empty or df1.empty:
        range1=st.slider("Rank range",0, 500,10)
        empty_query1="""SELECT Plot_Name,Start_Time,End_Time,Observer,Common_Name,Sky,Wind,Disturbance 
                        FROM forest
                        LIMIT %s;"""
        empty_query2= """SELECT Plot_Name,Start_Time,End_Time,Observer,Common_Name,Sky,Wind,Disturbance
                         FROM grassland
                         LIMIT %s;"""
        st.write("### bird data")
        st.markdown("""<h1> Forest </h1>""",unsafe_allow_html=True)
        st.table(get_data(empty_query1,params=(range1,)))
        st.markdown("""<h1> Grassland </h1>""",unsafe_allow_html=True)
        st.table(get_data(empty_query2,params=(range1,)))

with tab3:
    st.subheader("Bird Species At Risk")
    query4="""SELECT Common_Name,
                   COUNT(*) AS Risk,
                   Location_Type AS Location
                FROM grassland
                WHERE PIF_Watchlist_Status = TRUE
                GROUP BY Common_Name, Location_Type
                UNION
                SELECT Common_Name,
                   COUNT(*) AS Risk,
                   Location_Type AS Location
                FROM forest
                WHERE PIF_Watchlist_Status = TRUE
                GROUP BY Common_Name, Location_Type
                ORDER BY Risk DESC;"""
    df4=get_data(query4)
    st.table(df4)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        pie_query1="""SELECT Common_Name AS Name,
                           COUNT(*) AS AtRisk
                        FROM forest
                        WHERE PIF_Watchlist_Status = TRUE
                        GROUP BY Common_Name;"""
        pie_chart1=get_data(pie_query1)
        fig3, ax3 = plt.subplots()
        ax3.pie(pie_chart1['AtRisk'],labels=pie_chart1['Name'], autopct='%1.1f%%', startangle=35)
        ax3.axis('equal')
        ax3.set_title('No of Species At Risk in Forest')
        
        st.pyplot(fig3)
        st.divider()
# Second pie chart in right column
    with col2:
        pie_query2="""SELECT Common_Name AS Name,
                           COUNT(*) AS AtRisk
                        FROM grassland
                        WHERE PIF_Watchlist_Status = TRUE
                        GROUP BY Common_Name;"""
        pie_chart2=get_data(pie_query2)
        fig4, ax4 = plt.subplots()
        ax4.pie(pie_chart2['AtRisk'],labels=pie_chart2['Name'], autopct='%1.1f%%', startangle=45)
        ax4.axis('equal')
        ax4.set_title('No of Species At Risk in Grassland')
        st.pyplot(fig4)
        st.divider()

with tab4:
    AOU_Code="""SELECT DISTINCT AOU_Code FROM forest;"""
    
    st.markdown(
        """
        <style>
        .stSelectbox > div {
            width: 300px !important;  /* set desired width */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    Code=st.selectbox("AOU_Code",get_data(AOU_Code),)
    loc=st.selectbox("Select Location Type",["forest","grassland"],)
    b=st.button("Search",key="button1")
    if b:
        query5=f"""SELECT Common_Name,Sex,Temperature,Humidity,Sky,Wind,Disturbance
                    FROM {loc}
                    WHERE AOU_Code=%s;"""
        df5=get_data(query5,params=(Code,))
        st.table(df5)
