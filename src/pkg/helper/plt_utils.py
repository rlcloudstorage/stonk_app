"""
src/pkg/helper/plt_utils.py
---------------------------
Some misc. Matplotlib helper functions

Functions:
-   heatmap_plot_correlated_dataframe():
-   line_plot_all_columns_from_dataframe():
-   line_plot_shifted_column_vs_col_list_timeseries():
-   plot_savgol_filter_compare_alt_window_size():
"""
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pkg import config_obj
from pkg.helper.pd_utils import (
    correlate_dataframe_columns,
    shift_timeseries_dataframe_columns,
)


FIG_SIZE = (10, 7.5)
PLOT_DIR = "plot"

logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

work_dir = config_obj.get(section="config", option="work_dir")


def heatmap_plot_correlated_dataframe(dataframe: pd.DataFrame, col_list: list=[], period: int=3, show_plt: bool=False):
    """
    heatmap_plot_correlated_dataframe(dataframe, col_list, period, show_plt)
    ------------------------------------------------------------------------
    Create the correlation matrix of all columns in dataframe.

    :param dataframe: pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param col_list: columns NOT in `col_list` are shifted foward
        by the `period` value
    :type col_list: list
    :param period: optional number of periods to shift, default is `3`
    :type period: int
    :param show_plt: default is save to plot directory
    :type show_plt: bool
    """
    dataframe = shift_timeseries_dataframe_columns(dataframe=dataframe, col_list=col_list, period=period)

    # create pandas correlation matrix
    corr_df = correlate_dataframe_columns(dataframe=dataframe)

    # plot correlation matrix
    plt.figure(figsize=FIG_SIZE)
    sns.set_context("paper")
    sns.heatmap(
        data=corr_df, mask=np.triu(np.ones_like(corr_df, dtype=bool)),
        annot=True, fmt="d", vmax=100, vmin=-100, center=0, square=True,
        linewidths=0.5, cbar_kws={"shrink": 0.2}, cmap="coolwarm",
    ).set_title(
        f"Correlation - {period} Period Timeshift {(', '.join(col_list))}"
    )
    plt.show() if show_plt else plt.savefig(f"{work_dir}/{PLOT_DIR}/corr_{('_'.join(col_list))}_{period}.png")
    plt.close()


def line_plot_all_columns_from_dataframe(dataframe: pd.DataFrame, show_plt: bool=False):
    """plot dataframe"""

    plt.figure(figsize=FIG_SIZE)
    sns.set_context("paper")
    sns.lineplot(
        data=dataframe, palette="pastel", linewidth=2.5,
    ).set_title(f"{dataframe.name} Dataframe")

    plt.show() if show_plt else plt.savefig(f"{work_dir}/{PLOT_DIR}/{dataframe.name}.png")
    plt.close()


def line_plot_shifted_column_vs_col_list_timeseries(dataframe: pd.DataFrame, col_list: list, period: int=3, show_plt: bool=False):
    """create series of lineplots comparing timeseries"""
    dataframe = shift_timeseries_dataframe_columns(dataframe=dataframe, col_list=col_list, period=period)
    no_shift_df = dataframe[col_list].copy()
    total = len(dataframe.columns)- len(no_shift_df.columns)
    i = 0

    for col in dataframe.columns:
        if dataframe[col].name in col_list:
            continue
        i += 1
        plot_df = pd.concat(objs=[dataframe[col], no_shift_df], axis=1)

        # plot timeseries
        plt.figure(figsize=FIG_SIZE)
        sns.set_context("paper")
        sns.lineplot(
            data=plot_df, palette="pastel", linewidth=2.5,
        ).set_title(
            f"{period} Period Timeshift {dataframe[col].name} vs. {(', '.join(col_list))} ({i}/{total})"
        )
        plt.show() if show_plt else plt.savefig(f"{work_dir}/{PLOT_DIR}/shift_{dataframe[col].name}_{period}.png")
        plt.close()


def plot_savgol_filter_comparing_alternate_window_sizes(dataframe: pd.DataFrame, win_sz_list: list, polyorder: int, show_plt: bool=False):
    """"""
    from scipy.signal import savgol_filter

    for col in dataframe.columns:
        fig, axs = plt.subplots(ncols=2, nrows=2, figsize=FIG_SIZE)
        plt.xlabel("Date")
        plt.ylabel("Value")

        raw = pd.Series(data=dataframe[col], name=dataframe[col].name)

        for j, w in enumerate(win_sz_list):
            smooth = savgol_filter(x=raw, window_length=w, polyorder=polyorder, deriv=0)

            axs[0, j].plot(raw.index, raw, label=f"raw {dataframe.name} data")
            axs[0, j].plot(raw.index, smooth, label=f"smooth {dataframe.name} data")
            axs[0, j].legend()
            axs[0, j].set_title(f"{raw.name} - window {w}, polyorder {polyorder}")

        for j, w in enumerate(win_sz_list):
            slope = savgol_filter(x=raw, window_length=w, polyorder=polyorder, deriv=1)

            # axs[i+1, j].plot(raw.index, raw, label=f"raw {dataframe.name} data")
            axs[1, j].plot(raw.index, slope, label=f"smooth data slope")
            axs[1, j].legend()
            axs[1, j].set_title(f"{raw.name} - window {w}, polyorder {polyorder}")

        plt.tight_layout()
        plt.show() if show_plt else plt.savefig(f"{work_dir}/{PLOT_DIR}/savgol_{raw.name}_w{w}_p{polyorder}.png")
        plt.close()
