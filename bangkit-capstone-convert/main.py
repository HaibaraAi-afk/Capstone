# CSV Structure: data.csv
# Note: The amount is in INR
# 0: Income
# 1: Age
# 2: Dependents
# 3: Occupation
# 4: City_Tier
# 5: Rent
# 6: Loan_Repayment
# 7: Insurance
# 8: Groceries
# 9: Transport
# 10: Eating_Out
# 11: Entertainment
# 12: Utilities
# 13: Healthcare
# 14: Education
# 15: Miscellaneous
# 16: Desired_Savings_Percentage
# 17: Desired_Savings
# 18: Disposable_Income
# 19: Potential_Savings_Groceries
# 20: Potential_Savings_Transport
# 21: Potential_Savings_Eating_Out
# 22: Potential_Savings_Entertainment
# 23: Potential_Savings_Utilities
# 24: Potential_Savings_Healthcare
# 25: Potential_Savings_Education
# 26: Potential_Savings_Miscellaneous

# Desired CSV Structure: converted_data.csv
# 0: Income
# 1: Age
# 2: Dependents
# 3: Occupation
# 4: City_Tier
# 5: Bills = Rent + Loan_Repayment + Insurance
# 6: Bills_Percentage = (Bills / Income) * 100
# 7: Groceries = Groceries + Eating_Out
# 8: Groceries_Percentage = (Groceries / Income) * 100
# 9: Transport
# 10: Transport_Percentage = (Transport / Income) * 100
# 12: Entertainment
# 13: Entertainment_Percentage = (Entertainment / Income) * 100
# 14: Healthcare
# 15: Healthcare_Percentage = (Healthcare / Income) * 100
# 16: Education
# 17: Education_Percentage = (Education / Income) * 100
# 18: Utilities = Utilities + Miscellaneous
# 19: Utilities_Percentage = (Utilities / Income) * 100
# 20: Disposable_Income = Income - Bills - Groceries - Transport - Entertainment - Healthcare - Education - Utilities
# 21: Disposable_Income_Percentage = (Disposable_Income / Income) * 100

# 1. Read data.csv and delete converted_data.csv if exists
# 2. Iterate through each row in data.csv
# 3. Calculate the desired values
# 4. Convert the amounts to IDR using the exchange rate of 1 INR = 187.13 IDR
# 5. Write the desired values to converted_data.csv

import pandas as pd
import os

# Read data.csv
data = pd.read_csv("data.csv")

# Delete converted_data.csv if exists
try:
    os.remove("converted_data.csv")
except FileNotFoundError:
    pass
# Delete converted_data.csv if exists
try:
    os.remove("converted_data_amount.csv")
except FileNotFoundError:
    pass
# Delete converted_data.csv if exists
try:
    os.remove("converted_data_percentage.csv")
except FileNotFoundError:
    pass


rate = 187.13


def convert_to_idr(amount, rate):
    return amount * rate


with open("converted_data.csv", "a") as file:
    file.write(
        "Income,Age,Dependents,Occupation,City_Tier,Bills,Bills_Percentage,Groceries,Groceries_Percentage,Transport,Transport_Percentage,Entertainment,Entertainment_Percentage,Healthcare,Healthcare_Percentage,Education,Education_Percentage,Utilities,Utilities_Percentage,Disposable_Income,Disposable_Income_Percentage\n"
    )


# Iterate through each row in data.csv
for index, row in data.iterrows():
    amounts = {}
    percentages = {}

    # Calculate the desired values
    amounts["Bills"] = row["Rent"] + row["Loan_Repayment"] + row["Insurance"]
    amounts["Groceries"] = row["Groceries"] + row["Eating_Out"]
    amounts["Transport"] = row["Transport"]
    amounts["Entertainment"] = row["Entertainment"]
    amounts["Healthcare"] = row["Healthcare"]
    amounts["Education"] = row["Education"]
    amounts["Utilities"] = row["Utilities"] + row["Miscellaneous"]
    amounts["Disposable_Income"] = (
        row["Income"]
        - amounts["Bills"]
        - amounts["Groceries"]
        - amounts["Transport"]
        - amounts["Entertainment"]
        - amounts["Healthcare"]
        - amounts["Education"]
        - amounts["Utilities"]
    )

    # Convert the amounts to IDR using the exchange rate of 1 INR = 187.13 IDR
    income = convert_to_idr(row["Income"], rate)
    bills = convert_to_idr(amounts["Bills"], rate)
    groceries = convert_to_idr(amounts["Groceries"], rate)
    transport = convert_to_idr(amounts["Transport"], rate)
    entertainment = convert_to_idr(amounts["Entertainment"], rate)
    healthcare = convert_to_idr(amounts["Healthcare"], rate)
    education = convert_to_idr(amounts["Education"], rate)
    utilities = convert_to_idr(amounts["Utilities"], rate)
    disposable_income = convert_to_idr(amounts["Disposable_Income"], rate)

    # Calculate percentages of the amounts to the income
    percentages["Bills"] = (amounts["Bills"] / row["Income"]) * 100
    percentages["Groceries"] = (amounts["Groceries"] / row["Income"]) * 100
    percentages["Transport"] = (amounts["Transport"] / row["Income"]) * 100
    percentages["Entertainment"] = (amounts["Entertainment"] / row["Income"]) * 100
    percentages["Healthcare"] = (amounts["Healthcare"] / row["Income"]) * 100
    percentages["Education"] = (amounts["Education"] / row["Income"]) * 100
    percentages["Utilities"] = (amounts["Utilities"] / row["Income"]) * 100
    percentages["Disposable_Income"] = (
        amounts["Disposable_Income"] / row["Income"]
    ) * 100

    # Write the desired values to converted_data.csv
    with open("converted_data.csv", "a") as file:
        file.write(
            f"{income},{row['Age']},{row['Dependents']},{row['Occupation']},{row['City_Tier']},{bills},{percentages['Bills']},{groceries},{percentages['Groceries']},{transport},{percentages['Transport']},{entertainment},{percentages['Entertainment']},{healthcare},{percentages['Healthcare']},{education},{percentages['Education']},{utilities},{percentages['Utilities']},{disposable_income},{percentages['Disposable_Income']}\n"
        )
    with open("converted_data_amount.csv", "a") as file:
        file.write(
            f"{income},{row['Age']},{row['Dependents']},{row['Occupation']},{row['City_Tier']},{bills},{groceries},{transport},{entertainment},{healthcare},{education},{utilities},{disposable_income}\n"
        )
    with open("converted_data_percentage.csv", "a") as file:
        file.write(
            f"{income},{row['Age']},{row['Dependents']},{row['Occupation']},{row['City_Tier']},{percentages['Bills']},{percentages['Groceries']},{percentages['Transport']},{percentages['Entertainment']},{percentages['Healthcare']},{percentages['Education']},{percentages['Utilities']},{percentages['Disposable_Income']}\n"
        )

print("Conversion completed!")
