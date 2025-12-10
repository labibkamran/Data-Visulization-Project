import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Configuration
DATA_PATH = "/Users/robbannn/Desktop/SEM_5/DV_PROJECT/public-census_oct_2018.csv"
OUTPUT_DIR = "census_eda_output"
VIS_DIR = os.path.join(OUTPUT_DIR, "visualizations")
REPORT_PATH = os.path.join(OUTPUT_DIR, "report.md")

# Ensure output directories exist
os.makedirs(VIS_DIR, exist_ok=True)

# Set plot style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

    print("Initial shape:", df.shape)
    
    # Handle missing values for key columns
    df['Teachers'] = pd.to_numeric(df['Teachers'], errors='coerce').fillna(0)
    df['enrollment'] = pd.to_numeric(df['enrollment'], errors='coerce').fillna(0)
    
    # Create derived metrics
    df['Student_Teacher_Ratio'] = df.apply(lambda x: x['enrollment'] / x['Teachers'] if x['Teachers'] > 0 else 0, axis=1)
    
    return df

def generate_report_header():
    with open(REPORT_PATH, 'w') as f:
        f.write("# Census Data EDA Report\n\n")
        f.write("## Dataset Overview\n")
        f.write("This report provides a comprehensive analysis of the October 2018 Public Census data, focusing on school infrastructure, enrollment, and facilities.\n\n")

def append_to_report(section_title, text, image_filename=None):
    with open(REPORT_PATH, 'a') as f:
        f.write(f"### {section_title}\n\n")
        f.write(f"{text}\n\n")
        if image_filename:
            rel_path = os.path.join("visualizations", image_filename)
            f.write(f"![{section_title}]({rel_path})\n\n")

def generate_visuals(df):
    print("Generating visuals...")
    
    # 1. School Level Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='school_level', order=df['school_level'].value_counts().index)
    plt.title("Distribution of Schools by Level")
    plt.xticks(rotation=45)
    filename = "1_school_level_dist.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("School Level Distribution", "Count of schools across different levels (Primary, Middle, High, etc.).", filename)

    # 2. Urban vs Rural Enrollment
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='school_location', y='enrollment', estimator=sum, ci=None)
    plt.title("Total Enrollment: Urban vs Rural")
    filename = "2_urban_rural_enrollment.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("Urban vs Rural Enrollment", "Comparison of total student enrollment in Urban vs Rural areas.", filename)

    # 3. Gender Distribution
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='school_gender')
    plt.title("Distribution of Schools by Gender")
    filename = "3_school_gender_dist.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("School Gender Distribution", "Breakdown of schools designated for Male, Female, or Both.", filename)

    # 4. Building Condition
    plt.figure(figsize=(10, 6))
    df['bldg_condition'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title("School Building Condition")
    plt.ylabel('')
    filename = "4_bldg_condition.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("Building Condition", "Proportion of schools with varying building conditions.", filename)

    # 5. Basic Facilities Access
    facilities = ['electricity', 'drink_water', 'toilets', 'boundary_wall']
    # Ensure columns are numeric/boolean (1/0 or Yes/No mapped)
    # Assuming 1=Yes, 0=No based on typical census data, or check unique values
    # Based on head output: electricity=1, drink_water=1, etc.
    
    access_rates = {}
    for fac in facilities:
        if fac in df.columns:
            access_rates[fac] = df[fac].mean() * 100 # Assuming 1/0 coding
            
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(access_rates.keys()), y=list(access_rates.values()))
    plt.title("Percentage of Schools with Basic Facilities")
    plt.ylabel("Percentage (%)")
    filename = "5_basic_facilities.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("Basic Facilities Access", "Percentage of schools possessing key facilities like Electricity, Water, Toilets, and Boundary Walls.", filename)

    # 6. Student-Teacher Ratio by District (Top 20)
    if 'district' in df.columns:
        district_str = df.groupby('district')['Student_Teacher_Ratio'].mean().sort_values(ascending=False).head(20)
        plt.figure(figsize=(12, 8))
        sns.barplot(x=district_str.values, y=district_str.index)
        plt.title("Average Student-Teacher Ratio by District (Top 20 Highest)")
        filename = "6_str_by_district.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Student-Teacher Ratio by District", "Districts with the highest average Student-Teacher Ratios, indicating potential teacher shortages.", filename)

    # 7. Classroom Availability
    plt.figure(figsize=(10, 6))
    sns.histplot(df['functional_classrooms'], bins=30, kde=True)
    plt.title("Distribution of Functional Classrooms per School")
    plt.xlim(0, 20) # Limit x-axis for better visibility of common range
    filename = "7_classroom_dist.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("Classroom Availability", "Histogram showing the distribution of functional classrooms available in schools.", filename)

    # 8. Computer Lab Availability by Level
    if 'computer_lab' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='school_level', y='computer_lab', ci=None)
        plt.title("Computer Lab Availability by School Level")
        plt.ylabel("Proportion with Computer Lab")
        filename = "8_computer_lab_level.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Computer Lab Availability", "Proportion of schools with computer labs across different education levels.", filename)

    # 9. Library Availability by Level
    if 'library' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='school_level', y='library', ci=None)
        plt.title("Library Availability by School Level")
        plt.ylabel("Proportion with Library")
        filename = "9_library_level.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Library Availability", "Proportion of schools with libraries across different education levels.", filename)

    # 10. Enrollment vs Teachers
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Teachers', y='enrollment', alpha=0.3)
    plt.title("Enrollment vs Number of Teachers")
    plt.xlim(0, 100)
    plt.ylim(0, 3000)
    filename = "10_enrollment_vs_teachers.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("Enrollment vs Teachers", "Scatter plot showing the relationship between student enrollment and teacher count.", filename)

    # 11. Electricity Source
    if 'electricity_source' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, y='electricity_source', order=df['electricity_source'].value_counts().index)
        plt.title("Sources of Electricity in Schools")
        filename = "11_electricity_source.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Electricity Source", "Breakdown of electricity sources (e.g., WAPDA, Solar) used by schools.", filename)

    # 12. Drinking Water Source
    if 'drink_water_type' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, y='drink_water_type', order=df['drink_water_type'].value_counts().index)
        plt.title("Types of Drinking Water Sources")
        filename = "12_water_source.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Drinking Water Source", "Common sources of drinking water in schools.", filename)

    # 13. Playground Availability: Urban vs Rural
    if 'play_ground' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x='school_location', y='play_ground', ci=None)
        plt.title("Playground Availability: Urban vs Rural")
        plt.ylabel("Proportion with Playground")
        filename = "13_playground_urban_rural.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Playground Availability", "Comparison of playground availability in Urban vs Rural schools.", filename)

    # 14. School Status
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='school_status')
    plt.title("School Functional Status")
    filename = "14_school_status.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("School Status", "Count of functional vs non-functional schools.", filename)

    # 15. Establishment Year Trend
    if 'est_year' in df.columns:
        # Filter valid years (e.g., > 1800 and <= current year)
        valid_years = df[(df['est_year'] > 1800) & (df['est_year'] <= 2024)]
        plt.figure(figsize=(12, 6))
        sns.histplot(valid_years['est_year'], bins=50, kde=True)
        plt.title("Distribution of School Establishment Years")
        plt.xlabel("Year")
        filename = "15_est_year_trend.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("Establishment Year Trend", "Timeline showing when schools were established, highlighting periods of rapid expansion.", filename)

def main():
    generate_report_header()
    
    df = load_and_clean_data(DATA_PATH)
    if df is None:
        return

    generate_visuals(df)
    
    print(f"Census EDA complete. Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
