import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def read_minimax_vs_random_data() -> DataFrame:
    dfs: list[DataFrame] = []
    for depth in range(1, 7):
        df = pd.read_csv(
            f"data/minimax_vs_random/minimax_vs_random_depth_{depth}_minimax_first-True.csv",
            index_col=0,
        )
        df["depth"] = depth
        dfs.append(df)
    return pd.concat(dfs)


def main():
    df: DataFrame = read_minimax_vs_random_data()
    print(df.describe())


if __name__ == "__main__":
    main()
