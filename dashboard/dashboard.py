import streamlit as st
import pandas as pd

df = pd.read_csv("dashboard/main_data.csv")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])