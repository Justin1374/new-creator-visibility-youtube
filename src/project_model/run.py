import os
import matplotlib.pyplot as plt
import pandas as pd
from model import RecommendationModel


def run_single_condition(weight, condition_name, steps=50, seed=42):
    """Runs a deterministic 50-round simulation for a single popularity weight and exports raw CSV."""
    model = RecommendationModel(weight=weight, seed=seed)
    for _ in range(steps):
        model.step()

    data = model.datacollector.get_model_vars_dataframe()
    csv_filename = f"outputs/del03_{condition_name}_raw_visibility_by_round.csv"
    data.to_csv(csv_filename, index_label="Round")
    print(f"Saved raw trace: {csv_filename}")
    return data


def run_multiseed_sweep(weights=(0.10, 0.90), seeds=range(20), steps=50):
    """Runs a 20-seed robustness sweep across both conditions and exports summary metrics."""
    rows = []
    for weight in weights:
        condition = "baseline" if weight == 0.10 else "alternative"
        for seed in seeds:
            model = RecommendationModel(weight=weight, seed=seed)
            for _ in range(steps):
                model.step()
            df = model.datacollector.get_model_vars_dataframe()
            unique_new = sum(1 for c in model.creator_agents if c.is_new_creator and c.total_impressions > 0)
            unique_est = sum(1 for c in model.creator_agents if not c.is_new_creator and c.total_impressions > 0)
            rows.append({
                "Condition": condition,
                "Popularity_Weight": weight,
                "Seed": seed,
                "Mean_Percent_New_Creators": round(df["Percent_New_Creators_Recommended"].mean(), 4),
                "Mean_Topic_Match_Rate": round(df["Topic_Match_Rate"].mean(), 4),
                "Mean_Engagement_Rate": round(df["Engagement_Rate"].mean(), 4),
                "Final_Mean_New_Popularity": round(df["Mean_New_Creator_Popularity"].iloc[-1], 4),
                "Final_Mean_Est_Popularity": round(df["Mean_Est_Creator_Popularity"].iloc[-1], 4),
                "Unique_New_Creators_Exposed_of_50": unique_new,
                "Unique_Est_Creators_Exposed_of_50": unique_est,
            })

    summary_df = pd.DataFrame(rows)
    summary_csv = "outputs/del03_multiseed_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"Saved multi-seed summary: {summary_csv}")
    return summary_df


def plot_trajectory_comparison(base_df, alt_df):
    """Generates side-by-side trajectory comparison across rounds (seed=42)."""
    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7.5), sharex=True)

    # Panel A: New Creator Slot Share (%)
    axes[0].plot(
        base_df.index,
        base_df["Percent_New_Creators_Recommended"],
        label=f"Baseline (w_pop = 0.10) | Mean: {base_df['Percent_New_Creators_Recommended'].mean():.1f}%",
        color="#1f77b4",
        linewidth=2.0,
    )
    axes[0].plot(
        alt_df.index,
        alt_df["Percent_New_Creators_Recommended"],
        label=f"Alternative (w_pop = 0.90) | Mean: {alt_df['Percent_New_Creators_Recommended'].mean():.1f}%",
        color="#d62728",
        linewidth=2.0,
        linestyle="--",
    )
    axes[0].set_title(
        "DEL03 Baseline vs. Alternative: New Creator Slot Share & Viewer Engagement (Seed = 42)",
        fontsize=12,
        fontweight="bold",
    )
    axes[0].set_ylabel("New Creator Slots (%)")
    axes[0].set_ylim(-3, 100)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(loc="upper right")

    # Panel B: Realized Engagement Rate (%)
    axes[1].plot(
        base_df.index,
        base_df["Engagement_Rate"],
        label=f"Baseline Engagement Rate | Mean: {base_df['Engagement_Rate'].mean():.1f}%",
        color="#2ca02c",
        linewidth=1.8,
    )
    axes[1].plot(
        alt_df.index,
        alt_df["Engagement_Rate"],
        label=f"Alternative Engagement Rate | Mean: {alt_df['Engagement_Rate'].mean():.1f}%",
        color="#ff7f0e",
        linewidth=1.8,
        linestyle="--",
    )
    axes[1].set_xlabel("Recommendation Round (0-49)")
    axes[1].set_ylabel("Realized Engagement Rate (%)")
    axes[1].set_ylim(-3, 105)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(loc="upper right")

    plt.tight_layout()
    out_png = "outputs/del03_comparison_visibility_by_round.png"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved comparison trajectory figure: {out_png}")


def plot_multiseed_comparison(summary_df):
    """Generates a grouped bar chart with SD error bars across 20 seeds."""
    metrics = [
        ("Mean_Percent_New_Creators", "New Creator Slot Share (%)"),
        ("Mean_Topic_Match_Rate", "Viewer Topic Match Rate (%)"),
        ("Mean_Engagement_Rate", "Realized Engagement Rate (%)"),
    ]
    base_sub = summary_df[summary_df["Condition"] == "baseline"]
    alt_sub = summary_df[summary_df["Condition"] == "alternative"]

    base_means = [base_sub[m[0]].mean() for m in metrics]
    base_stds = [base_sub[m[0]].std() for m in metrics]
    alt_means = [alt_sub[m[0]].mean() for m in metrics]
    alt_stds = [alt_sub[m[0]].std() for m in metrics]

    x = range(len(metrics))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    bars1 = ax.bar(
        [i - width / 2 for i in x],
        base_means,
        width,
        yerr=base_stds,
        capsize=5,
        label="Baseline: Interest-Prioritized (w_pop = 0.10)",
        color="#1f77b4",
        edgecolor="black",
        linewidth=0.7,
    )
    bars2 = ax.bar(
        [i + width / 2 for i in x],
        alt_means,
        width,
        yerr=alt_stds,
        capsize=5,
        label="Alternative: Popularity-Prioritized (w_pop = 0.90)",
        color="#d62728",
        edgecolor="black",
        linewidth=0.7,
    )

    for bar in bars1:
        h = bar.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, h + 2.5),
            ha="center",
            fontsize=9.5,
            fontweight="bold",
        )
    for bar in bars2:
        h = bar.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, h + 2.5),
            ha="center",
            fontsize=9.5,
            fontweight="bold",
        )

    ax.set_title("DEL03 Multi-Seed Comparison Across 20 Runs (Mean +/- 1 SD)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Mean Percentage Across 50 Rounds (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels([m[1] for m in metrics], fontsize=10.5)
    ax.set_ylim(0, 115)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")

    plt.tight_layout()
    out_png = "outputs/del03_comparison_summary_distribution.png"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved multi-seed summary figure: {out_png}")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    print("Running DEL03 Baseline Condition (w_pop = 0.10, seed = 42)...")
    base_df = run_single_condition(weight=0.10, condition_name="baseline", steps=50, seed=42)

    print("Running DEL03 Alternative Condition (w_pop = 0.90, seed = 42)...")
    alt_df = run_single_condition(weight=0.90, condition_name="alternative", steps=50, seed=42)

    print("Running DEL03 20-Seed Robustness Sweep (seeds 0..19)...")
    summary_df = run_multiseed_sweep(weights=(0.10, 0.90), seeds=range(20), steps=50)

    plot_trajectory_comparison(base_df, alt_df)
    plot_multiseed_comparison(summary_df)
    print("DEL03 simulation and visualization complete.")