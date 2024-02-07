import tabula
import pandas

# Specifica il percorso del tuo file PDF
file_path = "https://www.itinerariprevidenziali.it/site/home/biblioteca/pubblicazioni/documento32059891.html"

# Specifica il numero della pagina contenente la tabella
page_number = 91

# Esegui l'estrazione dei dati
df_list = tabula.read_pdf(file_path, pages=page_number)

# Utilizza la seconda riga come intesta delle colonne
df = df_list[0].iloc[1:]

# Reimposta gli indici del DataFrame
df.reset_index(drop=True, inplace=True)

# Visualizza il DataFrame risultante
print(df)
df=df[3:]

# Definire un dizionario con i nuovi nomi delle colonne
nuovi_nomi_colonne = {'Unnamed: 0': 'Categoria', 'Unnamed: 1': 'Pensionati'}

# Utilizzare il metodo rename() per rinominare le colonne
df = df.rename(columns=nuovi_nomi_colonne)

import re

# Definire una funzione per la conversione
def converti_numero(stringa):
    # Rimuovere i punti dalla stringa e convertire in float
    try:
        numero = float(re.sub(r'\.', '', stringa))
        return numero
    except ValueError:
        return None

# Applicare la funzione di conversione alla colonna 'Pensionati'
df['Pensionati'] = df['Pensionati'].apply(converti_numero)

# Calcolare la colonna 'Pensionati_perc'
df = df.drop(54)
df['Pensionati_perc'] = df['Pensionati'].cumsum() / df['Pensionati'].sum()*100


df.reset_index(inplace=True)
del df['index']
df['Importo complessivo'] = df['Importo complessivo'].apply(converti_numero)

import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plt.title('Andamento del numero dei pensionati e dell\'importo annuo del reddito pensionistico')
plt.plot(df.Pensionati_perc, marker='o', label='Numero pensionati')
plt.xticks(range(0, len(df), 5), df['Importo medio'][::5], rotation=30, ha='right')
plt.xlabel('Categorie di reddito pensionistico lordo mensile')
plt.ylabel('Percentuale di Pensionati')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt


fig, ax1 = plt.subplots(figsize=(20, 10))

# Primo asse y (sinistro) per 'Numero pensionati_perc'
color = 'tab:blue'
ax1.set_xlabel('Importo medio netto annuale')
ax1.set_ylabel('% pensionati', color=color)
ax1.plot(df.index, df.Pensionati_perc, marker='o', color=color, )
ax1.tick_params(axis='y', labelcolor=color)

# Creazione di un secondo asse y (destro) per 'Importo complessivo'
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Costo complessivo in Miliardi di Euro', color=color)
ax2.plot(df.index, df['Importo complessivo']/1000000000, marker='o', color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.title('Numero pensionati VS Costo complessivo annuo delle pensioni')
ax1.tick_params(axis='x', which='major', labelrotation=15)
ax2.tick_params(axis='x', which='major', labelrotation=15)

ax1.set_xticks(range(0, len(df), 2))
ax1.set_xticklabels(df['Importo medio'][::2], rotation=15, ha='right')

ax2.set_xticks(range(0, len(df), 2))
ax2.set_xticklabels(df['Importo medio'][::2], rotation=15, ha='right')
plt.grid()
plt.tight_layout()

plt.text(0.05, -0.05, 'Tabella 5.5 - Numero pensionati e importo complessivo annuo del reddito pensionistico lordo e netto per classidi reddito mensile lordo - anno 2022. Dati XI Rapporto itinerari previdenziali', transform=fig.transFigure, fontsize=14)

plt.show()


# Plot del grafico
plt.figure(figsize=(20, 10))
plt.title('Numero pensionati e importo complessivo annuo del reddito pensionistico, top 5%')
plt.plot(df.Pensionati_perc, marker='o')

# Impostare le etichette sull'asse x mostrando solo ogni 5 categorie
plt.xticks(range(0, len(df),5), df.Categoria[::5], rotation=45, ha='right')


plt.ylim(bottom=95, top=101)
plt.grid(True)
plt.show()

# Plot del grafico
plt.figure(figsize=(20, 10))
plt.title('Numero pensionati e importo complessivo annuo del reddito pensionistico, top 50%')
plt.plot(df.Pensionati_perc, marker='o')

# Impostare le etichette sull'asse x mostrando solo ogni 5 categorie
plt.xticks(range(0, len(df),1), df.Categoria[::1], rotation=45, ha='right')

plt.ylim(bottom=50, top=101)
plt.grid(True)
plt.show()
