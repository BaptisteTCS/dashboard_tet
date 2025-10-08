import pandas as pd
from pandas import Timedelta
import plotly.graph_objects as go


def compute_totals_by_period(
    df: pd.DataFrame,
    date_col: str,
    group_col: str | bool = False,
    time_granularity: str = 'M',
    min_date: str = '2024-01-01',
    cumulatif: bool = True
) -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
    df['periode'] = df[date_col].dt.to_period(time_granularity).dt.to_timestamp()
    df = df[df['periode'] >= pd.to_datetime(min_date)]

    if group_col:
        grouped = df.groupby(['periode', group_col]).size().unstack(fill_value=0)
    else:
        grouped = df.groupby('periode').size().to_frame('Total')

    data = grouped.cumsum() if cumulatif else grouped
    cols_to_sum = [col for col in data.columns if col not in ['periode', 'Total']]
    if cols_to_sum:  # éviter erreur si déjà 'Total' unique
        data['Total'] = data[cols_to_sum].sum(axis=1)
    return data.reset_index()


def date_to_month(df_totals: pd.DataFrame) -> pd.DataFrame:
    if len(df_totals.periode) > 1:
        if (df_totals.periode.iloc[1] - df_totals.periode.iloc[0]) > Timedelta(days=15):
            df_totals['periode'] = df_totals.apply(lambda x: x['periode'].strftime('%B'), axis=1)
            return df_totals
        else:
            df_totals['periode'] = df_totals.apply(lambda x: x['periode'].date(), axis=1)
    return df_totals


def display_totals_table(df_totals: pd.DataFrame):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_totals.columns),
                    fill_color='#f2f2f2',
                    align='left',
                    font=dict(color='black', size=12)),
        cells=dict(values=[df_totals[col] for col in df_totals.columns],
                   fill_color='white',
                   align='left',
                   font=dict(color='black', size=11))
    )])
    fig.update_layout(width=1400, height=600, margin=dict(t=10))
    return fig


