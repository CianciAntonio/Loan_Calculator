import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

tot_value = float(input("insert estate value: "))
loan_percentage = float(input("insert loan % of estate value: "))
interest_rate0 = float(input("insert interest rate: "))
years = int(input("insert loan term in years: "))
am = input("select amortization type: f for french, i for italian: ")

interest_rate = interest_rate0 / 100 
months = years * 12
month0 = 0
loan_value = tot_value * loan_percentage
loan_value_diff = tot_value * (1 - loan_percentage)

loan_residue = [loan_value]
int_q = []
val_q = []
payment = []
month = []
final_interest_value = 0

for i in range(0,months):
    if am == "f":
        payment.append(interest_rate/12 * loan_residue[i]/(1-1/(pow(1+interest_rate/12,months - month0))))
        month0 = month0 + 1
        month.append(i+1)
        int_q.append(loan_residue[i] * interest_rate/12)
        val_q.append(payment[i] - int_q[i])
        loan_residue.append(loan_residue[i] - val_q[i])
        final_interest_value = final_interest_value + int_q[i] 
    elif am == "i":
        int_q.append(loan_residue[i] * interest_rate/12)
        val_q.append(loan_value / months)
        payment.append(int_q[i] + val_q[i])
        month.append(i+1)
        loan_residue.append(loan_residue[i] - val_q[i])
        final_interest_value = final_interest_value + int_q[i]
    else:
        print("error")

Total_money_spent = final_interest_value + tot_value

print(f"Final Value: {final_interest_value}\nAdvance: {loan_value_diff}\nTotal money spent: {Total_money_spent}")

tab = {
    "Month":month,
    "Capital Share":val_q,
    "Interest Share":int_q,
    "Residue Share":loan_residue[1:],
    "Monthly Payment":payment
}
df = pd.DataFrame(tab)

fig=px.line(data_frame=df,x=month,y=[val_q,int_q,payment],
            title="Monthly payment, Capital Share and Interest Share Trend",
            labels={"x":"Month","value":"€"}
)
newnames = {'wide_variable_0':'Interest Share','wide_variable_1':'Capital Share','wide_variable_2':'Payment'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

fig.show()