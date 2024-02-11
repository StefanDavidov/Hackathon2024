import pandas as pd
import numpy

if __name__ == "__main__":
    with open("../data/data.csv") as f:
        df = pd.read_csv(f)

    df = df.drop(["High", "Close", "Low", "Adj Close", "Security", "News - All News Volume", "Date"], axis=1)
    companies = ["INTC", "MSFT", "GOOGL", "AIZ", "DE", "AMZN", "AAPL", "TSLA", "NVDA"]

    drop_cols = [val for val in df.Symbol.unique() if val not in companies]

    df.drop(df[df["Symbol"].isin(drop_cols)].index, inplace=True)
    symbol_groups = df.groupby(df.Symbol)
    companies = df.Symbol.unique()
    new_df = pd.DataFrame()
    #Sector, Subindustry, Symbol
    for company in companies:
        symbol_frame = symbol_groups.get_group(company)
        symbol_frame_open = symbol_frame.Open
        last_col = [(symbol_frame_open.iloc[i+20] - symbol_frame_open.iloc[i])/symbol_frame_open.iloc[i] for i in range(0,symbol_frame_open.shape[0]-20)]
        ins_frame = symbol_frame.copy()
        ins_frame.drop(ins_frame.tail(20).index, inplace=True)
        ins_frame["y"] = last_col
        ins_frame = ins_frame.iloc[1:,:]
        new_df = pd.concat([new_df, ins_frame])
        print(company)
        print(new_df.shape)

    new_df = new_df.drop("GICS Sector", axis=1)
    new_df = new_df.drop("GICS Sub-Industry", axis=1)

    #new_df = new_df.drop("Symbol", axis=1)
    new_df.to_csv("../data/edited_data.csv")





