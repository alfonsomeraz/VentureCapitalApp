import streamlit as st
import pandas as pd
import datetime
from database import get_data
from schema import Deal
from millify import millify



collection = get_data()

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["login_password"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter password to add new deals", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Enter password to add new deals", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True





def main():
  st.title('Venture Capital Dashboard')
  st.write("This dashboard is to track venture capital deals across the US.")

  deals = collection.find({})
  df = pd.DataFrame(list(deals))

  deal_form, news = st.columns(2)

  col1, col2, col3 = st.columns(3)

  col1.metric(label="Total Deals", value=df.shape[0])
  col2.metric(label="Total Invested Capital", value=millify(df['deal_size'].sum()))
  col3.metric(label="Number of Investors", value="Coming Soon")

  with deal_form:
    
    if check_password():
      with st.form("my_form", clear_on_submit=True):
        st.subheader(':blue[Add New Deals]')
        company = st.text_input("Company Name")
        interest = st.slider("Interest", min_value=0, max_value=5, step=1)
        industry = st.selectbox("Industry", ["Software", "Biotech", "Fintech", "Energy", "Other"])
        location = st.text_input("Location")
        deal_stage = st.selectbox("Deal Stage", ["Seed", "Series A", "Series B", "Series C"])
        deal_size = st.number_input("Deal Size $ (millions)", min_value=0, max_value=999, step=1)
        lead_investor = st.text_input("Lead Investor")
        lead_investor_location = st.text_input("Lead Investor Location")
        investors_input = st.text_input("Other Investors")
        investors = [x.strip() for x in investors_input.split(',')]
        date_added = datetime.datetime.now()

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
          new_deal = Deal(
            company=company,
            interest=interest,
            industry=industry,
            location=location,
            deal_stage=deal_stage,
            deal_size=deal_size,
            lead_investor=lead_investor,
            lead_investor_location=lead_investor_location,
            investors=investors,
            date_added=date_added
          )
          collection.insert_one(new_deal.dict())
          st.success("Deal Added!")


  with news:
     None


  st.subheader("Deals")
  df = df.drop(columns=['_id'])
  show_data = st.checkbox("Show Data", value=True)
  if show_data:
    st.dataframe(df)






if __name__ == "__main__":
  main()