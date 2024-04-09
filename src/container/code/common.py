feature_columns_names = [
    "Loan_ID",
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicationIncome",
    "CoapplicationIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area",
]

label_column = "Loan_Status"

columns_dtype = {
    "Loan_ID": "object",
    "ApplicationIncome": "float64",
    "CoApplicationIncome": "float64",
    "LoanAmount": "float64",
    "Loan_Amount_Term": "float64",
    "Gender": "category",
    "Married": "category",
    "Dependents": "category",
    "Education": "category",
    "Credit_History": "category",
    "Property_Area": "category",
    "Loan_Status": "category",
}
