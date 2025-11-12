import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def radar_spider_graph_plotly_with_comparison(row: pd.Series, row_precedente: pd.Series, diff: float | None = None):
    categories = [
        'Pilotabilité des FA',
        'Indicateurs',
        'Objectifs',
        'Lien référentiel',
        'Avancement',
        'Budget'
    ]

    values = [
        row['score_pilotabilite'],
        row['score_indicateur'],
        row['score_objectif'],
        row['score_referentiel'],
        row['score_avancement'],
        row['score_budget']
    ]

    previous_values = [
        row_precedente['score_pilotabilite'],
        row_precedente['score_indicateur'],
        row_precedente['score_objectif'],
        row_precedente['score_referentiel'],
        row_precedente['score_avancement'],
        row_precedente['score_budget']
    ]

    if row.get('c_referentiel', 1) == 0:
        index = categories.index('Lien référentiel')
        for lst in (categories, values, previous_values):
            del lst[index]

    categories += [categories[0]]
    values += [values[0]]
    previous_values += [previous_values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Semaine actuelle',
        line=dict(color='#ffc121'),
        fillcolor='#ffefbc'
    ))

    fig.add_trace(go.Scatterpolar(
        r=previous_values,
        theta=categories,
        fill='none',
        name='Semaine précédente',
        line=dict(color='gray', dash='dash')
    ))

    fig.update_layout(
        width=700,
        height=600,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                angle=90,
                tickangle=0
            ),
            angularaxis=dict(
                direction='clockwise',
                rotation=90
            )
        ),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        title=""
    )

    return fig


