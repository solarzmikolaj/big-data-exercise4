# Raport z Analizy Rynku Koncertów Muzycznych w Polsce

Raport przedstawia wyniki automatycznej eksploracyjnej analizy danych (EDA) rynku imprez muzycznych w Polsce w latach 2024–2025, wykonanej za pomocą zestawu skryptów wchodzących w skład aplikacji. Projekt służy jako trening przed rozbudową do interaktywnego dashboardu (np. w Streamlit lub Jupyter Notebook przy użyciu biblioteki Plotly).

---

## 🖥️ Konsolowy Zapis Działania Programu

Poniżej znajduje się pełny log z konsoli wygenerowany podczas uruchomienia polecenia `python App/concerts_analysis.py`:

```text
======================================================================
  CZESC 1 - WCZYTANIE I WSTEPNA EKSPLORACJA
======================================================================

Shape: (1200, 11)
   -> 1200 wierszy (koncertow), 11 kolumn

Pierwsze 5 wierszy (head):
--------------------------------------------------
   event_id       data    miasto  latitude  longitude     gatunek typ_obiektu  pojemnosc  bilety_sprzedane  cena_biletu_pln  przychod_pln
0     50001 2024-04-12  Warszawa   52.2297    21.0122  electronic     stadion      28892             14552            390.0       5675280
1     50002 2025-01-20    Gdańsk   54.3520    18.6466     hip-hop        klub       1377               952             90.0         85680
2     50003 2024-08-28    Lublin   51.2465    22.5684  electronic        klub        734               678            110.0         74580
3     50004 2024-04-18  Katowice   50.2649    19.0238       indie    festiwal      45244             31557            130.0       4102410

Typy danych (dtypes):
--------------------------------------------------
event_id                     int64
data                datetime64[ns]
miasto                      object
latitude                   float64
longitude                  float64
gatunek                     object
typ_obiektu                 object
pojemnosc                    int64
bilety_sprzedane             int64
cena_biletu_pln            float64
przychod_pln                 int64

Zuzycie pamieci: 103.1 KB

Unikalne wartosci:
--------------------------------------------------
   Liczba unikalnych miast:   10
   Lista miast:               Warszawa, Gdańsk, Lublin, Katowice, Wrocław, Łódź, Kraków, Poznań, Szczecin, Białystok
   Liczba unikalnych gatunkow: 10
   Lista gatunkow:            electronic, hip-hop, indie, rock, jazz, pop, reggae, folk, metal, classical

Brakujace wartosci (isnull().sum()):
--------------------------------------------------
event_id            0
data                0
miasto              0
latitude            0
longitude           0
gatunek             0
typ_obiektu         0
pojemnosc           0
bilety_sprzedane    0
cena_biletu_pln     0
przychod_pln        0

-> Sma brakow w calym zbiorze: 0


======================================================================
  CZESC 2 - WYKRES SLUPKOWY (PRZYCHOD WG MIAST)
======================================================================
Wykres zapisano do pliku: F:\big-data-exercise4\Plots\01_wykres_slupkowy_miasta.html

Laczny przychod z koncertow wg miast (posortowane malejaco):
--------------------------------------------------
   Warszawa            391,973,430 PLN
   Gdańsk              192,767,710 PLN
   Łódź                181,357,180 PLN
   Kraków              175,778,640 PLN
   Poznań              170,662,360 PLN
   Szczecin            155,743,970 PLN
   Katowice            137,064,460 PLN
   Lublin              136,115,110 PLN
   Wrocław             125,091,800 PLN
   Białystok            50,603,470 PLN

-> Liderem rynku jest Warszawa z przychodem 391,973,430 PLN.

======================================================================
  CZESC 3 - WYKRESY LINIOWE / SZEREGI CZASOWE
======================================================================
Wykres ogolnego trendu miesiecznego zapisano: F:\big-data-exercise4\Plots\02_wykres_liniowy_miesiecznie.html
Wykres z podzialem na typy obiektow zapisano: F:\big-data-exercise4\Plots\03_wykres_liniowy_typy_obiektow.html

Srednia miesieczna liczba koncertow w Polsce: 50.0
Najgoraczy miesiac: 2025-10 (66 koncertow)
Najspokojniejszy miesiac: 2025-08 (33 koncertow)

======================================================================
  CZESC 4 - HISTOGRAM I BOXPLOT
======================================================================
Zapisano 3 warianty histogramow cen biletow w katalogu Plots/ (04a_histogram_cen_nbins_*.html)
-> Komentarz: Wartosc nbins=50 najlepiej pokazuje strukture rozkladu i lokalne maksima dla typowych progow cenowych (np. 100, 150, 200 zl).
Boxplot przychodow zapisano do pliku: F:\big-data-exercise4\Plots\04b_boxplot_przychod_typ_obiektu.html

Statystyki przychodu wg typu obiektu (sortowanie po medianie):
-----------------------------------------------------------------
Typ obiektu     | Liczba   | Mediana [PLN]   | Srednia [PLN]  
-----------------------------------------------------------------
stadion         | 67       |     6,654,800 |     7,592,995
festiwal        | 140      |     5,416,240 |     6,268,162
arena           | 163      |     1,150,250 |     1,241,742
amfiteatr       | 155      |       383,350 |       446,848
teatr           | 176      |       129,160 |       159,276
klub            | 499      |        55,400 |        62,499

KOMENTARZ ANLYTYCZNY (Boxplot przychodu):
   Najwyzsze przychody z pojedynczych wydarzen generuja festiwale oraz stadiony.
   Mediana przychodu dla festiwalu wynosi 5,416,240 PLN, a dla stadionu 6,654,800 PLN.
   Wynika to z potężnej pojemnosci tych obiektow (stadiony 20-70 tys. miejsc, festiwale 10-80 tys.)
   oraz wysokich mnoznikow cenowych biletow na imprezy masowe.

======================================================================
  CZESC 5 - SCATTER PLOT (CENA VS WYPELNIENIE SALI)
======================================================================
Scatter plot zapisano: F:\big-data-exercise4\Plots\05_scatter_cena_wypelnienie.html

Wspolczynnik korelacji (Pearson r) miedzy cena biletu a wypelnieniem: +0.0091

KOMENTARZ - Zaleznosc miedzy cena a wypelnieniem:
   Na wykresie rozrzutu nie widać silnej negatywnej ani pozytywnej zaleznosci liniowej
   miedzy cena biletu a wypelnieniem sali (korelacja bliska zeru).
   Wypelnienie sali zalezy w tym modelu od rozkladu beta(5, 2) i grawituje wewnatrz
   przedzialu 70% - 95%, niezaleznie od tego czy bilet kosztuje 80 zl w klubie,
   czy 400 zl na stadionie. Rozmiar punktow wyraznie grupuje typy obiektow:
   male kluby na dole skali pojemnosci, wielkie kola stadionow i festiwali.

======================================================================
  CZESC 6 - MAPA POLSKICH MIAST (SCATTER MAPBOX)
======================================================================
Mape interaktywna zapisano w pliku: F:\big-data-exercise4\Plots\06_mapa_koncertow.html
-> Uzyto mapbox_style='open-street-map', bez koniecznosci podawania klucza API.

Zagregowane dane geograficzne dla top 5 miast:
-----------------------------------------------------------------
  miasto  liczba_koncertow  srednia_cena_pln  laczny_przychod_pln
Warszawa               241            154.69            391973430
  Kraków               157            152.61            175778640
 Wrocław               130            135.92            125091800
  Gdańsk               127            151.65            192767710
    Łódź               123            148.70            181357180

======================================================================
  CZESC 7 - KOMPOZYCJA: SUBPLOTY 2x2
======================================================================
Dashboard 2x2 zapisano: F:\big-data-exercise4\Plots\07_dashboard_subplots_2x2.html
-> Figura zawiera 4 wykresy (slupki przychodow, slupki gatunkow, histogram cen i boxplot wypelnienia) ze wspolnym naglowkiem.

======================================================================
  CZESC 8 - WNIOSKI Z ANALIZY RYNKU KONCERTOW
======================================================================

------------------------------------------------------------------------
                NAJWAZNIEJSZE WNIOSKI Z ANALIZY RYNKU
------------------------------------------------------------------------

1. DOMINACJA STOLICY I DUZYCH AGLOMERACJI
   Najwyzsze przychody oraz najwieksza liczbe wydarzen notuje Warszawa
   (laczny przychod ok. 391,973,430 PLN). Kolejne miejsca zajmuja Krakow i Wroclaw.
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
   Najczesciej organizowanymi koncertami w polsce sa wydarzenia z gatunku HIP-HOP,
   a takze rock i pop. Gatunki niszowe (np. folk, reggae) odbywaja sie rzadziej
   i zazwyczaj w mniejszych obiektach klubowych.
```

