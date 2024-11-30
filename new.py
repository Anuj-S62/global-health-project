import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.cm as cm



# Load the dataset
file = "csv_data/final3.csv"
df = pd.read_csv(file)

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Preprocessing
def preprocess(df):
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Convert columns to numeric
    cols_to_convert = [
        "Family history of diabetes", "Sex of the respondent",
        "Ever diagnosed_diabetes", "Working", "Age at last birthday", "Ever diagnosed_hypertension"
    ]
    df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors="coerce")
    df.dropna(inplace=True)

    # Replace 2 with 0 in "Ever diagnosed_diabetes" and "Ever diagnosed_hypertension"
    df["Ever diagnosed_diabetes"].replace({2: 0}, inplace=True)
    df["Ever diagnosed_hypertension"].replace({2: 0}, inplace=True)

    return df

df = preprocess(df)

# Separate data for males and females
df_male = df[df["Sex of the respondent"] == 1]
df_female = df[df["Sex of the respondent"] == 2]

# Gender-Specific Analysis
def gender_analysis(df_gender, gender_name, condition_col):
    print(f"\n### Analysis for {gender_name} ({condition_col.replace('_', ' ').capitalize()}) ###\n")

    # Total count
    total = len(df_gender)
    condition_count = df_gender[condition_col].sum()

    print(f"Total {gender_name}: {total}")
    print(f"With {condition_col}: {condition_count} ({(condition_count / total) * 100:.2f}%)")

    # Working Status and Condition
    working_status = df_gender.groupby("Working")[condition_col].mean()
    print("\nCondition Prevalence by Working Status:")
    print(working_status)

    # Age and Condition
    df_gender["Age Group"] = pd.cut(df_gender["Age at last birthday"], bins=[0, 40, 60, 100], labels=["<40", "40-60", ">60"])
    age_group_stats = df_gender.groupby("Age Group")[condition_col].mean()
    print("\nCondition Prevalence by Age Group:")
    print(age_group_stats)

    # Family History and Condition
    if condition_col == "Ever diagnosed_diabetes":
        family_history = df_gender[df_gender["Family history of diabetes"] == 1][condition_col].mean()
        print(f"\nCondition Prevalence with Family History: {family_history:.2f}")
    else:
        family_history = None

    # Plots
    plt.figure(figsize=(10, 6))
    sns.barplot(x=working_status.index, y=working_status.values, palette="viridis")
    plt.title(f"{condition_col.replace('_', ' ').capitalize()} Prevalence by Working Status ({gender_name})")
    plt.ylabel("Prevalence")
    plt.xlabel("Working Status (1 = Working, 2 = Not Working)")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=age_group_stats.index, y=age_group_stats.values, palette="coolwarm")
    plt.title(f"{condition_col.replace('_', ' ').capitalize()} Prevalence by Age Group ({gender_name})")
    plt.ylabel("Prevalence")
    plt.xlabel("Age Group")
    plt.show()

    return working_status, age_group_stats, family_history

# Perform Analysis for Males and Females
print("### Diabetes Analysis ###")
male_diabetes = gender_analysis(df_male, "Males", "Ever diagnosed_diabetes")
female_diabetes = gender_analysis(df_female, "Females", "Ever diagnosed_diabetes")

print("### Hypertension Analysis ###")
male_hypertension = gender_analysis(df_male, "Males", "Ever diagnosed_hypertension")
female_hypertension = gender_analysis(df_female, "Females", "Ever diagnosed_hypertension")

