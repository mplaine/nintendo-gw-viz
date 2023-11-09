# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import datetime as dt
import pathlib
from typing import Union

# Third-party modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__email__ = "markku.laine@gmail.com"


# ----------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------

# Define colors
series_colors_dict = {
    "Silver": {"label_color": "#C0C0C0", "text_color": "#FFFFFF"},
    "Gold": {"label_color": "#FFD700", "text_color": "#131515"},
    "Wide Screen": {"label_color": "#D7CA7C", "text_color": "#46422C"},
    "Multi Screen": {"label_color": "#FF5F00", "text_color": "#FFFFFF"},
    "New Wide Screen": {"label_color": "#3C7E72", "text_color": "#FFFFFF"},
    "Table Top": {"label_color": "#FFFAC8", "text_color": "#6E4931"},
    "Panorama Screen": {"label_color": "#BA46DC", "text_color": "#FFFFFF"},
    "Super Color": {"label_color": "#000000", "text_color": "#FFFFFF"},
    "Micro VS. System": {"label_color": "#E6194B", "text_color": "#FFFFFF"},
    "Crystal Screen": {"label_color": "#275A76", "text_color": "#FFFFFF"},
    "Special Edition": {"label_color": "#FFE119", "text_color": "#131515"},
    "Reissue": {"label_color": "#B73E38", "text_color": "#FFFFFF"},
    "Colour Screen": {"label_color": "#3CB44B", "text_color": "#FFFFFF"},
}
series_label_colors_dict = {k: v["label_color"] for k, v in series_colors_dict.items()}
series_text_colors_dict = {k: v["text_color"] for k, v in series_colors_dict.items()}


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def generate_timeline_levels(series: pd.Series) -> list[int]:
    """
    Generates levels for a timeline automatically.

    Args:
        series (pd.Series): The Series containing series names.

    Returns:
        list[int]: A list of integers representing positive and negative levels for a timeline.
    """
    series_side_dict = {}
    positive_level = 2
    negative_level = -2
    next_coef = 1
    threshold_level = 16
    levels = []
    for s in series:
        if s not in series_side_dict:
            series_side_dict[s] = next_coef
            next_coef *= -1
        c = series_side_dict[s]
        if c > 0:
            levels.append(positive_level)
            if positive_level == threshold_level:
                positive_level = 2
            else:
                positive_level += c
        elif c < 0:
            levels.append(negative_level)
            if negative_level == -threshold_level:
                negative_level = -3
            else:
                negative_level += c

    return levels


def get_timeline_levels(series: pd.Series) -> list[int]:
    """
    Gets manually assigned levels for a timeline.

    Args:
        series (pd.Series): The Series containing series names.

    Returns:
        list[int]: A list of integers representing positive and negative levels for a timeline.
    """
    # fmt: off
    levels = [
        2, 3, 4, 5, 6, -2, -3, -4, 8, 9,          # 1-10
        10, 11, 12, 13, 14, 15, 16, 17, -2, -3,   # 11-20
        2, -4, -5, -6, -7, 6, 7, 8, 3, -8,        # 21-30
        9, 4, 11, 12, 13, -9, 14, -10, -14, -15,  # 31-40
        15, -2, -3, 16, -4, -11, 5, -12, -7, -8,  # 41-50
        -9, -13, 13, -14, 6, 7, 8, -15, -16, 9,   # 51-60
        2, 2, 3,                                  # 61-63
    ]
    # fmt: on
    return levels[: len(series)]


def millions_formatter(value: int, pos) -> str:
    """
    Formats large numerical values to abbreviated strings.

    Args:
        value (int): The numerical tick value to be formatted.
        pos (int): The tick value position.

    Returns:
        str: Formatted string representing the value in abbreviated format.

    Examples:
        millions_formatter(1500000)  # Returns '1.5M'
        millions_formatter(2500)     # Returns '2500'
        millions_formatter(350000)    # Returns '350K'
    """
    if value >= 1e6:
        return f"{value * 1e-6:.1f}M"
    elif value >= 1e3:
        return f"{value * 1e-3:.0f}K"
    else:
        return f"{value}"


