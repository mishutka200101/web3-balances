import streamlit as st

from utils.balancer_handler import *


st.set_page_config(page_title="Get Aptos balance")
st.title('Get Aptos balance')
with open('styles/main.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

addresses_str = st.text_area(label='Insert addresses that splitted by ENTER')
addresses = addresses_str.split('\n')

if addresses_str:
    df = pd.DataFrame(index=addresses, columns=['amount in USDT'])
    df.index.name = 'address'

    df = get_balance(df=df, chain="Aptos")
    st.write(df)
    st.write(
        f"""
        # Total balance ${sum(df['amount in USDT'])}
        """
    )
