import pandas as pd

print("Starting final merge...")

# function to convert German numbers
def clean_number(x):
    if isinstance(x, str):
        x = x.replace(".", "").replace(",", ".")
    return float(x)

# ---------------- LOAD ----------------
load = pd.read_csv(
    "DATA/data/Realisierter_Stromverbrauch_202501010000_202603010000_Stunde.csv",
    sep=";"
)

load = load.rename(columns={
    "Datum von": "time",
    "Netzlast [MWh] Berechnete Auflösungen": "load"
})

load["time"] = pd.to_datetime(load["time"], dayfirst=True)
load["load"] = load["load"].apply(clean_number)

load = load[["time", "load"]]


# ---------------- GENERATION ----------------
gen = pd.read_csv(
    "DATA/data/Realisierte_Erzeugung_202501010000_202603010000_Stunde.csv",
    sep=";"
)

gen = gen.rename(columns={
    "Datum von": "time",
    "Wind Offshore [MWh] Berechnete Auflösungen": "wind_offshore",
    "Wind Onshore [MWh] Berechnete Auflösungen": "wind_onshore",
    "Photovoltaik [MWh] Berechnete Auflösungen": "solar"
})

gen["time"] = pd.to_datetime(gen["time"], dayfirst=True)

gen["wind_offshore"] = gen["wind_offshore"].apply(clean_number)
gen["wind_onshore"] = gen["wind_onshore"].apply(clean_number)
gen["solar"] = gen["solar"].apply(clean_number)

gen["wind"] = gen["wind_offshore"] + gen["wind_onshore"]

gen = gen[["time", "wind", "solar"]]


# ---------------- PRICE ----------------
price = pd.read_csv(
    "DATA/data/Gro_handelspreise_202501010000_202603010000_Stunde.csv",
    sep=";"
)

price = price.rename(columns={
    "Datum von": "time",
    "Deutschland/Luxemburg [€/MWh] Berechnete Auflösungen": "price"
})

price["time"] = pd.to_datetime(price["time"], dayfirst=True)
price["price"] = price["price"].apply(clean_number)

price = price[["time", "price"]]


# ---------------- MERGE ----------------
df = load.merge(gen, on="time")
df = df.merge(price, on="time")

# ---------------- SAVE ----------------
df.to_csv("DATA/data/final_dataset.csv", index=False)

print("FINAL CLEAN DATASET CREATED 🔥")
print(df.head())