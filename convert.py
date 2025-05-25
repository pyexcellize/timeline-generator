import pandas as pd
from openpyxl import Workbook
import csv

df = pd.DataFrame()


def generate_data(num_rows=1000000):
    data = {
        "appearance_id": [f"ID-{i % 100}" for i in range(num_rows)],
        "date": [f"2024-01-{i % 28 + 1:02}" for i in range(num_rows)],
        "color": [f"Color-{i % 5}" for i in range(num_rows)],
        "type": [f"Type-{i % 5}" for i in range(num_rows)],
        "asdasd": [f"asdasd-{i % 5}" for i in range(num_rows)],
        "sss": [f"sss-{i % 5}" for i in range(num_rows)],
        "asasdasd": [f"asasdasd-{i % 5}" for i in range(num_rows)],
        "asdfgh": [f"asdfgh-{i % 5}" for i in range(num_rows)],
        "osjkdfspdf": [f"osjkdfspdf-{i % 5}" for i in range(num_rows)],
        "asdfoihjasoin": [f"asdfoihjasoin-{i % 5}" for i in range(num_rows)],
        "bfoiuhsew": [f"bfoiuhsew-{i % 5}" for i in range(num_rows)],
        "asdaoksnsdasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksnsdsasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "adsdaoksndasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asddaoksndasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaodksndasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndas2d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdsndas2d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdsnd1asd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndasdasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdnsdasd": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndas123d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndas1d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndas3d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndas4d": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)],
        "asdaoksdndasd5": [f"asdaoksndasd-{i % 5}" for i in range(num_rows)]
    }
    df = pd.DataFrame(data)
    df.set_index("appearance_id", inplace=True)
    return df


def save_to_excel(df, file_name="data.xlsx"):
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
        print(f"Data saved to {file_name}")
    return df


def save_to_csv(df, file_name="data.csv"):
    df.to_csv(file_name, index=True)
    print(f"Data saved to {file_name}")
    return df


def main():
    df = generate_data(300000)
    save_to_excel(df, "data/data.xlsx")


if __name__ == "__main__":
    main()
