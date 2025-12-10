import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Configuration
DATA_PATH = "/Users/robbannn/Desktop/SEM_5/DV_PROJECT/public-census_oct_2018.csv"
OUTPUT_DIR = "advanced_census_eda_output"
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
    
    # Numeric conversion & Filling
    cols_to_numeric = ['Teachers', 'enrollment', 'functional_classrooms', 'total_rooms', 
                       'total_toilets', 'usable_toilets', 'total_computers', 'est_year',
                       'dangerous_classrooms', 'total_area_marla', 'total_area_kanal']
    
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Binary/Categorical encoding for facilities (Assuming 1=Yes based on previous inspection)
    facilities = ['electricity', 'drink_water', 'toilets', 'boundary_wall', 'play_ground', 
                  'library', 'science_lab', 'computer_lab', 'internet']
    
    for fac in facilities:
        if fac in df.columns:
            # Ensure it's numeric 0/1. If it's string 'Yes'/'No', map it.
            # Based on previous head, they looked like 1.0 or NaN/0.0
            df[fac] = pd.to_numeric(df[fac], errors='coerce').fillna(0)

    # Building Condition Mapping
    if 'bldg_condition' in df.columns:
        # Map to numeric score for index calculation
        condition_map = {
            'Satisfying': 3,
            'Needed Minor Repairing': 2,
            'Needed Major Repairing': 1,
            'Dangerous': 0,
            'Under Construction': 1
        }
        df['bldg_condition_score'] = df['bldg_condition'].map(condition_map).fillna(0)

    return df

def generate_report_header():
    with open(REPORT_PATH, 'w') as f:
        f.write("# Advanced Census EDA Report\n\n")
        f.write("## Overview\n")
        f.write("Analysis of 16 specific questions regarding school quality, infrastructure, and outcomes.\n\n")

def append_to_report(section_title, text, image_filename=None):
    with open(REPORT_PATH, 'a') as f:
        f.write(f"### {section_title}\n\n")
        f.write(f"{text}\n\n")
        if image_filename:
            rel_path = os.path.join("visualizations", image_filename)
            f.write(f"![{section_title}]({rel_path})\n\n")

# --- Analysis Functions ---

def q1_constituency_quality(df):
    print("Q1: Constituency Quality Comparison...")
    # Quality Index Components
    # 1. Building Condition Score (already created)
    # 2. Functional Classrooms per Enrollment
    df['fc_per_student'] = df.apply(lambda x: x['functional_classrooms'] / x['enrollment'] if x['enrollment'] > 0 else 0, axis=1)
    
    # 3. Available Facilities Score
    fac_cols = ['drink_water', 'electricity', 'toilets', 'boundary_wall', 'play_ground']
    df['basic_facilities_score'] = df[fac_cols].sum(axis=1)
    
    # 4. Teachers & Staff
    # Normalize teachers
    df['teachers_norm'] = (df['Teachers'] - df['Teachers'].min()) / (df['Teachers'].max() - df['Teachers'].min() + 1e-5)
    
    # 5. Lab/Lib/Comp Access
    adv_fac_cols = ['library', 'science_lab', 'computer_lab', 'internet']
    df['adv_facilities_score'] = df[adv_fac_cols].sum(axis=1)
    
    # Composite Index (Simple weighted sum for EDA)
    # Normalize components first to 0-1 scale
    scaler = StandardScaler()
    components = ['bldg_condition_score', 'fc_per_student', 'basic_facilities_score', 'teachers_norm', 'adv_facilities_score']
    
    # Handle NaNs in components
    df[components] = df[components].fillna(0)
    
    # Create index
    df['Quality_Index'] = df[components].mean(axis=1)
    
    # Group by NA
    if 'na_no' in df.columns:
        na_quality = df.groupby('na_no')['Quality_Index'].mean().sort_values(ascending=False).head(20)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x=na_quality.values, y=na_quality.index.astype(str))
        plt.title("Top 20 National Assembly Constituencies by School Quality Index")
        plt.xlabel("Average Quality Index")
        plt.ylabel("NA Number")
        filename = "q1_na_quality_index.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("1. Constituency Quality Comparison", "Top 20 constituencies with the highest overall school quality index.", filename)

def q2_functional_predictors(df):
    print("Q2: Functional vs Non-functional Predictors...")
    if 'school_status' not in df.columns: return
    
    # Target: Functional (1) vs Non-functional (0)
    df['is_functional'] = df['school_status'].apply(lambda x: 1 if str(x).lower() == 'functional' else 0)
    
    features = ['bldg_condition_score', 'electricity', 'Teachers', 'drink_water', 'boundary_wall']
    # Encode categorical location/level
    le = LabelEncoder()
    if 'school_location' in df.columns:
        df['loc_encoded'] = le.fit_transform(df['school_location'].astype(str))
        features.append('loc_encoded')
    if 'school_level' in df.columns:
        df['level_encoded'] = le.fit_transform(df['school_level'].astype(str))
        features.append('level_encoded')
        
    X = df[features].fillna(0)
    y = df['is_functional']
    
    if len(y.unique()) > 1:
        rf = RandomForestClassifier(n_estimators=50, random_state=42)
        rf.fit(X, y)
        
        importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=importances.values, y=importances.index)
        plt.title("Feature Importance: Predicting School Functionality")
        filename = "q2_functional_predictors.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("2. Predictors of Functionality", "Factors most strongly predicting whether a school is Functional.", filename)

