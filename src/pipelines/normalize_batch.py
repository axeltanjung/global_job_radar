import pandas as pd
from src.parsers.title_classifier import is_data_role

df = pd.read_csv("data/raw/jobs_raw.csv")

df = df[df.title.apply(is_data_role)]
df.to_csv("data/processed/jobs_data_only.csv", index=False)