---

## 📈 Podsumowanie Wygenerowanych Artefaktów Plotly

Wszystkie wykresy zostały wygenerowane z użyciem interaktywnej biblioteki **Plotly** i zapisane do samodzielnych plików HTML w folderze `Plots/`:

1. **`01_wykres_slupkowy_miasta.html`** – Wykres słupkowy przychodów w podziale na miasta (z sortowaniem malejącym i czytelnymi etykietami na słupkach).
2. **`02_wykres_liniowy_miesiecznie.html`** – Wykres liniowy trendu liczby imprez na przestrzeni kolejnych miesięcy 2024 i 2025 roku.
3. **`03_wykres_liniowy_typy_obiektow.html`** – Wykres liniowy prezentujący miesięczne wahania z podziałem na 6 typów obiektów (klub, arena, stadion, festiwal, teatr, amfiteatr).
4. **`04a_histogram_cen_nbins_{20,50,100}.html`** – Zestaw 3 histogramów badających rozkład cen biletów; wariant `nbins=50` stanowi optymalny kompromis między szczegółowością a wygładzeniem.
5. **`04b_boxplot_przychod_typ_obiektu.html`** – Wykres pudełkowy (boxplot) porównujący rozkłady przychodów per typ obiektu, wyraźnie ukazujący potęgę imprez stadionowych i festiwalowych.
6. **`05_scatter_cena_wypelnienie.html`** – Wykres rozrzutu z kodowaniem koloru wg gatunku oraz rozmiaru punktu wg pojemności sali.
7. **`06_mapa_koncertow.html`** – Interaktywna mapa Polski w oparciu o OpenStreetMap (`px.scatter_mapbox`), prezentująca bąbelki o rozmiarze zależnym od liczby koncertów i kolorze od średniej ceny biletu.
8. **`07_dashboard_subplots_2x2.html`** – Zestawienie 4 kluczowych widoków w układzie 2×2 (zbudowane za pomocą `make_subplots`), gotowe do zaprezentowania na spotkaniu projektowym lub wklejenia do Streamlita.
