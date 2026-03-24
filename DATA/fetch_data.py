import pandas as pd

print("Project setup successful")

data = {
    "hour":[1,2,3,4,5],
    "electricity_demand":[50000,52000,51000,53000,54000]
}

df = pd.DataFrame(data)

df.to_csv("sample_energy_data.csv", index=False)

print("Sample dataset created")
