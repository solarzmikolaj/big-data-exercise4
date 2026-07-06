import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

def load_data(filepath: str) -> pd.DataFrame:
    """
    Funkcja wczytujaca dane o koncertach z pliku csv.
    Zwraca sforwardowany DataFrame z sparsowanymi datami w kolumnie 'data'.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=["data"])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku z danymi pod sciezka: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Blad podczas wczytywania pliku CSV: {e}")

def get_basic_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Oblicza podstawowe statystki i metadane dla zbioru koncertow.
    """
    return {
        "shape": df.shape,
        "dtypes": df.dtypes,
        "memory_usage_kb": df.memory_usage(deep=True).sum() / 1024,
        "null_counts": df.isnull().sum(),
        "total_nulls": df.isnull().sum().sum(),
        "unikalne_miasta": df["miasto"].nunique(),
        "unikalne_gatunki": df["gatunek"].nunique(),
        "lista_miast": df["miasto"].unique().tolist(),
        "lista_gatunkow": df["gatunek"].unique().tolist()
    }

def get_city_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje laczny przychod dla kazdego miasta i sortuje malejco.
    """
    revenue_df = df.groupby("miasto")["przychod_pln"].sum().reset_index()
    revenue_df = revenue_df.sort_values(by="przychod_pln", ascending=False).reset_index(drop=True)
    return revenue_df

def get_monthly_concerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje dane do poziomu miesiaca i liczy laczna liczbe koncertow.
    Zwraca ramke z kolumnami ['miesiac', 'liczba_koncertow'].
    """
    df_temp = df.copy()
    df_temp["miesiac"] = df_temp["data"].dt.to_period("M").astype(str)
    monthly = df_temp.groupby("miesiac").size().reset_index(name="liczba_koncertow")
    monthly = monthly.sort_values("miesiac").reset_index(drop=True)
    return monthly

def get_monthly_concerts_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje miesieczna liczbe koncertow z podzialem na typ obiektu.
    """
    df_temp = df.copy()
    df_temp["miesiac"] = df_temp["data"].dt.to_period("M").astype(str)
    monthly_type = df_temp.groupby(["miesiac", "typ_obiektu"]).size().reset_index(name="liczba_koncertow")
    monthly_type = monthly_type.sort_values(["miesiac", "typ_obiektu"]).reset_index(drop=True)
    return monthly_type

def add_occupancy_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dodaje kolumne 'wypelnienie' jako stosunek biletow sprzedanych do pojemnosci obiektu.
    """
    df_new = df.copy()
    df_new["wypelnienie"] = df_new["bilety_sprzedane"] / df_new["pojemnosc"]
    return df_new

def get_city_map_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje dane do poziomu miasta dla mapy: srednia cena biletu, liczba koncertow,
    laczny przychod oraz wspolrzedne geograficzne (latitude, longitude).
    """
    map_df = df.groupby("miasto").agg(
        srednia_cena_pln=("cena_biletu_pln", "mean"),
        liczba_koncertow=("event_id", "count"),
        laczny_przychod_pln=("przychod_pln", "sum"),
        latitude=("latitude", "first"),
        longitude=("longitude", "first")
    ).reset_index()
    
    map_df["srednia_cena_pln"] = map_df["srednia_cena_pln"].round(2)
    return map_df

def get_revenue_by_object_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Oblicza medine i sredni przychod w podziale na typ obiektu do komentarzy analitycznych.
    """
    stats_df = df.groupby("typ_obiektu")["przychod_pln"].agg(["count", "mean", "median", "sum"]).reset_index()
    stats_df = stats_df.sort_values(by="median", ascending=False).reset_index(drop=True)
    return stats_df
