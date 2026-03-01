import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("datacenter.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS servers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
server_name TEXT,
rack TEXT,
power_usage REAL
)
""")
conn.commit()

st.title("🏢 Data Center Resource Management")

menu = st.sidebar.selectbox("Menu", ["Add Server", "View Resources"])

if menu == "Add Server":
    name = st.text_input("Server Name")
    rack = st.text_input("Rack Number")
    power = st.number_input("Power Usage (Watts)", min_value=0.0)

    if st.button("Add"):
        cursor.execute("INSERT INTO servers(server_name,rack,power_usage) VALUES(?,?,?)",
                       (name, rack, power))
        conn.commit()
        st.success("Server Added!")

elif menu == "View Resources":
    df = pd.read_sql_query("SELECT * FROM servers", conn)
    st.dataframe(df)
    if not df.empty:
        st.metric("Total Power Usage", df["power_usage"].sum())