def q3_under_resourced_districts(df):
    print("Q3: Under-resourced Districts...")
    if 'district' not in df.columns: return
    
    # Normalize resources
    # Resource metric: Total Facilities / Enrollment (proxy for per-student resource)
    # Avoid div by zero
    df['resources_per_student'] = df['basic_facilities_score'] / (df['enrollment'] + 1)
    
    district_res = df.groupby('district')['resources_per_student'].mean().sort_values().head(20)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=district_res.values, y=district_res.index, palette="Reds_r")
    plt.title("Top 20 Most Under-resourced Districts (Per Student Facilities)")
    plt.xlabel("Normalized Resource Score")
    filename = "q3_under_resourced.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("3. Under-resourced Districts", "Districts with the lowest facilities per student ratio.", filename)

def q4_infra_gender_correlation(df):
    print("Q4: Infrastructure vs Gender Enrollment...")
    # Focus on Rural schools
    rural = df[df['school_location'] == 'Rural'].copy()
    
    # Compare facilities in Male vs Female schools
    facs = ['toilets', 'boundary_wall', 'functional_classrooms']
    
    melted = rural.melt(id_vars=['school_gender'], value_vars=facs, var_name='Facility', value_name='Count')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=melted, x='Facility', y='Count', hue='school_gender', ci=None)
    plt.title("Facility Availability in Rural Schools by Gender")
    filename = "q4_infra_gender.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("4. Infrastructure vs Gender (Rural)", "Comparison of key facilities in rural Male vs Female schools.", filename)

def q5_upgraded_strain(df):
    print("Q5: Upgraded Schools Strain...")
    # Identify upgraded schools (if upgrade year is present and > 0)
    upgrade_cols = ['upgrade_primary_year', 'upgrade_middle_year', 'upgrade_high_year']
    # Check if any upgrade col has valid year
    df['is_upgraded'] = df[upgrade_cols].apply(lambda x: x.max() > 0, axis=1)
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='is_upgraded', y='dangerous_classrooms', showfliers=False)
    plt.title("Dangerous Classrooms: Upgraded vs Non-Upgraded Schools")
    plt.xticks([0, 1], ['Non-Upgraded', 'Upgraded'])
    filename = "q5_upgraded_strain.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("5. Upgraded Schools Strain", "Comparison of dangerous classroom counts in upgraded vs non-upgraded schools.", filename)

def q6_lab_predictors(df):
    print("Q6: Lab Availability Predictors...")
    # Correlation of labs with potential predictors
    labs = ['science_lab', 'physics_lab', 'chemistry_lab', 'biology_lab']
    predictors = ['enrollment', 'Teachers', 'total_rooms', 'bldg_condition_score']
    
    # Ensure cols exist
    valid_labs = [c for c in labs if c in df.columns]
    valid_preds = [c for c in predictors if c in df.columns]
    
    if valid_labs and valid_preds:
        corr = df[valid_labs + valid_preds].corr().loc[valid_labs, valid_preds]
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title("Correlation: Lab Availability vs Predictors")
        filename = "q6_lab_predictors.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("6. Lab Predictors", "Correlation between lab availability and school size/infrastructure metrics.", filename)

def q7_teacher_furniture(df):
    print("Q7: Teacher Furniture vs Outcomes...")
    if 'teachers_with_furniture' in df.columns:
        df['teachers_with_furniture'] = pd.to_numeric(df['teachers_with_furniture'], errors='coerce').fillna(0)
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='teachers_with_furniture', y='enrollment', alpha=0.3)
        plt.title("Teachers with Furniture vs Enrollment")
        plt.xlim(0, 50)
        plt.ylim(0, 2000)
        filename = "q7_teacher_furniture.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("7. Teacher Furniture Impact", "Relationship between teachers having furniture and student enrollment.", filename)

def q8_security_female_enrollment(df):
    print("Q8: Security vs Female Enrollment...")
    # Filter for Female schools
    female_schools = df[df['school_gender'] == 'Female'].copy()
    
    if not female_schools.empty:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=female_schools, x='boundary_wall', y='enrollment', showfliers=False)
        plt.title("Female School Enrollment: With vs Without Boundary Wall")
        plt.xticks([0, 1], ['No Wall', 'Has Wall'])
        filename = "q8_security_female.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("8. Security & Female Enrollment", "Impact of boundary walls on enrollment in female schools.", filename)

def q9_facilities_retention(df):
    print("Q9: Facilities vs Teacher Retention (Proxy)...")
    # Proxy: Head Type (Permanent vs Contract/Acting)
    if 'head_type' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='head_type', y='basic_facilities_score')
        plt.title("Basic Facilities Score by Head Teacher Type")
        filename = "q9_facilities_head_type.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("9. Facilities vs Teacher Retention", "Association between facility quality and head teacher status (Permanent vs Temporary).", filename)

