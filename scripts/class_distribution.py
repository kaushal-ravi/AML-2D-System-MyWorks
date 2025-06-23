import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def check_class_distribution(input_path=r"C:\AML-kaushal\AML-2D-System-MyWorks\AML_project\cleaned_master_data.csv"):
    df = pd.read_csv(input_path)

    if 'shape_type' not in df.columns:
        print("Error: 'shape_type' column not found.")
        return

    print("\nClass Distribution:")
    print(df['shape_type'].value_counts())

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.countplot(x='shape_type', data=df, palette='Set2')
    plt.title("Shape Type Distribution")
    plt.xlabel("Shape Type")
    plt.ylabel("Count")
    plt.tight_layout()

    # Create 'outputs' folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)

    plt.savefig("outputs/class_distribution.png")
    plt.show()

if __name__ == "__main__":
    check_class_distribution()
