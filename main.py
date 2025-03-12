import streamlit as st
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# --- Authentication ---
def auth_youtube():
    creds_json = json.loads(st.secrets["CLIENT_SECRETS_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_json,
        scopes=['https://www.googleapis.com/auth/yt-analytics.readonly']
    )
    return build('youtubeAnalytics', 'v2', credentials=creds)

# --- Fetch Data ---
def get_data(youtube, start_date, end_date):
    report = youtube.reports().query(
        ids='channel==MINE',
        startDate=start_date,
        endDate=end_date,
        metrics='views,averageViewDuration,averageViewPercentage,clickThroughRate',
        dimensions='video'
    ).execute()
    return pd.DataFrame(report.get('rows', []), report['columnHeaders']

# --- UI ---
st.set_page_config(layout="wide")
st.title("🎬 YouTube Analytics Dashboard")

if st.button("🔄 Refresh Data"):
    youtube = auth_youtube()

    # Get data
    df_mar, headers = get_data(youtube, '2024-03-01', '2024-03-11')
    df_mar = pd.DataFrame(df_mar, columns=[h['name'] for h in headers])

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Views", df_mar['views'].sum())
    col2.metric("Avg. Duration", f"{df_mar['averageViewDuration'].mean():.1f}s")
    col3.metric("CTR", f"{df_mar['clickThroughRate'].mean():.1%}")

    # Charts
    st.line_chart(df_mar.set_index('video')['views'])
    st.dataframe(df_mar)