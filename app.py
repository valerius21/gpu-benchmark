import streamlit as st
import pandas as pd
import plotly.express as px

# Lade die CSV-Datei
df = pd.read_csv('benchmarks.csv')

# Neue Spalte 'did_run' erstellen
df['did_run'] = ~df['Tokens/Sekunde'].astype(str).isin(['zu groß', 'kein Speicher'])

# Ersetze nicht-numerische Einträge mit NaN
df['Tokens/Sekunde'] = pd.to_numeric(df['Tokens/Sekunde'], errors='coerce')
df['Preis pro Token/Sekunde (EUR)'] = pd.to_numeric(df['Preis pro Token/Sekunde (EUR)'], errors='coerce')
df['GPU-Auslastung (%)'] = pd.to_numeric(df['GPU-Auslastung (%)'], errors='coerce')

# Titel
st.title('Benchmark Vergleich')

# Zeige die Tabelle
st.subheader('Gesamte Benchmark-Tabelle')
st.dataframe(df)

# Filteroptionen
st.subheader('Filter')

setup_filter = st.multiselect('Setup auswählen', options=df['Setup'].unique(), default=df['Setup'].unique())
modell_filter = st.multiselect('Modell auswählen', options=df['Modell'].unique(), default=df['Modell'].unique())
only_ran = st.checkbox('Nur erfolgreiche Läufe anzeigen', value=False)

filtered_df = df[
    (df['Setup'].isin(setup_filter)) &
    (df['Modell'].isin(modell_filter))
]

if only_ran:
    filtered_df = filtered_df[filtered_df['did_run']]

st.subheader('Gefilterte Ergebnisse')
st.dataframe(filtered_df)

# Beste Preis/Token/Sekunde pro Modell
st.subheader('Beste Preis/Token/Sekunde pro Modell')

for modell in filtered_df['Modell'].unique():
    modell_df = filtered_df[(filtered_df['Modell'] == modell) & (filtered_df['did_run'])]
    if not modell_df.empty:
        best_row = modell_df.loc[modell_df['Preis pro Token/Sekunde (EUR)'].idxmin()]
        st.write(f"**{modell}**: {best_row['Setup']} mit {best_row['Preis pro Token/Sekunde (EUR)']} EUR/Token/Sekunde")

# Diagramme
st.subheader('Vergleichsdiagramme')

# Tokens/Sekunde Balkendiagramm
fig_tokens = px.bar(
    filtered_df[filtered_df['did_run']],
    x='Setup',
    y='Tokens/Sekunde',
    color='Modell',
    barmode='group',
    title='Tokens pro Sekunde Vergleich'
)
st.plotly_chart(fig_tokens)

# Preis pro Token/Sekunde Balkendiagramm
fig_price = px.bar(
    filtered_df[filtered_df['did_run']],
    x='Setup',
    y='Preis pro Token/Sekunde (EUR)',
    color='Modell',
    barmode='group',
    title='Preis pro Token/Sekunde Vergleich'
)
st.plotly_chart(fig_price)

# GPU-Auslastung Balkendiagramm
fig_gpu = px.bar(
    filtered_df[filtered_df['did_run']],
    x='Setup',
    y='GPU-Auslastung (%)',
    color='Modell',
    barmode='group',
    title='GPU-Auslastung Vergleich'
)
st.plotly_chart(fig_gpu)
