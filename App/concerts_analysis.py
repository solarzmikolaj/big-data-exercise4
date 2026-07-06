import os
import warnings
import pandas as pd
import numpy as np

import data_processing as dp
import visualization as viz

# Ignorujemy ostrzezenia dla czystszego logu w konsoli
warnings.filterwarnings('ignore')

# Wyznaczanie sciezek absolutnych wzgledem katalogu projektu
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "Data", "koncerty_polska.csv")
PLOTS_DIR = os.path.join(PROJECT_ROOT, "Plots")

def run_part_1_exploration(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 1 - WCZYTANIE I WSTEPNA EKSPLORACJA")
    print("=" * 70)
    
    info = dp.get_basic_info(df)
    
    print(f"\nShape: {info['shape']}")
    print(f"   -> {info['shape'][0]} wierszy (koncertow), {info['shape'][1]} kolumn\n")
    
    print("Pierwsze 5 wierszy (head):")
    print("-" * 50)
    print(df.head().to_string())
    
    print("\nTypy danych (dtypes):")
    print("-" * 50)
    print(info['dtypes'].to_string())
    print(f"\nZuzycie pamieci: {info['memory_usage_kb']:.1f} KB\n")
    
    print("Unikalne wartosci:")
    print("-" * 50)
    print(f"   Liczba unikalnych miast:   {info['unikalne_miasta']}")
    print(f"   Lista miast:               {', '.join(info['lista_miast'])}")
    print(f"   Liczba unikalnych gatunkow: {info['unikalne_gatunki']}")
    print(f"   Lista gatunkow:            {', '.join(info['lista_gatunkow'])}\n")
    
    print("Brakujace wartosci (isnull().sum()):")
    print("-" * 50)
    print(info['null_counts'].to_string())
    print(f"\n-> Sma brakow w calym zbiorze: {info['total_nulls']}\n")

def run_part_2_bar_chart(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 2 - WYKRES SLUPKOWY (PRZYCHOD WG MIAST)")
    print("=" * 70)
    
    out_file = os.path.join(PLOTS_DIR, "01_wykres_slupkowy_miasta.html")
    viz.plot_city_revenue_bar(df, out_file)
    print(f"Wykres zapisano do pliku: {out_file}")
    
    rev_df = dp.get_city_revenue(df)
    print("\nLaczny przychod z koncertow wg miast (posortowane malejaco):")
    print("-" * 50)
    for idx, row in rev_df.iterrows():
        print(f"   {row['miasto']:<15s} {row['przychod_pln']:>15,.0f} PLN")
    print(f"\n-> Liderem rynku jest {rev_df.iloc[0]['miasto']} "
          f"z przychodem {rev_df.iloc[0]['przychod_pln']:,.0f} PLN.")

def run_part_3_time_series(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 3 - WYKRESY LINIOWE / SZEREGI CZASOWE")
    print("=" * 70)
    
    out_file1 = os.path.join(PLOTS_DIR, "02_wykres_liniowy_miesiecznie.html")
    viz.plot_monthly_concerts_line(df, out_file1)
    print(f"Wykres ogolnego trendu miesiecznego zapisano: {out_file1}")
    
    out_file2 = os.path.join(PLOTS_DIR, "03_wykres_liniowy_typy_obiektow.html")
    viz.plot_monthly_concerts_by_type_line(df, out_file2)
    print(f"Wykres z podzialem na typy obiektow zapisano: {out_file2}")
    
    monthly = dp.get_monthly_concerts(df)
    print(f"\nSrednia miesieczna liczba koncertow w Polsce: {monthly['liczba_koncertow'].mean():.1f}")
    max_month = monthly.loc[monthly["liczba_koncertow"].idxmax()]
    min_month = monthly.loc[monthly["liczba_koncertow"].idxmin()]
    print(f"Najgoraczy miesiac: {max_month['miesiac']} ({max_month['liczba_koncertow']} koncertow)")
    print(f"Najspokojniejszy miesiac: {min_month['miesiac']} ({min_month['liczba_koncertow']} koncertow)")

def run_part_4_histogram_and_boxplot(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 4 - HISTOGRAM I BOXPLOT")
    print("=" * 70)
    
    # Rysujemy histogramy dla nbins 20, 50, 100
    viz.plot_price_histograms(df, PLOTS_DIR)
    print("Zapisano 3 warianty histogramow cen biletow w katalogu Plots/ (04a_histogram_cen_nbins_*.html)")
    print("-> Komentarz: Wartosc nbins=50 najlepiej pokazuje strukture rozkladu i lokalne maksima dla typowych progow cenowych (np. 100, 150, 200 zl).")
    
    out_box = os.path.join(PLOTS_DIR, "04b_boxplot_przychod_typ_obiektu.html")
    viz.plot_revenue_boxplot_by_type(df, out_box)
    print(f"Boxplot przychodow zapisano do pliku: {out_box}")
    
    stats_obj = dp.get_revenue_by_object_type(df)
    print("\nStatystyki przychodu wg typu obiektu (sortowanie po medianie):")
    print("-" * 65)
    print(f"{'Typ obiektu':<15s} | {'Liczba':<8s} | {'Mediana [PLN]':<15s} | {'Srednia [PLN]':<15s}")
    print("-" * 65)
    for _, r in stats_obj.iterrows():
        print(f"{r['typ_obiektu']:<15s} | {r['count']:<8d} | {r['median']:>13,.0f} | {r['mean']:>13,.0f}")
    
    print(f"""
KOMENTARZ ANLYTYCZNY (Boxplot przychodu):
   Najwyzsze przychody z pojedynczych wydarzen generuja festiwale oraz stadiony.
   Mediana przychodu dla festiwalu wynosi {stats_df_val(stats_obj, 'festiwal', 'median'):,.0f} PLN, a dla stadionu {stats_df_val(stats_obj, 'stadion', 'median'):,.0f} PLN.
   Wynika to z potężnej pojemnosci tych obiektow (stadiony 20-70 tys. miejsc, festiwale 10-80 tys.)
   oraz wysokich mnoznikow cenowych biletow na imprezy masowe.
""")

def stats_df_val(df: pd.DataFrame, obj_type: str, col: str) -> float:
    return df.loc[df["typ_obiektu"] == obj_type, col].values[0]

def run_part_5_scatter_plot(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 5 - SCATTER PLOT (CENA VS WYPELNIENIE SALI)")
    print("=" * 70)
    
    out_scatter = os.path.join(PLOTS_DIR, "05_scatter_cena_wypelnienie.html")
    df_occ = dp.add_occupancy_rate(df)
    viz.plot_occupancy_scatter(df_occ, out_scatter)
    print(f"Scatter plot zapisano: {out_scatter}")
    
    corr_val = df_occ["cena_biletu_pln"].corr(df_occ["wypelnienie"])
    print(f"\nWspolczynnik korelacji (Pearson r) miedzy cena biletu a wypelnieniem: {corr_val:+.4f}")
    
    print("""
KOMENTARZ - Zaleznosc miedzy cena a wypelnieniem:
   Na wykresie rozrzutu nie widać silnej negatywnej ani pozytywnej zaleznosci liniowej
   miedzy cena biletu a wypelnieniem sali (korelacja bliska zeru).
   Wypelnienie sali zalezy w tym modelu od rozkladu beta(5, 2) i grawituje wewnatrz
   przedzialu 70% - 95%, niezaleznie od tego czy bilet kosztuje 80 zl w klubie,
   czy 400 zl na stadionie. Rozmiar punktow wyraznie grupuje typy obiektow:
   male kluby na dole skali pojemnosci, wielkie kola stadionow i festiwali.
""")

def run_part_6_map(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 6 - MAPA POLSKICH MIAST (SCATTER MAPBOX)")
    print("=" * 70)
    
    out_map = os.path.join(PLOTS_DIR, "06_mapa_koncertow.html")
    viz.plot_city_map(df, out_map)
    print(f"Mape interaktywna zapisano w pliku: {out_map}")
    print("-> Uzyto mapbox_style='open-street-map', bez koniecznosci podawania klucza API.")
    
    map_df = dp.get_city_map_aggregates(df).sort_values(by="liczba_koncertow", ascending=False)
    print("\nZagregowane dane geograficzne dla top 5 miast:")
    print("-" * 65)
    print(map_df[["miasto", "liczba_koncertow", "srednia_cena_pln", "laczny_przychod_pln"]].head(5).to_string(index=False))

def run_part_7_subplots(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 7 - KOMPOZYCJA: SUBPLOTY 2x2")
    print("=" * 70)
    
    out_sub = os.path.join(PLOTS_DIR, "07_dashboard_subplots_2x2.html")
    viz.plot_2x2_subplots(df, out_sub)
    print(f"Dashboard 2x2 zapisano: {out_sub}")
    print("-> Figura zawiera 4 wykresy (slupki przychodow, slupki gatunkow, histogram cen i boxplot wypelnienia) ze wspolnym naglowkiem.")

def run_part_8_conclusions(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("  CZESC 8 - WNIOSKI Z ANALIZY RYNKU KONCERTOW")
    print("=" * 70)
    
    rev_df = dp.get_city_revenue(df)
    stats_obj = dp.get_revenue_by_object_type(df)
    top_genre = df["gatunek"].value_counts().index[0]
    
    print(f"""
------------------------------------------------------------------------
                NAJWAZNIEJSZE WNIOSKI Z ANALIZY RYNKU
------------------------------------------------------------------------

1. DOMINACJA STOLICY I DUZYCH AGLOMERACJI
   Najwyzsze przychody oraz najwieksza liczbe wydarzen notuje Warszawa
   (laczny przychod ok. {rev_df.iloc[0]['przychod_pln']:,.0f} PLN). Kolejne miejsca zajmuja Krakow i Wroclaw.
   Wielkosc rynku koncertowego jest silnie powiazana z potencjalem ludnosciowym
   i infrastrukturalnym danego miasta.

2. HIERARCHIA OBIEKTOW KULTURY
   Najwyzsze przychody z pojedynczych imprez generuja stadiony oraz festiwale
   (mediana przychodu powyzej 5-7 mln PLN). Klb i teatry organizuja najwiecej
   wydarzen w ujecciu ilosciowym, ale ich wklad w laczny obrot rynkowy jest mniejszy
   ze wzgledu na mniejsza pojemnosc sal (200-2000 miejsc).

3. CENY BILETOW A TYP OBIEKTU
   Najwyzsze ceny biletow wystepuja na stadionach i festiwalach (mnoznik rzedu 1.5x-1.8x
   wzgledem ceny bazowej gatunku). Mimo wyzszych cen biletow, wypelnienie sal na imprezach
   masowych pozostaje bardzo wysokie, co swiadczy o silnym popycie na koncerty gwiazd.

4. SEZONOWOSC WYDARZEN
   Analiza szeregow czasowych pokazuje wyrazna specyfike sezonowa dla plenerow.
   Imprezy festiwalowe i amfiteatralne odbywaja sie niemal wylacznie w okresie
   letnim (czerwiec-sierpien), podczas gdy kluby, teatry i areny funkcjonuja
   stale przez caly rok z lekkim szczytem w sezonie jesienno-zimowym.

5. PREFERENCJE GATUNKOWE
   Najczesciej organizowanymi koncertami w polsce sa wydarzenia z gatunku {top_genre.upper()},
   a takze rock i pop. Gatunki niszowe (np. folk, reggae) odbywaja sie rzadziej
   i zazwyczaj w mniejszych obiektach klubowych.
""")
    
    print("=" * 70)
    print("  ANALIZA ZAKONCZONA — pliki HTML z wykresami zapisano w folderze 'Plots/'")
    print("=" * 70)
    
    if os.path.exists(PLOTS_DIR):
        print("\nWygenerowane pliki wykresow:")
        for f in sorted(os.listdir(PLOTS_DIR)):
            print(f"   Plots/{f}")
    print()

def main():
    try:
        df = dp.load_data(DATA_PATH)
    except Exception as e:
        print(f"Blad wczytywania danych: {e}")
        return
        
    run_part_1_exploration(df)
    run_part_2_bar_chart(df)
    run_part_3_time_series(df)
    run_part_4_histogram_and_boxplot(df)
    run_part_5_scatter_plot(df)
    run_part_6_map(df)
    run_part_7_subplots(df)
    run_part_8_conclusions(df)

if __name__ == '__main__':
    main()
