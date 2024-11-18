# Import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load and prepare the data
df = pd.read_csv("Dataset/converted_data.csv")

# Define features (X) and targets (y)
features = ["Income", "Dependents"]
targets = [
    "Bills_Percentage",
    "Groceries_Percentage",
    "Transport_Percentage",
    "Entertainment_Percentage",
    "Healthcare_Percentage",
    "Education_Percentage",
    "Utilities_Percentage",
    "Disposable_Income_Percentage",
]

X = df[features]
y = df[targets]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize and train models for each expense category
models = {}
scores = {}

for target in targets:
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train[target])

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate scores
    r2 = r2_score(y_test[target], y_pred)
    rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))

    # Store model and scores
    models[target] = model
    scores[target] = {"R2": r2, "RMSE": rmse}

# Display model performance
print("Model Performance Metrics:")
print("\nR-squared scores:")
for target, metrics in scores.items():
    print(f"{target}: {metrics['R2']:.4f}")

print("\nRoot Mean Squared Error:")
for target, metrics in scores.items():
    print(f"{target}: {metrics['RMSE']:.4f}")

# Visualization of model performance
plt.figure(figsize=(12, 6))
r2_scores = [metrics["R2"] for metrics in scores.values()]
categories = [cat.replace("_Percentage", "") for cat in targets]

plt.bar(categories, r2_scores)
plt.title("R-squared Scores by Expense Category")
plt.xticks(rotation=45)
plt.ylabel("R-squared Score")
plt.tight_layout()
plt.show()


# Function to make recommendations
def get_expense_recommendations(income, dependents):
    # Create input array
    input_data = np.array([[income, dependents]])

    # Get predictions for each category
    recommendations = {}
    for category, model in models.items():
        percentage = model.predict(input_data)[0]
        # Ensure percentage is between 0 and 100
        percentage = max(0, min(100, percentage))
        recommendations[category] = percentage

    # Calculate actual amounts
    amounts = {}
    for category, percentage in recommendations.items():
        category_name = category.replace("_Percentage", "")
        amounts[category_name] = (percentage / 100) * income

    return recommendations, amounts


# Example usage
sample_income = 5000000
sample_dependents = 2

percentages, amounts = get_expense_recommendations(sample_income, sample_dependents)

print(
    "\nExample Recommendations for Income:",
    sample_income,
    "and Dependents:",
    sample_dependents,
)
print("\nRecommended Percentages:")
for category, percentage in percentages.items():
    category_name = category.replace("_Percentage", "")
    print(f"{category_name}: {percentage:.2f}%")

print("\nRecommended Monthly Amounts:")
for category, amount in amounts.items():
    print(f"{category}: {amount:,.2f}")

# Feature importance analysis
plt.figure(figsize=(12, 6))
importance_data = []

for target in targets:
    model = models[target]
    importance = abs(model.coef_)
    importance_data.append(
        {
            "Category": target.replace("_Percentage", ""),
            "Income_Importance": importance[0],
            "Dependents_Importance": importance[1],
        }
    )

importance_df = pd.DataFrame(importance_data)

# Plot feature importance
plt.figure(figsize=(12, 6))
x = np.arange(len(importance_df))
width = 0.35

plt.bar(x - width / 2, importance_df["Income_Importance"], width, label="Income")
plt.bar(
    x + width / 2, importance_df["Dependents_Importance"], width, label="Dependents"
)

plt.xlabel("Expense Categories")
plt.ylabel("Feature Importance (Absolute Coefficient Value)")
plt.title("Feature Importance by Expense Category")
plt.xticks(x, importance_df["Category"], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