def visualize_games_produced(df: pd.DataFrame, max_release_year: Union[None, int] = None, save_figure: bool = True) -> None:
    """
    Creates a bar plot visualization showing the number of games produced for each game.

    Args:
        df (pd.DataFrame): The DataFrame containing the games data.
        max_release_year (int): The maximum release year for a game to be included (default: None).
        save_figure (bool): Save the figure (default: True).
    """
    # Create a plotting data frame
    plotting_df = df.copy()
    if max_release_year is not None:
        plotting_df = plotting_df[plotting_df["date of release"].dt.year <= max_release_year]

    # Add the "series color" column
    plotting_df["series color"] = plotting_df["series"].map(series_label_colors_dict)

    # Create a figure for the visualization
    fig, ax = plt.subplots(figsize=(15, 7))

    # Bar plot
    labels = [f"{game} ({model})" for game, model in zip(plotting_df["game"], plotting_df["model"])]
    sns.barplot(data=plotting_df, y="produced", x=labels, hue="series", palette=series_label_colors_dict)

    # Customize axes
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines[["bottom"]].set_color("#F0F0F0")
    ax.tick_params(axis="x", which="both", bottom=False, top=False, labelsize=8, rotation=90)
    ax.tick_params(axis="y", which="both", left=False, right=False, labelsize=8)
    ax.set_ylim(0, plotting_df["produced"].max() + 200000)
    ax.yaxis.grid(color="#F0F0F0")
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    plt.xlabel("Game", labelpad=10)
    plt.ylabel("Quantity", labelpad=10)

    # Add title and legend
    ax.set_title(
        "Number of Nintendo Game & Watch Games Produced per Game", fontsize=20, pad=20, fontweight="normal", loc="left"
    )
    ax.legend(
        # series_colors_dict.keys(),
        borderpad=2,
        loc="upper right",
        bbox_to_anchor=(0.85, 0.95),
        title="Series",
        title_fontsize="large",
        alignment="left",
    )

    # Save figure
    if save_figure:
        games_produced_filepath = pathlib.Path("figures/nintendo_game_and_watch_games_produced.png")
        plt.savefig(games_produced_filepath, bbox_inches="tight", pad_inches=0.5, dpi=72)

    # Show figure
    plt.show()


def visualize_games_released(df: pd.DataFrame, max_release_year: Union[None, int] = None, save_figure: bool = True) -> None:
    """
    Creates a bar plot visualization showing the number of games released per year.

    Args:
        df (pd.DataFrame): The DataFrame containing the games released data.
        max_release_year (int): The maximum release year for a game to be included (default: None).
        save_figure (bool): Save the figure (default: True).
    """
    # Create a plotting data frame
    plotting_df = df.copy()
    if max_release_year is not None:
        plotting_df = plotting_df[plotting_df["year"] <= max_release_year]

    # Create a figure for the visualization
    fig, ax = plt.subplots(figsize=(8, 4))

    # Bar plot
    sns.barplot(data=plotting_df, y="games", x="year")

    # Customize axes
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines[["bottom"]].set_color("#F0F0F0")
    ax.tick_params(axis="x", which="both", bottom=False, top=False, labelsize=8)
    ax.tick_params(axis="y", which="both", left=False, right=False, labelsize=8)
    ax.set_ylim(0, plotting_df["games"].max() + 1)
    ax.yaxis.grid(color="#F0F0F0")
    ax.set_axisbelow(True)
    plt.xlabel("Year", labelpad=10)
    plt.ylabel("Quantity", labelpad=10)

    # Add title
    plt.title("Number of Nintendo Game & Watch Games Released per Year", pad=20, fontsize=14, loc="left")

    # Save figure
    if save_figure:
        games_released_filepath = pathlib.Path("figures/nintendo_game_and_watch_games_released.png")
        plt.savefig(games_released_filepath, bbox_inches="tight", pad_inches=0.5, dpi=72)

    # Show figure
    plt.show()


def visualize_outliers(df: pd.DataFrame, column_name: str) -> None:
    """
    Creates histogram and box plot visualizations showing the distribution and outliers of a specific column in
    a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        column_name (str): The name of the column in the DataFrame for which to generate plots.
    """
    # Create a plotting data frame
    plotting_df = df.copy()

    # Create a figure for the visualizations
    fig, ax = plt.subplots(1, 2, figsize=(10, 3))

    # Histogram
    sns.histplot(ax=ax[0], data=plotting_df, x=column_name)
    ax[0].set_xlabel(column_name)
    ax[0].set_title(f"Histogram of '{column_name}'")

    # Box plot
    sns.boxplot(ax=ax[1], data=plotting_df, x=column_name, fliersize=2)
    plt.xlabel(column_name)
    plt.title(f"Box plot of '{column_name}'")

    plt.show()


def visualize_series_released(df: pd.DataFrame, max_release_year: Union[None, int] = None, save_figure: bool = True) -> None:
    """
    Creates a bar plot visualization showing the number of games released for each series.

    Args:
        df (pd.DataFrame): The DataFrame containing the series data.
        max_release_year (int): The maximum release year for a game to be included (default: None).
        save_figure (bool): Save the figure (default: True).
    """
    # Create a plotting data frame
    plotting_df = df.copy()
    if max_release_year is not None:
        plotting_df = plotting_df[plotting_df["from"] <= max_release_year]

    # Create a figure for the visualization
    fig, ax = plt.subplots(figsize=(8, 4))

    # Bar plot
    sns.barplot(data=plotting_df, y="games", x="series", hue="series", palette=series_label_colors_dict)

    # Customize axes
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines[["bottom"]].set_color("#F0F0F0")
    ax.tick_params(axis="x", which="both", bottom=False, top=False, labelsize=8, rotation=90)
    ax.tick_params(axis="y", which="both", left=False, right=False, labelsize=8)
    ax.set_ylim(0, plotting_df["games"].max() + 1)
    ax.yaxis.grid(color="#F0F0F0")
    ax.set_axisbelow(True)
    plt.xlabel("Series", labelpad=10)
    plt.ylabel("Quantity", labelpad=10)

    # Add title
    plt.title("Number of Nintendo Game & Watch Games Released per Series", pad=20, fontsize=14, loc="left")

    # Save figure
    if save_figure:
        series_released_filepath = pathlib.Path("figures/nintendo_game_and_watch_series_released.png")
        plt.savefig(series_released_filepath, bbox_inches="tight", pad_inches=0.5, dpi=72)

    # Show figure
    plt.show()


