import pytest
import pandas as pd

from pkg.helper import plt_utils


col_list = ['CCC', 'DDD']


@pytest.fixture(scope="package")
def input_df():
    """"""
    input_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00'), pd.Timestamp('0001-01-04 04:00:00')],
        'columns': ['AAA', 'BBB', 'CCC', 'DDD'],
        'data': [(4253, 2881, 430, 18741), (4290, 2942, 436, 18873), (4158, 2855, 427, 18499), (4204, 2909, 434, 18604)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    input_df = pd.DataFrame.from_dict(data=input_dict, orient="tight")
    input_df.name = "input_df"

    # print(f"\n*** input_df:\n{input_df}")
    return input_df


@pytest.mark.skip("42")
def test_heatmap_plot_correlated_dataframe(input_df):
    """"""
    # plt_utils.heatmap_plot_correlated_dataframe(dataframe=input_df, col_list=col_list, period=1)
    plt_utils.heatmap_plot_correlated_dataframe(dataframe=input_df, col_list=col_list, period=1, show_plt=True)


@pytest.mark.skip("42")
def test_line_plot_all_columns_from_dataframe(input_df):
    """"""
    # plt_utils.line_plot_all_columns_from_dataframe(dataframe=input_df)
    plt_utils.line_plot_all_columns_from_dataframe(dataframe=input_df, show_plt=True)


@pytest.mark.skip("42")
def test_line_plot_shifted_column_vs_col_list_timeseries(input_df):
    """"""
    plt_utils.line_plot_shifted_column_vs_col_list_timeseries(dataframe=input_df, col_list=col_list, period=1)
    # plt_utils.line_plot_shifted_column_vs_col_list_timeseries(dataframe=input_df, col_list=col_list, period=1, show_plt=True)


@pytest.mark.skip("42")
def test_plot_savgol_filter_comparing_alternate_window_sizes(input_df):
    """"""
    win_sz_list = [2, 3]
    polyorder = 1
    # plt_utils.plot_savgol_filter_comparing_alternate_window_sizes(dataframe=input_df, win_sz_list=win_sz_list, polyorder=polyorder)
    plt_utils.plot_savgol_filter_comparing_alternate_window_sizes(dataframe=input_df, win_sz_list=win_sz_list, polyorder=polyorder, show_plt=True)
