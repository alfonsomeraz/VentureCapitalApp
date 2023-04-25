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
    

    company_count_by_industry = df.groupby('industry')['company'].count().reset_index()
    deal_size_by_industry = df.groupby('industry')['deal_size'].sum().reset_index()
    show_data = st.checkbox("Show Data", value=True)
    deal_data = pd.merge(company_count_by_industry, deal_size_by_industry, on='industry')

    if show_data:
        st.dataframe(deal_data)
    
    tab1, tab2 = st.tabs(["Deal Size by Industry", "Company Count by Industry"])
    
    with tab1:
        deal_bars = (
            alt.Chart(deal_size_by_industry, title="Deals by Industry")
            .mark_bar()
            .encode(
                x='industry:N',
                y='deal_size:Q',
                color=alt.Color('industry:N')
            )
        )
        st.altair_chart(deal_bars, theme="streamlit", use_container_width=True)
    with tab2:
        company_bars = (
            alt.Chart(company_count_by_industry, title="Companies by Industry")
            .mark_bar()
            .encode(
                x='industry:N',
                y='company:Q',
                color=alt.Color('industry:N')
            )
        )
        st.altair_chart(company_bars, theme="streamlit", use_container_width=True)



    


if __name__ == "__main__":
    main()