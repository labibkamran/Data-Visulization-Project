import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Configuration
DATA_PATH = "/Users/robbannn/Desktop/SEM_5/DV_PROJECT/non-asher-cleaned/new/Consolidated (Educational Dataset).csv"
OUTPUT_DIR = "eda_output"
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

    # 1. Convert Percentage Columns
    for col in df.columns:
        if df[col].dtype == 'object':
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else ""
            if isinstance(sample, str) and '%' in sample:
                df[col] = df[col].str.rstrip('%').astype('float') / 100.0

    # 2. Convert other numeric columns
    numeric_cols = [
        'Education score', 'Learning score', 'Retention score', 'Gender parity score', 'School infrastructure score',
        'Bomb Blasts Occurred', 'Drone attacks in Pakistan', 'Terrorist Attacks Affectees',
        'Primary Schools with single classroom', 'Primary Schools with single teacher',
        'Toilet', 'Electricity', 'Drinking water', 'Boundary wall',
        'Total number of schools', 'Enrolment score'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Handle Missing Values (Median Imputation for numeric)
    numeric_df = df.select_dtypes(include=[np.number])
    df[numeric_df.columns] = numeric_df.fillna(numeric_df.median())

    return df

def generate_report_header():
    with open(REPORT_PATH, 'w') as f:
        f.write("# Expanded Automated EDA Report\n\n")
        f.write("## Dataset Overview\n")
        f.write("This report contains a deep dive into the educational dataset, covering distributions, geographic trends, cluster profiles, and multivariate interactions.\n\n")

def append_to_report(section_title, text, image_filenames=None):
    with open(REPORT_PATH, 'a') as f:
        f.write(f"### {section_title}\n\n")
        f.write(f"{text}\n\n")
        if image_filenames:
            if isinstance(image_filenames, str):
                image_filenames = [image_filenames]
            for img in image_filenames:
                rel_path = os.path.join("visualizations", img)
                f.write(f"![{section_title}]({rel_path})\n\n")

def analyze_distributions(df):
    print("Analyzing Distributions...")
    scores = ['Education score', 'Learning score', 'Retention score', 'Gender parity score', 'School infrastructure score']
    scores = [c for c in scores if c in df.columns]
    
    generated_plots = []
    
    # Histograms
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(scores, 1):
        plt.subplot(2, 3, i)
        sns.histplot(df[col], kde=True, bins=20)
        plt.title(f"Distribution of {col}")
    plt.tight_layout()
    filename = "score_distributions.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    generated_plots.append(filename)
    
    # Boxplots
    plt.figure(figsize=(15, 8))
    sns.boxplot(data=df[scores], orient='h')
    plt.title("Boxplots of Educational Scores")
    plt.tight_layout()
    filename = "score_boxplots.png"
    plt.savefig(os.path.join(VIS_DIR, filename))
    plt.close()
    generated_plots.append(filename)
    
    insight = "Analysis of score distributions. Histograms show the spread and skewness, while boxplots highlight outliers and central tendencies."
    append_to_report("Score Distributions", insight, generated_plots)

def analyze_geographic(df):
    print("Analyzing Geographic Trends...")
    
    if 'Province' not in df.columns:
        return

    # Average Scores by Province
    scores = ['Education score', 'School infrastructure score']
    scores = [c for c in scores if c in df.columns]
    
    for score in scores:
        plt.figure(figsize=(10, 6))
        province_avg = df.groupby('Province')[score].mean().sort_values(ascending=False).reset_index()
        sns.barplot(data=province_avg, x='Province', y=score, palette='viridis')
        plt.title(f"Average {score} by Province")
        plt.xticks(rotation=45)
        
        filename = f"avg_{score.replace(' ', '_')}_by_province.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        
        insight = f"Comparison of {score} across different provinces. Helps identify high and low performing regions."
        append_to_report(f"Geographic: {score} by Province", insight, filename)

    # Top/Bottom Cities
    if 'City' in df.columns and 'Education score' in df.columns:
        city_avg = df.groupby('City')['Education score'].mean().sort_values()
        
        # Bottom 10
        plt.figure(figsize=(10, 8))
        sns.barplot(x=city_avg.head(10).values, y=city_avg.head(10).index, palette='Reds_r')
        plt.title("Bottom 10 Cities by Education Score")
        plt.xlabel("Education Score")
        filename = "bottom_10_cities.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        
        # Top 10
        plt.figure(figsize=(10, 8))
        sns.barplot(x=city_avg.tail(10).values, y=city_avg.tail(10).index, palette='Greens_r')
        plt.title("Top 10 Cities by Education Score")
        plt.xlabel("Education Score")
        filename = "top_10_cities.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        
        insight = "Identification of the best and worst performing cities based on Education Score."
        append_to_report("City Performance Extremes", insight, ["top_10_cities.png", "bottom_10_cities.png"])

def analyze_clusters(df):
    print("Analyzing Clusters...")
    
    # Check for cluster column (could be 'Cluster' or similar)
    cluster_col = next((c for c in df.columns if 'cluster' in c.lower()), None)
    
    if cluster_col:
        print(f"Found cluster column: {cluster_col}")
        scores = ['Education score', 'School infrastructure score', 'Retention score', 'Learning score']
        scores = [c for c in scores if c in df.columns]
        
        if scores:
            # Melt for grouped bar plot
            cluster_avg = df.groupby(cluster_col)[scores].mean().reset_index()
            melted = cluster_avg.melt(id_vars=cluster_col, var_name='Metric', value_name='Score')
            
            plt.figure(figsize=(12, 6))
            sns.barplot(data=melted, x=cluster_col, y='Score', hue='Metric')
            plt.title("Average Scores by Cluster")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            
            filename = "cluster_profiles.png"
            plt.savefig(os.path.join(VIS_DIR, filename))
            plt.close()
            
            insight = f"Profile of different clusters based on key educational metrics. Shows distinct characteristics of each group."
            append_to_report("Cluster Profiling", insight, filename)

def analyze_multivariate(df):
    print("Analyzing Multivariate Interactions...")
    
    # Pairplot for key metrics
    key_metrics = ['Education score', 'School infrastructure score', 'Gender parity score', 'Retention score']
    key_metrics = [c for c in key_metrics if c in df.columns]
    
    if len(key_metrics) > 1:
        sns.pairplot(df[key_metrics].dropna(), kind='reg', plot_kws={'line_kws':{'color':'red'}, 'scatter_kws': {'alpha': 0.1}})
        plt.suptitle("Pairplot of Key Educational Metrics", y=1.02)
        
        filename = "key_metrics_pairplot.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        
        insight = "Pairwise relationships between key metrics. The regression lines indicate the direction and strength of trends."
        append_to_report("Multivariate Relationships", insight, filename)

    # Security x Infrastructure x Outcomes
    # Bubble plot: X=Infrastructure, Y=Education Score, Size=Bomb Blasts (if available)
    if 'School infrastructure score' in df.columns and 'Education score' in df.columns and 'Bomb Blasts Occurred' in df.columns:
        plt.figure(figsize=(10, 8))
        sns.scatterplot(
            data=df, 
            x='School infrastructure score', 
            y='Education score', 
            size='Bomb Blasts Occurred', 
            hue='Province' if 'Province' in df.columns else None,
            sizes=(20, 500), 
            alpha=0.6,
            palette='deep'
        )
        plt.title("Infrastructure vs Education Score (Bubble Size = Bomb Blasts)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        filename = "bubble_infra_edu_security.png"
        plt.savefig(os.path.join(VIS_DIR, filename))
        plt.close()
        
        insight = "Multidimensional view: Infrastructure vs Education Score, with bubble size representing security incidents. Large bubbles in low-score areas suggest security impact."
        append_to_report("Security Impact Bubble Plot", insight, filename)

def analyze_enrolment(df):
    # Re-using previous logic but enhancing
    print("Analyzing Enrolment...")
    if '% Boys Enrolled' in df.columns and '% Girls Enrolled' in df.columns:
        # 1. Trend over years
        if 'Year' in df.columns:
            yearly = df.groupby('Year')[['% Boys Enrolled', '% Girls Enrolled']].mean().reset_index()
            melted = yearly.melt('Year', var_name='Gender', value_name='Percentage')
            
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=melted, x='Year', y='Percentage', hue='Gender', marker='o')
            plt.title("Enrolment Trends: Boys vs Girls")
            plt.ylim(0, 1)
            filename = "enrolment_trend_line.png"
            plt.savefig(os.path.join(VIS_DIR, filename))
            plt.close()
            append_to_report("Enrolment Trends", "Line chart showing the progression of enrolment percentages over time.", filename)

def main():
    generate_report_header()
    
    df = load_and_clean_data(DATA_PATH)
    if df is None:
        return

    analyze_distributions(df)
    analyze_geographic(df)
    analyze_clusters(df)
    analyze_multivariate(df)
    analyze_enrolment(df) # Enhanced version
    
    print(f"Expanded analysis complete. Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