def prepare_line_data_nivo(
    df: pd.DataFrame,
    date_col: str,
    group_col: str | bool = False,
    time_granularity: str = 'M',
    min_date: str = "2024-01-01",
    colors: list[str] | None = None,
    cumulatif: bool = True,
    use_values_col: str | None = None
):
    """
    Prépare les données au format Nivo pour un graphique Line.
    
    Returns:
        tuple: (data, color_scheme, totaux, objectif_value)
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
    df['periode'] = df[date_col].dt.to_period(time_granularity).dt.to_timestamp()

    if group_col:
        if use_values_col:
            grouped = df.groupby(['periode', group_col])[use_values_col].sum().unstack(fill_value=0)
        else:
            grouped = df.groupby(['periode', group_col]).size().unstack(fill_value=0)
        total_by_type = grouped.sum().sort_values(ascending=False)
        grouped = grouped[total_by_type.index]
    else:
        if use_values_col:
            grouped = df.groupby('periode')[use_values_col].sum().to_frame('Total')
        else:
            grouped = df.groupby('periode').size().to_frame('Total')

    data_to_plot = grouped.cumsum() if cumulatif else grouped
    data_to_plot = data_to_plot[data_to_plot.index >= pd.to_datetime(min_date)]

    # Calculer les totaux pour l'affichage
    totaux = data_to_plot.sum(axis=1).reset_index()
    totaux.columns = ['periode', 'total']
    
    # Préparer les données au format Nivo
    nivo_data = []
    
    for col in data_to_plot.columns:
        serie_data = []
        for idx, row in data_to_plot.iterrows():
            if time_granularity == 'M':
                x_label = idx.strftime('%b %Y')
            elif time_granularity == 'W':
                x_label = idx.strftime('%d/%m/%y')
            else:
                x_label = str(idx)
            
            serie_data.append({
                "x": x_label,
                "y": float(row[col])
            })
        
        nivo_data.append({
            "id": str(col),
            "data": serie_data
        })
    
    # Déterminer les couleurs
    if group_col:
        group_list = set(df[group_col].unique())
        if group_list == {'actif', 'inactif'}:
            color_scheme = ["#A4E7C7", "#FFD0BB"]
        else:
            if colors is None:
                if df[group_col].nunique() < 6:
                    color_scheme = ["#A4E7C7", "#FFD0BB", "#F7C59F", "#7C77B9", "#92B4EC"]
                else:
                    color_scheme = [
                        "#E1E1FD", "#96C7DA", "#D9D9D9", "#E4CDEE", "#FEF1D8",
                        "#F7B1C2", "#A4E7C7", "#FFD0BB", "#C3C3FB", "#EEEEEE",
                        "#FFB595", "#D8EEFE", "#FBE7B5", "#B8D6F7"
                    ]
            else:
                color_scheme = colors
    else:
        color_scheme = ["#A4E7C7"]
    
    return nivo_data, color_scheme, totaux


def prepare_radar_data_nivo(row: pd.Series, row_precedente: pd.Series):
    """
    Prépare les données au format Nivo pour un graphique radar avec comparaison.
    
    Args:
        row: Série pandas avec les scores de la semaine actuelle
        row_precedente: Série pandas avec les scores de la semaine précédente
        
    Returns:
        Liste de dictionnaires au format attendu par Nivo Radar
    """
    categories = [
        'Pilotabilité',
        'Indicateurs',
        'Objectifs',
        'Référentiel',
        'Avancement',
        'Budget'
    ]
    
    keys = [
        'score_pilotabilite',
        'score_indicateur',
        'score_objectif',
        'score_referentiel',
        'score_avancement',
        'score_budget'
    ]
    
    # Préparer les données au format Nivo
    data = []
    for cat, key in zip(categories, keys):
        # Vérifier si le référentiel doit être exclu
        if key == 'score_referentiel' and row.get('c_referentiel', 1) == 0:
            continue
            
        data.append({
            "taste": cat,
            "Actuelle": round(float(row[key]), 2),
            "Précédente": round(float(row_precedente[key]), 2)
        })
    
    return data


def radar_spider_graph_plotly(row: pd.Series):
    categories = [
        'Pilotabilité des FA',
        'Indicateurs',
        'Objectifs',
        'Lien référentiel',
        'Avancement',
        'Budget'
    ]
    values = [
        row['score_pilotabilite'],
        row['score_indicateur'],
        row['score_objectif'],
        row['score_referentiel'],
        row['score_avancement'],
        row['score_budget']
    ]

    if row.get('c_referentiel', 1) == 0:
        index = categories.index('Lien référentiel')
        del categories[index]
        del values[index]

    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=row.get('nom_ct', 'Collectivité'),
        line=dict(color='#ffc121'),
        fillcolor='#ffefbc'
    ))

    fig.update_layout(
        width=700,
        height=600,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                angle=90,
                tickangle=0
            ),
            angularaxis=dict(
                direction='clockwise',
                rotation=90
            )
        ),
        showlegend=False,
        title=f"Score : {round(row.get('score', np.mean(values[:-1])), 2)} / 5"
    )

    return fig


def plot_area_with_totals(
    df: pd.DataFrame,
    date_col: str,
    group_col: str | bool = False,
    time_granularity: str = 'M',
    legend_title: str = "",
    min_date: str = "2024-01-01",
    colors: list[str] | None = None,
    cumulatif: bool = True,
    x_title: str = "",
    y_title: str = "",
    values_graph: bool = True,
    objectif: float | None = None,
    title: str = "",
    use_values_col: str | None = None
):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
    df['periode'] = df[date_col].dt.to_period(time_granularity).dt.to_timestamp()

    if group_col:
        if use_values_col:
            # Cas où les valeurs sont déjà sommées
            grouped = df.groupby(['periode', group_col])[use_values_col].sum().unstack(fill_value=0)
        else:
            # Cas standard: compter les lignes
            grouped = df.groupby(['periode', group_col]).size().unstack(fill_value=0)
        total_by_type = grouped.sum().sort_values(ascending=False)
        grouped = grouped[total_by_type.index]
    else:
        if use_values_col:
            # Cas où les valeurs sont déjà sommées
            grouped = df.groupby('periode')[use_values_col].sum().to_frame('Total')
        else:
            # Cas standard: compter les lignes
            grouped = df.groupby('periode').size().to_frame('Total')

    data_to_plot = grouped.cumsum() if cumulatif else grouped
    
    data_to_plot = data_to_plot[data_to_plot.index >= pd.to_datetime(min_date)]

    df_melt = data_to_plot.reset_index().melt(
        id_vars='periode',
        var_name='Origine' if group_col else 'Type',
        value_name='Valeur'
    )

    if time_granularity == 'M':
        df_melt['periode_label'] = df_melt['periode'].dt.strftime('%B')
    else:
        df_melt['periode_label'] = df_melt['periode'].astype(str)

    totaux = data_to_plot.sum(axis=1).reset_index().iloc[1:].reset_index(drop=True)
    totaux.columns = ['periode', 'total']

    if group_col:
        group_list = set(df[group_col].unique())
        # Mapping spécifique pour actif/inactif
        if group_list == {'actif', 'inactif'}:
            color_map = {
                'actif': "#A4E7C7",
                'inactif': "#FFD0BB"
            }
        else:
            # Pour les autres cas, utiliser une palette par défaut
            if colors is None:
                if df[group_col].nunique() < 6:
                    colors = ["#A4E7C7", "#FFD0BB", "#F7C59F", "#7C77B9", "#92B4EC"]
                else:
                    colors = [
                        "#E1E1FD", "#96C7DA", "#D9D9D9", "#E4CDEE", "#FEF1D8",
                        "#F7B1C2", "#A4E7C7", "#FFD0BB", "#C3C3FB", "#EEEEEE",
                        "#FFB595", "#D8EEFE", "#FBE7B5", "#B8D6F7"
                    ]
            color_map = {col: colors[i % len(colors)] for i, col in enumerate(data_to_plot.columns)}
    else:
        color_map = None

    fig = px.area(
        df_melt,
        x="periode",
        y="Valeur",
        color="Origine" if group_col else None,
        color_discrete_map=color_map if group_col else None,
        custom_data=["periode_label"]
    )

    if not group_col:
        fig.update_traces(
            fill='tozeroy',
            fillcolor='rgba(164,231,199,0.5)',
            line=dict(color='rgba(164,231,199,0.9)'),
        )

    fig.update_traces(
        hovertemplate='%{y}<extra></extra>',
        line_shape='spline',
        mode='lines+markers',
        marker=dict(size=5, symbol='circle')
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.2,
        gridcolor='lightgray',
        tickfont=dict(color='gray', size=10)
    )
    fig.update_xaxes(showgrid=False)

    fig.update_layout(
        width=1000,
        height=630,
        legend_title_text=legend_title if group_col else None,
        hovermode="x unified",
        template="simple_white",
        xaxis_title=x_title,
        yaxis_title=y_title,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
    )

    if values_graph:
        # Utiliser une couleur qui fonctionne bien sur les deux thèmes
        # Bleu foncé avec bordure blanche pour la lisibilité
        text_color = '#9A9A9A'  
        
        display_values = totaux['total']
            
        fig.add_trace(
            go.Scatter(
                x=totaux['periode'],
                y=totaux['total'] * 1.02,
                text=display_values,
                mode='text',
                textposition='top left',
                showlegend=False,
                textfont=dict(color=text_color, size=12),
                hoverinfo='skip'
            )
        )

    if objectif is not None:
        fig.add_trace(
            go.Scatter(
                x=data_to_plot.index,
                y=[objectif] * len(data_to_plot),
                mode='lines',
                name='Objectif',
                line=dict(color='#F4A6A6', width=2, dash='dash'),
                showlegend=True,
                hoverinfo='skip'
            )
        )

    return fig


def indicator(value: float, title: str):
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number",
        value=value,
        title={"text": title},
        number={"font": {"size": 60, "color": "royalblue"}}
    ))

    fig.update_layout(
        height=200,
        margin=dict(t=40, b=0, l=0, r=0)
    )

    return fig


