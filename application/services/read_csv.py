import pandas as pd


def read_csv_file():
    url = 'https://drive.google.com/uc?export=download&id=13nk_FYpcayUck2Ctrela5Tjt9JQbjznt'
    df = pd.read_csv(url)
    height = df["Height(Inches)"].mean()
    weight = df["Weight(Pounds)"].mean()
    height_sm = height * 2.54
    weight_kg = weight * 0.453592
    print(f'Average height of people: {height_sm} sm')
    print(f'Average weight of people: {weight_kg} kg')
