import pandas as pd
import streamlit as st
from pinotdb import connect
from datetime import datetime
import plotly.express as px
import time


conn = connect(host="localhost", port=9001, path="/sql", scheme="http")

HISTORY_IN_SECONDS = 60


def plot_number_of_events():
    st.header("Number of events")
    query = f"""
        select
            datetrunc('second', ts, 'MILLISECONDS') as dateSecond
            , datetimeconvert(
                ts, 
                '1:MILLISECONDS:EPOCH', 
                '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss', 
                '1:MILLISECONDS'
            ) AS convertedTimeSecond 
            , count(*) as cnt_events
            , sum(value) as sum_value
        from
            fakeevents
        where
            ts > ago('PT{HISTORY_IN_SECONDS}S')
        group by
            dateSecond
            , convertedTimeSecond
        order by
            dateSecond desc
        limit
            {HISTORY_IN_SECONDS}
    """

    curs = conn.cursor()
    curs.execute(query)

    df_ts = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    fig = px.bar(df_ts, x="convertedTimeSecond", y="sum_value")
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Total events",
        yaxis_range=[0, 50],
    )
    st.plotly_chart(fig, use_container_width=True)


st.sidebar.title("Latest Update")

now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.sidebar.write(f"Last update: {dt_string}")

SLEEP_TIME = 2
st.session_state.sleep_time = SLEEP_TIME
st.session_state.auto_refresh = True

plot_number_of_events()

time.sleep(SLEEP_TIME)
st.experimental_rerun()