# Combined Analysis
def combined_analysis(df_gender, gender_name, condition_col):
    print(f"\n### Combined Analysis for {gender_name} ({condition_col.replace('_', ' ').capitalize()}) ###\n")

    # Combined Effect of Working and Living Location
    combined_work_location = df_gender.groupby(["Working", "Place of birth-village/town"])[condition_col].mean()
    print("\nCondition Prevalence by Working Status and Living Location:")
    print(combined_work_location)

    # Combined Effect of Working, Living Location, and Family History
    if condition_col == "Ever diagnosed_diabetes":
        combined_work_location_family = df_gender.groupby(["Working", "Place of birth-village/town", "Family history of diabetes"])[condition_col].mean()
        print("\nCondition Prevalence by Working Status, Living Location, and Family History:")
        print(combined_work_location_family)

    # Combined Effect of Age Group, Working, and Living Location
    df_gender["Age Group"] = pd.cut(df_gender["Age at last birthday"], bins=[40, 60, 80, 100], labels=["40-60", "60-80", ">80"])
    combined_age_work_location = df_gender.groupby(["Age Group", "Working", "Place of birth-village/town"])[condition_col].mean()
    print("\nCondition Prevalence by Age Group, Working Status, and Living Location:")
    print(combined_age_work_location)

    # Heatmap Plot
    plt.figure(figsize=(10, 6))
    sns.heatmap(combined_work_location.unstack(), annot=True, cmap="YlGnBu", fmt=".2f")
    plt.title(f"{condition_col.replace('_', ' ').capitalize()} Prevalence by Work & Living Location ({gender_name})")
    plt.xlabel("Place of Birth (1 = Village, 2 = Town)")
    plt.ylabel("Working Status (1 = Working, 2 = Not Working)")
    plt.show()

# Perform Combined Analysis for Males and Females
combined_analysis(df_male, "Males", "Ever diagnosed_diabetes")
combined_analysis(df_female, "Females", "Ever diagnosed_diabetes")

combined_analysis(df_male, "Males", "Ever diagnosed_hypertension")
combined_analysis(df_female, "Females", "Ever diagnosed_hypertension")

# Aggregate Data for Heatmap
def aggregate_state_data(df_gender, condition_col):
    return (
        df_gender.groupby("State")[condition_col]
        .mean()
        .reset_index()
        .rename(columns={condition_col: "Prevalence"})
    )

male_diabetes = aggregate_state_data(df_male, "Ever diagnosed_diabetes")
female_diabetes = aggregate_state_data(df_female, "Ever diagnosed_diabetes")

# Load India Shapefile
india_map = gpd.read_file("/Users/anujsolanki/global-health/india-polygon.shp")

# Merge Male and Female Data with India Shapefile
def merge_with_map(india_map, data, col_name):
    # Create a copy of the map
    merged_map = india_map.copy()
    
    # Normalize state names to handle potential variations
    def normalize_state_name(name):
        # Add any necessary name mappings here
        name_mappings = {
            'Jammu & Kashmir': 'Jammu and Kashmir',
            'Jammu and Kashmir': 'Jammu and Kashmir',
            'NCT of Delhi': 'Delhi'
        }
        return name_mappings.get(name, name)
    
    # Normalize state names in both datasets
    merged_map['st_nm'] = merged_map['st_nm'].apply(normalize_state_name)
    data['State'] = data['State'].apply(normalize_state_name)
    
    # Merge the data
    merged_map = merged_map.merge(data, left_on="st_nm", right_on="State", how="left")
    
    # Fill NaN values with 0
    merged_map['Prevalence'] = merged_map['Prevalence'].fillna(0)
    
    return merged_map

# Merge data
india_male = merge_with_map(india_map, male_diabetes, "Male Diabetes")
india_female = merge_with_map(india_map, female_diabetes, "Female Diabetes")

# Plot Heatmap with improved visualization
def plot_heatmap(india_data, title):
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Create a custom colormap with white for zero values
    cmap = cm.YlOrRd
    cmap.set_under('white')  # Color for values below the minimum
    
    # Normalize the color scale
    norm = colors.Normalize(vmin=india_data['Prevalence'].min(), vmax=india_data['Prevalence'].max())
    
    # Plot the map
    india_data.plot(
        column="Prevalence",
        cmap=cmap,
        norm=norm,
        linewidth=0.8,
        edgecolor='0.8',
        ax=ax,
        legend=True,
        legend_kwds={
            'label': 'Diabetes Prevalence',
            'orientation': 'horizontal'
        },
        missing_kwds={
            'color': 'lightgrey'  # Color for missing data
        }
    )
    
    # Add state labels
    for idx, row in india_data.iterrows():
        plt.annotate(
            text=f"{row['st_nm']}\n{row['Prevalence']:.2f}", 
            xy=(row.geometry.centroid.x, row.geometry.centroid.y),
            ha='center', 
            va='center',
            fontsize=6
        )
    
    ax.set_title(title, fontdict={'fontsize': 16}, loc="center")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Plot heatmaps
plot_heatmap(india_male, "Male Diabetes Prevalence by State")
plot_heatmap(india_female, "Female Diabetes Prevalence by State")