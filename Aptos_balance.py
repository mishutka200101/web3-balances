import streamlit as st

from utils.balancer_handler import *


st.set_page_config(page_title="Get Aptos balance")
with open('styles/main.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
st.title('Get Aptos balance')


addresses_str = st.text_area(label='Insert addresses that splitted by ENTER')
addresses = addresses_str.split('\n')
addresses_stripped = [_.strip() for _ in addresses]

if addresses_str:
    aptos_df = pd.DataFrame(index=addresses_stripped, columns=['amount in USDT', 'txs'])
    aptos_df.index.name = 'address'

    aptos_df = get_balance(df=aptos_df, chain="Aptos")
    st.dataframe(data=aptos_df, use_container_width=True)
    st.write(
        f"""
        # Total balance ${round(sum(aptos_df['amount in USDT'], 2))}
        """
    )
