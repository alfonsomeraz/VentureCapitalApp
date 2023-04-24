import streamlit as st
import pandas as pd
from database import get_data
import altair as alt


def main():
    st.title("Data Visualization")
    st.write("This page is to visualize the data from the database.")
    
    deals = get_data()

    df = pd.DataFrame(deals)
    df = df.drop(columns=['_id'])

    deal_size_by_industry = df.groupby('industry')['deal_size'].sum().reset_index()
    show_data = st.checkbox("Show Data", value=True)

    if show_data:
        st.dataframe(deal_size_by_industry)
    
    bars = (
        alt.Chart(deal_size_by_industry, title="Deals by Industry")
        .mark_bar()
        .encode(
            x='industry:N',
            y='deal_size:Q',
            color=alt.Color('industry:N')
        )
    )


    st.altair_chart(bars, theme="streamlit", use_container_width=True)



if __name__ == "__main__":
    main()