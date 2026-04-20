import pandas as pd
import matplotlib.pyplot as plt


def main():
    bad_minimax_df = pd.read_csv("data/max_vs_random_depth_4.csv")
    good_minimax_df = pd.read_csv("data/minimax_vs_random_depth_4_minimax_first-True.csv")
    random_df = pd.read_csv("data/random_vs_random.csv")
    combined_df = pd.concat([bad_minimax_df,good_minimax_df, random_df], keys=("bad minimax","good minimax", "random"), names=["algorithm"])

    print(combined_df)
    # minimax_df["score"].hist(alpha=0.5, label="Minimax", density=True)
    # random_df["score"].hist(alpha=0.5, label="Random", density=True)
    combined_df.boxplot(column="score", by="algorithm")

    plt.show()
    


if __name__ == "__main__":
    main()
