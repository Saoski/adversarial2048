import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame


def read_minimax_vs_random_data() -> DataFrame:
    dfs: list[DataFrame] = []
    for depth in range(1, 6):
        path = f"../data/minimax_vs_random_depth_{depth}_simulations_500.csv"
        df = pd.read_csv(
            path,
            index_col=0,
        )
        df["depth"] = depth
        dfs.append(df)
    return pd.concat(dfs)


def read_minimax_vs_adversary_data() -> DataFrame:
    dfs: list[DataFrame] = []
    depth = 5
    rollout = 20
    monte_carlo_depth = 12
    simulations = 500

    # Minimax vs random
    path = f"../data/minimax_vs_random_depth_{depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "random"
    dfs.append(df)

    # Minimax vs minimax
    path = f"../data/minimax_vs_minimax_depth_{depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "minimax"
    dfs.append(df)

    # Minimax vs expectimax
    path = f"../data/minimax_vs_expectimax_depth_{depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "expectimax"
    dfs.append(df)

    # Minimax vs monte carlo
    path = f"../data/minimax_vs_monte_carlo_minimax_depth_{depth}_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "monte_carlo"
    df["monte_carlo_depth"] = monte_carlo_depth
    df["rollout"] = rollout
    dfs.append(df)

    big_df = pd.concat(dfs)
    big_df["depth"] = depth
    return big_df

def read_monte_carlo_vs_adversary_data() -> DataFrame:
    dfs: list[DataFrame] = []
    depth = 5
    rollout = 20
    monte_carlo_depth = 12
    simulations = 500

    # Monte-carlo vs Minimax
    path = f"../data/monte_carlo_vs_minimax_minimax_depth_{depth}_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "minimax"
    df["monte_carlo_depth"] = monte_carlo_depth
    df["rollout"] = rollout

    dfs.append(df)

    # Monte-carlo vs Expectimax
    path = f"../data/monte_carlo_vs_expectimax_rollout_{rollout}_expectimax_depth_{depth}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["adversary"] = "minimax"
    df["monte_carlo_depth"] = monte_carlo_depth
    df["rollout"] = rollout

    dfs.append(df)

    return pd.concat(dfs)


def read_monte_carlo_vs_random_data() -> DataFrame:
    rollout = 20
    monte_carlo_depth = 12
    simulations = 500
    path = f"../data/monte_carlo_vs_random_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulations}.csv"
    df = pd.read_csv(
        path,
        index_col=0,
    )
    df["monte_carlo_depth"] = monte_carlo_depth
    df["rollout"] = rollout
    return df


def make_cat_plots(
    data: DataFrame, x: str, y: str, title: str, linestyles: str = "-", ci: float = 90
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Point plot with confidence interval
    sns.pointplot(
        data=data, x=x, y=y, ax=axes[0], errorbar=("ci", ci), linestyles=linestyles
    )
    axes[0].set_title(f"{ci}% Confidence Interval")

    # Box plot
    sns.boxplot(data=data, x=x, y=y, ax=axes[1])
    axes[1].set_title("Box Plot")

    # Violin plot
    sns.violinplot(data=data, x=x, y=y, ax=axes[2])
    axes[2].set_title("Violin Plot")

    fig.suptitle(title, fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()


def main():
    df: DataFrame = read_minimax_vs_random_data()
    print(df.describe())


if __name__ == "__main__":
    main()
