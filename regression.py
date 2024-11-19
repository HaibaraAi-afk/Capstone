import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# Load and clean the dataset
def load_and_clean_data(filepath):
    data = pd.read_csv(filepath)
    data.dropna(inplace=True)
    return data


# Train the regression model
def train_model(data):
    X = data[["Income", "Dependents"]]
    y = data[
        [
            "Bills",
            "Groceries",
            "Transport",
            "Entertainment",
            "Healthcare",
            "Education",
            "Utilities",
        ]
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Evaluation:\nMean Squared Error: {mse}\nR² Score: {r2}")

    return model


# Predict allocations based on income and dependents
def predict_allocations(model, income, dependents):
    input_data = np.array([[income, dependents]])
    predicted_allocations = model.predict(input_data)[0]

    total_allocations = sum(predicted_allocations)
    savings = income - total_allocations

    allocations = {
        "Bills": predicted_allocations[0],
        "Groceries": predicted_allocations[1],
        "Transport": predicted_allocations[2],
        "Entertainment": predicted_allocations[3],
        "Healthcare": predicted_allocations[4],
        "Education": predicted_allocations[5],
        "Utilities": predicted_allocations[6],
        "Savings": savings,
    }

    return allocations


# Main function to run the program
def main():
    data = load_and_clean_data("Dataset/Converted_data.csv")
    model = train_model(data)

    while True:
        try:
            income = float(input("Enter your income: "))
            dependents = int(input("Enter the number of dependents: "))

            allocations = predict_allocations(model, income, dependents)

            print("\nRecommended Allocations:")
            for category, amount in allocations.items():
                print(f"{category}: {amount:,.0f}")

            total = sum(allocations.values())
            print(f"\nTotal Allocations: {total:,.0f}")
            print(f"Validation: {'Valid' if np.isclose(total, income) else 'Invalid'}")

            break
        except ValueError:
            print(
                "Invalid input. Please enter numeric values for income and dependents."
            )


if __name__ == "__main__":
    main()
