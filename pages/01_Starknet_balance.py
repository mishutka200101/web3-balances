import streamlit as st

from utils.balancer_handler import *


st.set_page_config(page_title="Get Starknet balance")
with open('styles/main.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
st.title('Get Starknet balance')


starknet_addresses_str = st.text_area(label='Insert addresses that splitted by ENTER')
starknet_addresses = starknet_addresses_str.split('\n')
starknet_addresses_stripped = [_.strip() for _ in starknet_addresses]

if starknet_addresses_str:
    starknet_df = pd.DataFrame(index=starknet_addresses_stripped, columns=['amount in USDT', 'txs'])
    starknet_df.index.name = 'address'

    starknet_df = get_balance(df=starknet_df, chain="Starknet")
    st.dataframe(data=starknet_df, use_container_width=True)
    st.write(
        f"""
        # Total balance ${round(sum(starknet_df['amount in USDT'], 2))}
        """
    )
