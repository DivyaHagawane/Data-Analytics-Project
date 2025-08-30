import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox

df = None  # global DataFrame

# Load Excel
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            messagebox.showinfo("Success", "File Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read file\n{e}")

# Clean data
def clean_data():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    after = df.shape[0]
    messagebox.showinfo("Cleaning Done", f"Removed {before - after} rows.")

# Analyze data
def analyze_data():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    try:
        total_patients = df['Patient_ID'].nunique()
        total_revenue = df['Treatment_Cost_USD'].sum()
        avg_bill = df['Treatment_Cost_USD'].mean()
        result.set(f"Total Patients: {total_patients}\n"
                   f"Total Revenue: ₹{total_revenue:,.0f}\n"
                   f"Average Bill: ₹{avg_bill:,.0f}")
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed\n{e}")

# Create charts
def create_charts():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    try:
        # Patients by Department
        df['Department'].value_counts().plot(kind='bar', title="Patients by Department")
        plt.show()

        # Revenue by Department
        df.groupby('Department')['Treatment_Cost_USD'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Revenue by Department")
        plt.ylabel("")
        plt.show()

        # Age distribution
        df['Age'].plot(kind='hist', bins=5, title="Age Distribution")
        plt.xlabel("Age")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Charts failed\n{e}")

# ---------------- GUI ----------------
root = Tk()
root.title("Hospital Data Analytics")
root.geometry("400x300")

Button(root, text="📂 Load File", command=load_file, width=20).pack(pady=5)
Button(root, text="🧹 Clean Data", command=clean_data, width=20).pack(pady=5)
Button(root, text="📊 Analyze Data", command=analyze_data, width=20).pack(pady=5)
Button(root, text="📈 Create Charts", command=create_charts, width=20).pack(pady=5)

result = StringVar()
Label(root, textvariable=result, bg="white", width=40, height=6, anchor="w", justify=LEFT).pack(pady=10)

root.mainloop()