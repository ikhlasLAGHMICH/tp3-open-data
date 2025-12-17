import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str = "") -> go.Figure:
    """Crée un bar chart interactif."""
    fig = px.bar(
        df, x=x, y=y, 
        title=title,
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        hovermode="x unified"
    )
    return fig


def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str = "") -> go.Figure:
    """Crée un pie chart interactif."""
    fig = px.pie(
        df, names=names, values=values,
        title=title,
        hole=0.3  # Donut chart
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_scatter_plot(df: pd.DataFrame, x: str, y: str, 
                        color: str = None, title: str = "") -> go.Figure:
    """Crée un scatter plot interactif."""
    fig = px.scatter(
        df, x=x, y=y, color=color,
        title=title,
        template="plotly_white"
    )
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    return fig


def create_histogram(df: pd.DataFrame, x: str, nbins: int = 30, 
                     title: str = "") -> go.Figure:
    """Crée un histogramme interactif."""
    fig = px.histogram(
        df, x=x, nbins=nbins,
        title=title,
        template="plotly_white"
    )
    return fig


def create_line_chart(df: pd.DataFrame, x: str, y: str, 
                      title: str = "") -> go.Figure:
    """Crée un line chart interactif."""
    fig = px.line(
        df, x=x, y=y,
        title=title,
        template="plotly_white",
        markers=True
    )
    return fig


def create_heatmap(df: pd.DataFrame, title: str = "") -> go.Figure:
    """Crée une heatmap de corrélation."""
    # Sélectionner uniquement les colonnes numériques
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    
    fig = px.imshow(
        corr,
        title=title or "Matrice de corrélation",
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )
    return fig