import pandas as pd
import matplotlib.pyplot as plt


def main():
    minimax_df = pd.read_csv("data/max_vs_random_depth_4.csv")
    random_df = pd.read_csv("data/random_play.csv")
    combined_df = pd.concat([minimax_df, random_df], keys=("minimax", "random"), names=["algorithm"])

    print(combined_df)
    # minimax_df["score"].hist(alpha=0.5, label="Minimax", density=True)
    # random_df["score"].hist(alpha=0.5, label="Random", density=True)
    combined_df.boxplot(column="score", by="algorithm")

    plt.show()
    


if __name__ == "__main__":
    main()
