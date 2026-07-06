import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional

import data_processing as dp

def _save_fig(fig: go.Figure, output_path: Optional[str]):
    """
    Pomocnicza funkcja do zapisywania wykresu do pliku HTML w katalogu Plots.
    """
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.write_html(output_path, include_plotlyjs="cdn")

def plot_city_revenue_bar(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Tworzy interaktywny wykres slupkowy pokazujacy laczny przychod w kazdym miescie.
    Slupki sa posortowane malejaco, dodano czytelne etykiety i tytul.
    """
    revenue_df = dp.get_city_revenue(df)
    
    fig = px.bar(
        revenue_df,
        x="miasto",
        y="przychod_pln",
        title="Łączny przychód z koncertów w polskich miastach [PLN]",
        labels={"miasto": "Miasto", "przychod_pln": "Łączny przychód [PLN]"},
        color="przychod_pln",
        color_continuous_scale="Viridis",
        text_auto=".2s"
    )
    
    fig.update_layout(
        xaxis_title="Miasto",
        yaxis_title="Przychód [PLN]",
        coloraxis_showscale=False,
        template="plotly_white",
        title_font_size=18,
        hoverlabel=dict(bgcolor="white", font_size=13)
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    _save_fig(fig, output_path)
    return fig

def plot_monthly_concerts_line(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Rysuje wykres liniowy pokazujacy laczna liczbe koncertow w kazdym miesiacu.
    """
    monthly_df = dp.get_monthly_concerts(df)
    
    fig = px.line(
        monthly_df,
        x="miesiac",
        y="liczba_koncertow",
        markers=True,
        title="Łączna liczba koncertów w poszczególnych miesiącach (2024–2025)",
        labels={"miesiac": "Miesiąc", "liczba_koncertow": "Liczba koncertów"}
    )
    
    fig.update_layout(
        xaxis_title="Miesiąc",
        yaxis_title="Liczba zorganizowanych koncertów",
        template="plotly_white",
        title_font_size=18
    )
    fig.update_traces(line=dict(width=3, color="#1f77b4"), marker=dict(size=8))
    
    _save_fig(fig, output_path)
    return fig

def plot_monthly_concerts_by_type_line(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Tworzy wykres liniowy z miesieczna liczba koncertow z podzialem na typ obiektu.
    """
    monthly_type_df = dp.get_monthly_concerts_by_type(df)
    
    fig = px.line(
        monthly_type_df,
        x="miesiac",
        y="liczba_koncertow",
        color="typ_obiektu",
        markers=True,
        title="Miesięczna liczba koncertów z podziałem na typ obiektu",
        labels={"miesiac": "Miesiąc", "liczba_koncertow": "Liczba koncertów", "typ_obiektu": "Typ obiektu"}
    )
    
    fig.update_layout(
        xaxis_title="Miesiąc",
        yaxis_title="Liczba koncertów",
        template="plotly_white",
        title_font_size=18,
        legend_title="Typ obiektu"
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    
    _save_fig(fig, output_path)
    return fig

def plot_price_histograms(df: pd.DataFrame, output_dir: Optional[str] = None) -> Dict[int, go.Figure]:
    """
    Generuje histogramy cen biletow dla roznych wartosci nbins (20, 50, 100).
    Zwraca slownik {nbins: figura}.
    """
    figs = {}
    bins_list = [20, 50, 100]
    
    for b in bins_list:
        fig = px.histogram(
            df,
            x="cena_biletu_pln",
            nbins=b,
            title=f"Rozkład cen biletów na koncerty (nbins = {b})",
            labels={"cena_biletu_pln": "Cena biletu [PLN]"},
            color_discrete_sequence=["#2ca02c"]
        )
        fig.update_layout(
            xaxis_title="Cena biletu [PLN]",
            yaxis_title="Liczba ofert",
            template="plotly_white",
            title_font_size=18,
            bargap=0.05
        )
        
        if output_dir:
            out_path = os.path.join(output_dir, f"04a_histogram_cen_nbins_{b}.html")
            _save_fig(fig, out_path)
            
        figs[b] = fig
        
    return figs

def plot_revenue_boxplot_by_type(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Rysuje boxplot przychodu z podzialem na typ obiektu.
    """
    # Sortowanie po medianie przychodu dla lepszej czytelnosci
    order = df.groupby("typ_obiektu")["przychod_pln"].median().sort_values(ascending=False).index.tolist()
    
    fig = px.box(
        df,
        x="typ_obiektu",
        y="przychod_pln",
        category_orders={"typ_obiektu": order},
        color="typ_obiektu",
        title="Rozkład przychodu z koncertów w podziale na typ obiektu",
        labels={"typ_obiektu": "Typ obiektu", "przychod_pln": "Przychód z wydarzenia [PLN]"}
    )
    
    fig.update_layout(
        xaxis_title="Typ obiektu",
        yaxis_title="Przychód [PLN]",
        template="plotly_white",
        title_font_size=18,
        showlegend=False
    )
    
    _save_fig(fig, output_path)
    return fig

def plot_occupancy_scatter(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Tworzy wykres rozrzutu (scatter plot) badajacy zaleznosc miedzy cena biletu a wypelnieniem sali.
    Koloruje punktami wg gatunku, rozmiar wg pojemnosci obiektu.
    """
    df_with_occ = dp.add_occupancy_rate(df) if "wypelnienie" not in df.columns else df
    
    fig = px.scatter(
        df_with_occ,
        x="cena_biletu_pln",
        y="wypelnienie",
        color="gatunek",
        size="pojemnosc",
        hover_name="miasto",
        hover_data=["typ_obiektu", "pojemnosc", "bilety_sprzedane", "przychod_pln"],
        title="Zależność między ceną biletu a wypełnieniem sali (rozmiar punktu: pojemność)",
        labels={
            "cena_biletu_pln": "Cena biletu [PLN]",
            "wypelnienie": "Współczynnik wypełnienia sali (0.0 - 1.0)",
            "gatunek": "Gatunek muzyczny",
            "pojemnosc": "Pojemność obiektu",
            "typ_obiektu": "Typ obiektu"
        },
        size_max=35,
        opacity=0.75
    )
    
    fig.update_layout(
        xaxis_title="Cena biletu [PLN]",
        yaxis_title="Wypełnienie sali",
        template="plotly_white",
        title_font_size=18,
        legend_title="Gatunek"
    )
    
    _save_fig(fig, output_path)
    return fig

def plot_city_map(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Generuje mape Polski (px.scatter_mapbox) ze srednia cena i liczba koncertow per miasto.
    Wykorzystuje darmowy mapbox_style='open-street-map' bez klucza API.
    """
    map_df = dp.get_city_map_aggregates(df)
    
    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        size="liczba_koncertow",
        color="srednia_cena_pln",
        hover_name="miasto",
        hover_data={
            "latitude": False,
            "longitude": False,
            "liczba_koncertow": True,
            "srednia_cena_pln": True,
            "laczny_przychod_pln": True
        },
        color_continuous_scale="Plasma",
        size_max=40,
        zoom=5.3,
        center={"lat": 52.0, "lon": 19.3},
        title="Mapa polskiej sceny koncertowej: liczba wydarzeń i średnia cena biletów",
        labels={
            "srednia_cena_pln": "Średnia cena [PLN]",
            "liczba_koncertow": "Liczba koncertów",
            "laczny_przychod_pln": "Przychód [PLN]"
        }
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        title_font_size=18,
        template="plotly_white"
    )
    
    _save_fig(fig, output_path)
    return fig

def plot_2x2_subplots(df: pd.DataFrame, output_path: Optional[str] = None) -> go.Figure:
    """
    Kompozycja 4 wykresow w jednej figurze 2x2 przy uzyciu make_subplots.
    Wykresy podsumowujace caly zbior danych o polskim rynku koncertowym.
    """
    df_occ = dp.add_occupancy_rate(df) if "wypelnienie" not in df.columns else df
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "1. Łączny przychód wg miast [PLN]",
            "2. Liczba koncertów wg gatunku muzycznego",
            "3. Rozkład cen biletów (histogram)",
            "4. Wypełnienie sali wg typu obiektu"
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.10
    )
    
    # Subplot (1,1): Slupki przychodu wg miasta
    rev_df = dp.get_city_revenue(df_occ).head(6)
    fig.add_trace(
        go.Bar(
            x=rev_df["miasto"],
            y=rev_df["przychod_pln"],
            marker_color="#1f77b4",
            name="Przychód [PLN]",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Subplot (1,2): Liczba koncertow wg gatunku
    genre_df = df_occ["gatunek"].value_counts().reset_index()
    genre_df.columns = ["gatunek", "liczba"]
    fig.add_trace(
        go.Bar(
            x=genre_df["gatunek"],
            y=genre_df["liczba"],
            marker_color="#ff7f0e",
            name="Liczba koncertów",
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Subplot (2,1): Histogram cen
    fig.add_trace(
        go.Histogram(
            x=df_occ["cena_biletu_pln"],
            nbinsx=40,
            marker_color="#2ca02c",
            name="Ceny biletów",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Subplot (2,2): Boxplot wypelnienia wg typu obiektu
    types_order = df_occ.groupby("typ_obiektu")["wypelnienie"].median().sort_values(ascending=False).index
    for t_obj in types_order:
        sub_df = df_occ[df_occ["typ_obiektu"] == t_obj]
        fig.add_trace(
            go.Box(
                y=sub_df["wypelnienie"],
                name=t_obj,
                showlegend=False
            ),
            row=2, col=2
        )
        
    # Aktualizacja ukladu naglowka i osi
    fig.update_layout(
        title_text="<b>Dashboard analityczny rynku koncertów muzycznych w Polsce</b>",
        title_font_size=22,
        title_x=0.5,
        height=850,
        width=1350,
        template="plotly_white"
    )
    
    # Etykiety osi dla poszczegolnych subplottow
    fig.update_xaxes(title_text="Miasto", row=1, col=1)
    fig.update_yaxes(title_text="Przychód [PLN]", row=1, col=1)
    
    fig.update_xaxes(title_text="Gatunek", row=1, col=2)
    fig.update_yaxes(title_text="Liczba wydarzeń", row=1, col=2)
    
    fig.update_xaxes(title_text="Cena biletu [PLN]", row=2, col=1)
    fig.update_yaxes(title_text="Liczba ofert", row=2, col=1)
    
    fig.update_xaxes(title_text="Typ obiektu", row=2, col=2)
    fig.update_yaxes(title_text="Wypełnienie (0-1)", row=2, col=2)
    
    _save_fig(fig, output_path)
    return fig
