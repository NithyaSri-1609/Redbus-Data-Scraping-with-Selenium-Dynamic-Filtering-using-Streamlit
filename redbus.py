import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Set page config
st.set_page_config(page_title="REDBUS APP", layout='wide')
st.title(":red[REDBUS APP]")

# Create a connection to the MySQL database using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:nithya@localhost/REDBUS')

# Query to fetch data from a table
query = "SELECT * FROM bus_details"
df = pd.read_sql(query, engine)

# Ensure correct data types
df['Rating'] = df['Rating'].astype(float)
df['Price'] = df['Price'].astype(float)

# Convert 'Departure time' and 'Arrival time' from timedelta to a proper string format
def convert_timedelta_to_str(td):
    if pd.isna(td):
        return "00:00:00"
    return f"{td.components.hours:02}:{td.components.minutes:02}:{td.components.seconds:02}"

df['Departure time'] = df['Departure time'].apply(convert_timedelta_to_str)
df['Arrival time'] = df['Arrival time'].apply(convert_timedelta_to_str)

# Split 'Bus Type' into 'AC' vs. 'Non-AC' and 'Seater' vs. 'Sleeper'
df['AC/Non-AC'] = df['Bus Type'].apply(lambda x: 'Non-A/C' if 'Non A/C' in x or 'Non A.C' in x or 'Non-AC' in x or 'Non AC' in x else 'A/C')
df['Seater/Sleeper'] = df['Bus Type'].apply(lambda x: 'Seater' if 'Seater' in x else 'Sleeper' if 'Sleeper' in x else 'others')

# Sidebar for navigation
st.sidebar.image(r'C:\Users\hp\Downloads\redBus Logo - PNG Logo Vector Brand Downloads (SVG, EPS).jpg', width=100)
st.sidebar.title(":red[MAIN MENU]")

# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'State_name' not in st.session_state:
    st.session_state.State_name = ''
if 'route' not in st.session_state:
    st.session_state.route = ''
if 'ac_type' not in st.session_state:
    st.session_state.ac_type = ''
if 'seat_type' not in st.session_state:
    st.session_state.seat_type = ''
if 'start_time' not in st.session_state:
    st.session_state.start_time = ''
if 'fare_range' not in st.session_state:
    st.session_state.fare_range = (float(df['Price'].min()), float(df['Price'].max()))

# Sidebar buttons
home_button = st.sidebar.button(":red[HOME]")
select_bus_button = st.sidebar.button(":red[SELECT THE BUS]")
about_button = st.sidebar.button(":red[ABOUT APP]")

# Main interface
# Home page content
if home_button:
    st.session_state.page = 'home'
elif select_bus_button:
    st.session_state.page = 'select_bus'
elif about_button:
    st.session_state.page = 'about_app'

# Display content based on page
if st.session_state.page == 'home':
    st.image(r'F:\NITHYA ONLINE DATA SCIENCE\PROJECT REDBUS\1_S-95TWd9jgxT87cKkZWnFg.jpg', width=780)

elif st.session_state.page == 'about_app':
    # Display project description when "Home" button is clicked
    st.header("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit (Domain-Transportation)")
    st.write("""
    # Project Overview:
             
    The "Redbus Data Scraping and Filtering with Streamlit Application" aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.

    # Skills Takeaway From This Project
    • Web Scraping using Selenium
             
    • Python Programming
             
    • Streamlit for Web Applications
            
    • SQL for Data Storage and Retrieval

    # Objectives
    1. Automate Data Extraction:
             
        • Leverage Selenium to scrape detailed bus travel data from Redbus.
             
        • Extract crucial information including bus routes, schedules, prices, and seat availability.
             
    2. Data Storage:
             
        • Store the scraped data in a SQL database.
             
    3. Streamlit Application:
             
        • Use a Streamlit application to display and filter the scraped data.

    # Technology Used
             
    • Web Scraping: Selenium
             
    • Programming Language: Python
             
    • Web Application Framework: Streamlit
             
    • Database: MySQL
             
    • Data Processing and Analysis: Pandas

    # Project Workflow
    1. Web Scraping with Selenium:
             
        • Set up Selenium WebDriver to interact with the Redbus website.
             
        • Navigate through the website to collect data on bus routes, schedules, prices, and seat availability.
             
        • Parse and structure the collected data.
             
    2. Data Storage in SQL:
             
        • Design and create a SQL database schema to store the scraped data.
             
        • Use SQL queries to insert the structured data into the database.
             
    3. Developing the Streamlit Application:
             
        • Build a user interface using Streamlit to display the bus travel data.
             
        • Implement interactive filters to allow users to explore the data based on various criteria (e.g., route, schedule, price).
             
        • Provide visualizations and insights to help users make data-driven decisions.

    # Benefits
             
    • Automated Data Collection: Save time and reduce manual effort in collecting bus travel data.
             
    • Centralized Data Storage: Organize and manage data efficiently using a SQL database.
             
    • Interactive Data Exploration: Allow users to explore and analyze the data through a user-friendly Streamlit application.
             
    • Enhanced Decision-Making: Provide valuable insights to improve operational efficiency and strategic planning in the transportation industry.
             
    """)

elif st.session_state.page == 'select_bus':

    # Filter options

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.State_name = st.selectbox('SELECT STATE', options=[''] + df['State Name'].unique().tolist(), index=0)
    
    filtered_routes = df[df['State Name'] == st.session_state.State_name]['Route Name'].unique().tolist() if st.session_state.State_name else df['Route Name'].unique().tolist()
    with col2:
        st.session_state.route = st.selectbox('SELECT ROUTE', options=[''] + filtered_routes, index=0)
    

    st.session_state.fare_range = st.slider(
            'Bus Fare Range',
            min_value=float(df['Price'].min()),
            max_value=float(df['Price'].max()),
            value=(float(df['Price'].min()), float(df['Price'].max()))
        )
    
    col5, col6 = st.columns(2)
    with col5:
        st.session_state.ac_type = st.selectbox('AC/Non-AC', options=[''] + df['AC/Non-AC'].unique().tolist(), index=0)
    with col6:
        st.session_state.seat_type = st.selectbox('Seater/Sleeper', options=[''] + df['Seater/Sleeper'].unique().tolist(), index=0)

    # Apply filters to the dataframe

    filtered_df = df
    if st.session_state.State_name:
        filtered_df = filtered_df[filtered_df['State Name'].str.strip() == st.session_state.State_name]
    if st.session_state.route:
        filtered_df = filtered_df[filtered_df['Route Name'].str.strip() == st.session_state.route]
    if st.session_state.ac_type:
        filtered_df = filtered_df[filtered_df['AC/Non-AC'].str.strip() == st.session_state.ac_type]
    if st.session_state.seat_type:
        filtered_df = filtered_df[filtered_df['Seater/Sleeper'].str.strip() == st.session_state.seat_type]
    if st.session_state.start_time:
        filtered_df = filtered_df[filtered_df['Departure time'].str.strip() == st.session_state.start_time]
    if st.session_state.fare_range:
        filtered_df = filtered_df[(filtered_df['Price'] >= st.session_state.fare_range[0]) & (filtered_df['Price'] <= st.session_state.fare_range[1])]

    st.dataframe(filtered_df)
    
    # Show if no results found
    if filtered_df.empty:
        st.write("No buses match the selected criteria.")