def q10_spatial_disparities(df):
    print("Q10: Spatial Disparities (Dangerous Classrooms)...")
    if 'tehsil' in df.columns:
        # % Dangerous classrooms
        df['pct_dangerous'] = df.apply(lambda x: x['dangerous_classrooms'] / x['total_rooms'] if x['total_rooms'] > 0 else 0, axis=1)
        
        tehsil_danger = df.groupby('tehsil')['pct_dangerous'].mean().sort_values(ascending=False).head(15)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x=tehsil_danger.values, y=tehsil_danger.index, palette="magma")
        plt.title("Top 15 Tehsils by % Dangerous Classrooms")
        plt.xlabel("Percentage Dangerous")
        filename = "q10_spatial_danger.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("10. Spatial Disparities", "Tehsils with the highest percentage of dangerous classrooms.", filename)

def q11_land_vs_functionality(df):
    print("Q11: Land Area vs Functionality...")
    # Use total_area_marla as metric
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='total_area_marla', y='functional_classrooms', alpha=0.3)
    plt.title("Total Land Area (Marla) vs Functional Classrooms")
    plt.xlim(0, 200) # Limit for visibility
    plt.ylim(0, 30)
    filename = "q11_land_functionality.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("11. Land vs Functionality", "Relationship between available land area and actual functional classrooms.", filename)

def q12_playground_impact(df):
    print("Q12: Playground Impact on Higher Enrollment...")
    # Filter Middle/High schools
    higher_levels = ['Middle', 'High', 'High Secondary']
    subset = df[df['school_level'].isin(higher_levels)].copy()
    
    if not subset.empty:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=subset, x='play_ground', y='enrollment', showfliers=False)
        plt.title("Enrollment in Higher Level Schools: Playground vs No Playground")
        plt.xticks([0, 1], ['No Playground', 'Has Playground'])
        filename = "q12_playground_impact.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("12. Playground Impact", "Enrollment differences in Middle/High schools based on playground availability.", filename)

def q13_clustering(df):
    print("Q13: School Clustering...")
    # Features for clustering
    features = ['enrollment', 'Teachers', 'basic_facilities_score', 'bldg_condition_score']
    X = df[features].fillna(0)
    
    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df['cluster'] = clusters
    
    # PCA for visualization
    pca = PCA(n_components=2)
    pca_res = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=pca_res[:,0], y=pca_res[:,1], hue=clusters, palette='viridis', alpha=0.6)
    plt.title("School Clusters (PCA Visualization)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    filename = "q13_clustering.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("13. School Clustering", "Clustering of schools based on infrastructure, enrollment, and teachers.", filename)

def q14_internet_predictors(df):
    print("Q14: Internet Access Predictors...")
    # Simple bar of internet access by location and level
    if 'internet' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='school_level', y='internet', hue='school_location', ci=None)
        plt.title("Internet Access by Level and Location")
        plt.ylabel("Proportion with Internet")
        filename = "q14_internet_access.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("14. Internet Access Predictors", "Internet availability breakdown by school level and urban/rural location.", filename)

def q15_str_vs_facilities(df):
    print("Q15: Student-Teacher Ratio vs Facilities...")
    # Calculate STR
    df['str'] = df.apply(lambda x: x['enrollment'] / x['Teachers'] if x['Teachers'] > 0 else 0, axis=1)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='basic_facilities_score', y='str', alpha=0.1)
    plt.title("Student-Teacher Ratio vs Basic Facilities Score")
    plt.ylim(0, 100)
    filename = "q15_str_facilities.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    append_to_report("15. STR vs Facilities", "Relationship between facility completeness and student-teacher ratio.", filename)

def q16_age_vs_infra(df):
    print("Q16: Old vs New Schools Infrastructure...")
    if 'est_year' in df.columns:
        df['is_old'] = df['est_year'] < 1980
        
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x='is_old', y='bldg_condition_score', ci=None)
        plt.title("Building Condition Score: Old (<1980) vs New Schools")
        plt.xticks([0, 1], ['New', 'Old'])
        filename = "q16_age_infra.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        append_to_report("16. Age vs Infrastructure", "Comparison of building condition scores between schools established before and after 1980.", filename)

def main():
    generate_report_header()
    
    df = load_and_clean_data(DATA_PATH)
    if df is None:
        return

    # Execute all questions
    q1_constituency_quality(df)
    q2_functional_predictors(df)
    q3_under_resourced_districts(df)
    q4_infra_gender_correlation(df)
    q5_upgraded_strain(df)
    q6_lab_predictors(df)
    q7_teacher_furniture(df)
    q8_security_female_enrollment(df)
    q9_facilities_retention(df)
    q10_spatial_disparities(df)
    q11_land_vs_functionality(df)
    q12_playground_impact(df)
    q13_clustering(df)
    q14_internet_predictors(df)
    q15_str_vs_facilities(df)
    q16_age_vs_infra(df)
    
    print(f"Advanced Census EDA complete. Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
