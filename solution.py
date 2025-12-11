import pandas as pd

# load csv file
df = pd.read_csv("source.csv")

# convert Datetime column from UTC to UTC plus 6
df["Datetime"] = pd.to_datetime(df["Datetime"]) + pd.Timedelta(hours=6)

# create the total column
totals = []

for idx, row in df.iterrows():
    name = row["Name"]
    purity = row["Purity"]
    amount = row["Amount"]
    price = row["Price"]
    time_val = row["Datetime"]
    
    # adjust price for Impure
    if purity == "Impure":
        price = price * 0.75
    
    # Product A outright
    if name == "ProductA":
        total = amount * price
    
    # Product B diff
    elif name == "ProductB":
        # match ProductA at the same datetime
        match = df[(df["Name"] == "ProductA") & (df["Datetime"] == time_val)]
        
        if not match.empty:
            price_a = match.iloc[0]["Price"]
            
            # adjust Product A price if impure
            if purity == "Impure":
                price_a = price_a * 0.75
            
            total = amount * price_a
        else:
            total = None
    
    else:
        total = None
    
    totals.append(total)

df["total"] = totals

# save result csv
df.to_csv("result.csv", index=False)
