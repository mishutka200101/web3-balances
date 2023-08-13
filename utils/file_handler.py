import pandas as pd


def read_excel(filename: str):
    df = pd.ExcelFile(filename, engine='openpyxl')
    return df


def write_to_excel(df, filename: str):
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer)