def visualize_timeline(
    df: pd.DataFrame, max_release_year: Union[None, int] = None, auto_levels: bool = True, save_figure: bool = True
) -> None:
    """
    Creates a timeline visualization showing the evolution of Nintendo Game & Watch.

    Args:
        df (pd.DataFrame): The DataFrame containing the games data.
        max_release_year (int): The maximum release year for a game to be included (default: None).
        auto_levels (bool): Use automatically generated levels for the timeline (default: True).
        save_figure (bool): Save the figure (default: True).
    """
    # Create a plotting data frame
    plotting_df = df.copy()
    if max_release_year is not None:
        plotting_df = plotting_df[plotting_df["date of release"].dt.year <= max_release_year]

    # Add the "level" column
    if auto_levels:
        plotting_df["level"] = generate_timeline_levels(plotting_df["series"])
    else:
        plotting_df["level"] = get_timeline_levels(plotting_df["series"])

    # Add the "label color" and "text color" columns
    plotting_df["label color"] = plotting_df["series"].map(series_label_colors_dict)
    plotting_df["text color"] = plotting_df["series"].map(series_text_colors_dict)

    # Create a figure for the visualization
    fig, ax = plt.subplots(figsize=(25, 15))

    # Customize axes
    min_year = plotting_df["date of release"].min().year
    max_year = plotting_df["date of release"].max().year
    min_date = dt.date(min_year, 1, 1)
    max_date = dt.date(max_year + 1, 1, 1)
    ax.set_xticks(
        ticks=pd.date_range(min_date, max_date, freq="ys"),
        labels=range(min_year, max_year + 2),
        rotation="horizontal",
        ha="center",
    )
    ax.set_ylim(plotting_df["level"].min(), plotting_df["level"].max())
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines[["bottom"]].set_position(("axes", 0.5))
    ax.spines[["bottom"]].set_color("black")
    ax.spines[["bottom"]].set_linewidth(2)
    ax.spines[["bottom"]].set_zorder(1)
    ax.tick_params(axis="x", colors="black", labelsize=12, which="major", width=2)
    for label in plt.gca().get_xticklabels():
        label.set_fontweight("medium")
    ax.yaxis.set_visible(False)

    # Create timeline markers
    # fmt: off
    ax.plot_date(
        plotting_df["date of release"],
        [0,] * len(plotting_df),
        fmt="o",
        color="#BBBBBB",
        fillstyle="full",
        markersize=7,
        markerfacecolor="white",
        zorder=2,
    )
    # fmt: on

    # Include the games data
    for i in range(len(plotting_df)):
        release_order = plotting_df.loc[i, "release order"]
        game = plotting_df.loc[i, "game"]
        series = plotting_df.loc[i, "series"]
        model = plotting_df.loc[i, "model"]
        released = plotting_df.loc[i, "date of release"]
        level = plotting_df.loc[i, "level"]
        label_color = plotting_df.loc[i, "label color"]
        text_color = plotting_df.loc[i, "text color"]
        text = f"#{release_order} {game} ({model})"  # ({released.strftime('%B %d, %Y')})"

        # Draw line
        plt.plot(
            [released, released],
            [0, level],
            marker=None,
            color="#BBBBBB",
            linestyle="solid",
            label=series,
            linewidth=1.0,
            zorder=0,
        )

        # Draw text
        t = ax.text(x=released, y=level, s=text, color=text_color, ha="left", zorder=2)
        t.set_bbox(dict(facecolor=label_color, edgecolor=label_color, alpha=1.0))

    # Add title and legend
    ax.set_title(
        "Timeless Classics: The Evolution of Nintendo Game & Watch", fontsize=30, pad=60, fontweight="normal", loc="center"
    )
    legend_colors = [v["label_color"] for v in series_colors_dict.values()]
    legend_lines = [Line2D([0], [0], color=lc, lw=10) for lc in legend_colors]
    ax.legend(
        legend_lines,
        series_colors_dict.keys(),
        borderpad=2,
        loc="lower right",
        bbox_to_anchor=(1, 0.1),
        title="Series",
        title_fontsize="large",
        alignment="left",
    )

    # Add copyright text
    copyright_text = f"\u00A9 {dt.datetime.now().year} Markku Laine"
    ax.text(
        x=1.0,
        y=0.0,
        s=copyright_text,
        color="black",
        ha="right",
        va="bottom",
        transform=plt.gca().transAxes,
        fontsize=10,
        zorder=2,
    )

    # Save figure
    if save_figure:
        timeline_filepath = pathlib.Path("figures/nintendo_game_and_watch_timeline.png")
        plt.savefig(timeline_filepath, bbox_inches="tight", pad_inches=1, dpi=72)

    # Show figure
    plt.show()
