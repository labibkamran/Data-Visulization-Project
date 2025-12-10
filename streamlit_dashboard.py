"""
Interactive School Performance Dashboard with Exploratory Analysis
Built with Streamlit and Plotly for comprehensive data visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title=" School Performance Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: 45px; padding: 0 15px; font-size: 14px; }
    h1, h2, h3 { color: #1E3A5F; }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def normalize(series):
    """Normalize a series to 0-1 range"""
    series = pd.to_numeric(series, errors="coerce").fillna(0)
    if series.max() == series.min():
        return series * 0
    return (series - series.min()) / (series.max() - series.min())

def encode_bldg_condition(x):
    """Encode building condition to score"""
    if pd.isna(x): return np.nan
    s = str(x).lower()
    if "satisf" in s or "good" in s: return 1.0
    if "minor" in s or "needed" in s: return 0.5
    if "bad" in s or "rough" in s or "major" in s: return 0.0
    return np.nan

def label_readiness(score):
    """Label lab readiness based on score"""
    if score <= 3: return "Very Low"
    elif score <= 7: return "Low"
    elif score <= 11: return "Medium"
    elif score <= 15: return "High"
    else: return "Excellent"

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_and_prepare_data():
    """Load and prepare the dataset with all score calculations"""
    csv_path = "/Users/robbannn/Desktop/SEM_5/DV_PROJECT/public-census_oct_2018.csv"
    df = pd.read_csv(csv_path, low_memory=False)
    df.columns = df.columns.str.strip()
    
    # Convert necessary columns to numeric
    numeric_cols = [
        "total_rooms", "functional_classrooms", "usable_toilets", "total_toilets",
        "dangerous_classrooms", "dangerous_non_classrooms", "electricity",
        "drink_water", "main_gate", "boundary_wall_state", "security",
        "play_ground", "library", "science_lab", "computer_lab", "internet", 
        "pp_no", "na_no", "enrollment", "Teachers", "NonTeachers",
        "total_computers", "total_computer_training_students", "est_year",
        "need_repairing_toilets", "sewerage", "toilets",
        "physics_lab", "biology_lab", "chemistry_lab", "home_economic_lab",
        "physics_appratus", "biology_appratus", "chemistry_appratus",
        "home_economic_appratus", "combine_lab", "combine_appratus",
        "cricket", "football", "hockey", "badminton", "volleyball", "table_tennis"
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Clean binary columns
    binary_fix = ["electricity", "drink_water", "boundary_wall_state", "main_gate"]
    for col in binary_fix:
        if col in df.columns:
            df[col] = df[col].replace({2: 0, 3: 0})
    
    # Derived metrics
    df['students_per_classroom'] = df.apply(
        lambda r: r['enrollment'] / r['functional_classrooms'] 
        if r['functional_classrooms'] > 0 else np.nan, axis=1
    )
    
    df['usable_toilets_per_100'] = df.apply(
        lambda r: (r['usable_toilets'] / r['enrollment'] * 100) 
        if r['enrollment'] > 0 else np.nan, axis=1
    )
    
    df['computers_per_100'] = df.apply(
        lambda r: (r['total_computers'] / r['enrollment'] * 100) 
        if r['enrollment'] > 0 else np.nan, axis=1
    )
    
    # Building condition score
    if 'bldg_condition' in df.columns:
        df['bldg_condition_score'] = df['bldg_condition'].apply(encode_bldg_condition)
    
    # School Quality Index
    df['toilets_scaled'] = df['usable_toilets_per_100'].clip(0, 10) / 10
    df['computers_scaled'] = df['computers_per_100'].clip(0, 10) / 10
    
    df['school_quality_index'] = (
        0.25 * df['bldg_condition_score'].fillna(0) +
        0.20 * df['toilets_scaled'].fillna(0) +
        0.25 * normalize(df['students_per_classroom'].fillna(50)) +
        0.15 * df['computers_scaled'].fillna(0) +
        0.10 * df['library'].fillna(0) +
        0.05 * df['electricity'].fillna(0)
    )
    
    # Lab readiness
    lab_cols = ["physics_lab", "biology_lab", "chemistry_lab", "home_economic_lab",
                "physics_appratus", "biology_appratus", "chemistry_appratus",
                "home_economic_appratus", "combine_lab", "combine_appratus", "computer_lab"]
    for col in lab_cols:
        if col not in df.columns:
            df[col] = 0
    df["lab_score"] = df[lab_cols].sum(axis=1)
    df["lab_readiness"] = df["lab_score"].apply(label_readiness)
    
    # Performance scores
    df["Infrastructure_Score"] = (
        0.20 * normalize(df["total_rooms"]) +
        0.20 * normalize(df["functional_classrooms"] / df["total_rooms"].replace(0, 1)) +
        0.20 * df["electricity"].fillna(0) +
        0.20 * df["drink_water"].fillna(0) +
        0.10 * df["usable_toilets"].fillna(0) +
        0.10 * df["main_gate"].fillna(0)
    ) * 100
    
    df["Safety_Score"] = (
        0.30 * (1 - normalize(df["dangerous_classrooms"])) +
        0.20 * (1 - normalize(df["dangerous_non_classrooms"])) +
        0.20 * df["boundary_wall_state"].fillna(0) +
        0.20 * df["main_gate"].fillna(0) +
        0.10 * df["security"].fillna(0)
    ) * 100
    
    df["Facilities_Score"] = (
        0.20 * df["play_ground"].fillna(0) +
        0.20 * df["library"].fillna(0) +
        0.20 * df["science_lab"].fillna(0) +
        0.15 * df["computer_lab"].fillna(0) +
        0.15 * df["internet"].fillna(0)
    ) * 100
    
    df["Total_Performance"] = (
        0.40 * df["Infrastructure_Score"] +
        0.30 * df["Safety_Score"] +
        0.30 * df["Facilities_Score"]
    ) / 100
    
    # Teacher-student ratio
    df["ts_ratio"] = df["enrollment"] / df["Teachers"].replace(0, np.nan)
    df["ts_ratio"] = df["ts_ratio"].replace([np.inf, -np.inf], np.nan)
    
    # Clean IDs and text
    if "school_id" not in df.columns:
        df["school_id"] = df.index
    
    df["district"] = df["district"].fillna("Unknown").astype(str)
    df["school_level"] = df["school_level"].fillna("Unknown").astype(str)
    df["school_name"] = df["school_name"].fillna("Unknown").astype(str)
    df["pp_no"] = df["pp_no"].fillna(0).astype(int)
    
    if "school_gender" in df.columns:
        df["school_gender"] = df["school_gender"].fillna("Unknown").astype(str)
    if "school_shift" in df.columns:
        df["school_shift"] = df["school_shift"].fillna("Unknown").astype(str)
    if "school_location" in df.columns:
        df["school_location"] = df["school_location"].fillna("Unknown").astype(str)
    if "medium" in df.columns:
        df["medium"] = df["medium"].fillna("Unknown").astype(str)
    
    return df

# ============================================================
# PLOT FUNCTIONS
# ============================================================
def create_horizontal_bar(data, score_col, title, color_scale="Greens"):
    """Create interactive horizontal bar chart"""
    data = data.copy()
    data["label"] = (
        data["school_name"].str[:30] + " | PP-" + 
        data["pp_no"].astype(str) + " | " + data["district"]
    )
    data = data.sort_values(score_col, ascending=True)
    
    colors = px.colors.sequential.Greens[3:] if color_scale == "Greens" else px.colors.sequential.Reds[3:]
    n_bars = len(data)
    bar_colors = [colors[min(i * len(colors) // n_bars, len(colors) - 1)] for i in range(n_bars)]
    
    fig = go.Figure(go.Bar(
        y=data["label"], x=data[score_col], orientation='h',
        marker=dict(color=bar_colors),
        text=data[score_col].round(2), textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{x:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        height=max(350, len(data) * 35),
        margin=dict(l=10, r=10, t=40, b=30),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    return fig

def get_top_bottom(df, score_col, n):
    """Get top n and bottom n (non-zero) schools"""
    top = df.nlargest(n, score_col)
    bottom = df[df[score_col] > 0].nsmallest(n, score_col)
    return top, bottom

# ============================================================
# MAIN APP
# ============================================================
def main():
    st.title("🏫 School Performance Dashboard")
    st.markdown("### Comprehensive Analysis with Exploratory Data Analysis")
    
    try:
        df = load_and_prepare_data()
        st.success(f"Loaded **{len(df):,}** schools")
    except Exception as e:
        st.error(f" Error: {e}")
        st.stop()
    
    # ============================================================
    # SIDEBAR
    # ============================================================
    st.sidebar.header("🔍 Filters")
    
    selected_districts = st.sidebar.multiselect(
        "District(s)", ["All"] + sorted(df["district"].unique().tolist()), default=["All"]
    )
    selected_levels = st.sidebar.multiselect(
        "School Level(s)", ["All"] + sorted(df["school_level"].unique().tolist()), default=["All"]
    )
    num_schools = st.sidebar.slider("Top/Bottom Schools", 3, 20, 10)
    
    # Apply filters
    filtered_df = df.copy()
    if "All" not in selected_districts:
        filtered_df = filtered_df[filtered_df["district"].isin(selected_districts)]
    if "All" not in selected_levels:
        filtered_df = filtered_df[filtered_df["school_level"].isin(selected_levels)]
    
    st.sidebar.metric("Filtered Schools", f"{len(filtered_df):,}")
    
    # ============================================================
    # SUMMARY METRICS
    # ============================================================
    st.markdown("---")
    cols = st.columns(4)
    metrics = [
        ("🏗️ Infrastructure", "Infrastructure_Score"),
        ("🛡️ Safety", "Safety_Score"),
        ("🎓 Facilities", "Facilities_Score"),
        ("🏆 Total", "Total_Performance")
    ]
    for col, (label, score_col) in zip(cols, metrics):
        avg = filtered_df[score_col].mean()
        col.metric(label, f"{avg:.1f}", f"{avg - df[score_col].mean():.1f}")
    
    # ============================================================
    # MAIN TABS
    # ============================================================
    main_tabs = st.tabs([
        " Performance Scores",
        " Exploratory Analysis"
    ])
    
    # ==================== TAB 1: PERFORMANCE SCORES ====================
    with main_tabs[0]:
        perf_tabs = st.tabs(["Overview", "Infrastructure", "Safety", "Facilities", "Total", "Correlations"])
        
        # Overview
        with perf_tabs[0]:
            st.header("Score Distributions")
            fig = make_subplots(rows=2, cols=2, subplot_titles=[
                'Infrastructure', 'Safety', 'Facilities', 'Total Performance'
            ])
            scores = ['Infrastructure_Score', 'Safety_Score', 'Facilities_Score', 'Total_Performance']
            colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
            for i, (score, color) in enumerate(zip(scores, colors)):
                fig.add_trace(go.Histogram(x=filtered_df[score], marker_color=color, opacity=0.7, nbinsx=25),
                             row=i//2+1, col=i%2+1)
            fig.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # ===== DISTRICT-WISE COMPARISON =====
            st.markdown("---")
            st.subheader("📍 District-wise Average Scores Comparison")
            
            scores = ['Infrastructure_Score', 'Safety_Score', 'Facilities_Score', 'Total_Performance']
            colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
            
            district_avg = filtered_df.groupby('district')[scores].mean().reset_index()
            district_avg = district_avg.sort_values('Total_Performance', ascending=False).head(15)
            
            fig_district = go.Figure()
            for score, color in zip(scores, colors):
                fig_district.add_trace(go.Bar(
                    name=score.replace('_', ' '),
                    x=district_avg['district'],
                    y=district_avg[score],
                    marker_color=color
                ))
            
            fig_district.update_layout(
                barmode='group',
                height=550,
                title="Top 15 Districts by Average Total Performance",
                xaxis_title="District",
                yaxis_title="Average Score",
                hovermode='x unified',
                xaxis_tickangle=-45,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_district, use_container_width=True)
            
            # ===== RESOURCE AVAILABILITY HEATMAP =====
            st.subheader("🔥 Resource Availability Heatmap by Location")
            
            if "school_location" in filtered_df.columns:
                resource_cols = ["electricity", "drink_water", "usable_toilets", "boundary_wall_state", "main_gate"]
                matrix = filtered_df.groupby("school_location")[resource_cols].mean()
                
                fig_heatmap = go.Figure(go.Heatmap(
                    z=matrix.values,
                    x=[c.replace('_', ' ').title() for c in resource_cols],
                    y=matrix.index,
                    colorscale='Blues',
                    text=matrix.values.round(2),
                    texttemplate='%{text}',
                    colorbar=dict(title="Avg")
                ))
                fig_heatmap.update_layout(height=350, title="Resource Availability by Location (Urban/Rural)")
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Infrastructure
        with perf_tabs[1]:
            st.header("🏗️ Infrastructure")
            top, bottom = get_top_bottom(filtered_df, "Infrastructure_Score", num_schools)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(create_horizontal_bar(top, "Infrastructure_Score", f"Top {num_schools}", "Greens"), use_container_width=True)
            with c2:
                st.plotly_chart(create_horizontal_bar(bottom, "Infrastructure_Score", f"Bottom {num_schools}", "Reds"), use_container_width=True)
        
        # Safety
        with perf_tabs[2]:
            st.header("🛡️ Safety")
            top, bottom = get_top_bottom(filtered_df, "Safety_Score", num_schools)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(create_horizontal_bar(top, "Safety_Score", f"Top {num_schools}", "Greens"), use_container_width=True)
            with c2:
                st.plotly_chart(create_horizontal_bar(bottom, "Safety_Score", f"Bottom {num_schools}", "Reds"), use_container_width=True)
        
        # Facilities
        with perf_tabs[3]:
            st.header("🎓 Facilities")
            top, bottom = get_top_bottom(filtered_df, "Facilities_Score", num_schools)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(create_horizontal_bar(top, "Facilities_Score", f"Top {num_schools}", "Greens"), use_container_width=True)
            with c2:
                st.plotly_chart(create_horizontal_bar(bottom, "Facilities_Score", f"Bottom {num_schools}", "Reds"), use_container_width=True)
        
        # Total
        with perf_tabs[4]:
            st.header("🏆 Total Performance")
            top, bottom = get_top_bottom(filtered_df, "Total_Performance", num_schools)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(create_horizontal_bar(top, "Total_Performance", f"Top {num_schools}", "Greens"), use_container_width=True)
            with c2:
                st.plotly_chart(create_horizontal_bar(bottom, "Total_Performance", f"Bottom {num_schools}", "Reds"), use_container_width=True)
        
        # Correlations
        with perf_tabs[5]:
            st.header(" Correlations")
            corr = filtered_df[scores].corr()
            fig = go.Figure(go.Heatmap(
                z=corr.values, x=[s.replace('_', ' ') for s in scores],
                y=[s.replace('_', ' ') for s in scores],
                colorscale='RdBu', zmid=0, text=corr.values.round(3), texttemplate='%{text}'
            ))
            fig.update_layout(height=500, title="Score Correlations")
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: EXPLORATORY ANALYSIS ====================
    with main_tabs[1]:
        eda_tabs = st.tabs([
            " Demographics",
            " Infrastructure",
            " Utilities",
            " Sports & Labs",
            " Staff & Students",
            " Timeline",
            " PCA Analysis"
        ])
        
        # ---------- DEMOGRAPHICS ----------
        with eda_tabs[0]:
            st.header("📋 School Demographics")
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Medium distribution
                if "medium" in filtered_df.columns:
                    medium_counts = filtered_df["medium"].value_counts()
                    fig = px.pie(values=medium_counts.values, names=medium_counts.index,
                                title="Medium of Instruction", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                
                # School location
                if "school_location" in filtered_df.columns:
                    loc_counts = filtered_df["school_location"].value_counts()
                    fig = px.bar(x=loc_counts.index, y=loc_counts.values,
                                title="Urban vs Rural Schools", color=loc_counts.index)
                    st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                # School gender
                if "school_gender" in filtered_df.columns:
                    gender_counts = filtered_df["school_gender"].value_counts()
                    fig = px.bar(x=gender_counts.index, y=gender_counts.values,
                                title="School Gender Type", color=gender_counts.index)
                    st.plotly_chart(fig, use_container_width=True)
                
                # School shift - Remove Unknown
                if "school_shift" in filtered_df.columns:
                    shift_df = filtered_df[~filtered_df["school_shift"].isin(["Unknown", "unknown", ""])]
                    shift_counts = shift_df["school_shift"].value_counts()
                    fig = px.bar(x=shift_counts.index, y=shift_counts.values,
                                title="School Shift Distribution", color=shift_counts.index)
                    st.plotly_chart(fig, use_container_width=True)
            
            # School level distribution
            level_counts = filtered_df["school_level"].value_counts()
            fig = px.bar(y=level_counts.index, x=level_counts.values, orientation='h',
                        title="School Levels Distribution", color=level_counts.index)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Non-functional reasons with selector and cleaned data
            if "non_func_reason" in filtered_df.columns:
                st.subheader("⚠️ Non-Functional Reasons")
                
                # Clean invalid values
                invalid_values = ["0", 0, 0.0, "2", 2, 2.0, "1", 1, 1.0, "3", 3, 3.0, "", None]
                reasons_df = filtered_df[~filtered_df["non_func_reason"].isin(invalid_values)]
                reasons_df = reasons_df[reasons_df["non_func_reason"].notna()]
                reasons_df = reasons_df[reasons_df["non_func_reason"].astype(str).str.strip() != ""]
                
                all_reasons = reasons_df["non_func_reason"].value_counts()
                
                if len(all_reasons) > 0:
                    # User selector for number of reasons to show
                    top_n_reasons = st.slider("Select number of reasons to display", 
                                             min_value=3, max_value=min(20, len(all_reasons)), 
                                             value=min(10, len(all_reasons)), key="nfr_slider")
                    
                    reasons_to_show = all_reasons.head(top_n_reasons)
                    fig = px.bar(y=reasons_to_show.index, x=reasons_to_show.values, orientation='h',
                                title=f"Top {top_n_reasons} Non-Functional Reasons",
                                color=reasons_to_show.values, color_continuous_scale="Reds")
                    fig.update_layout(height=max(300, top_n_reasons * 35))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No valid non-functional reasons found in data.")
        
        # ---------- INFRASTRUCTURE ----------
        with eda_tabs[1]:
            st.header("🏗️ Building & Classroom Analysis")
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Building ownership - Remove 1 and 2
                if "bldg_ownership" in filtered_df.columns:
                    own_df = filtered_df[~filtered_df["bldg_ownership"].astype(str).isin(["1", "2", "1.0", "2.0"])]
                    own_counts = own_df["bldg_ownership"].value_counts().head(10)
                    fig = px.bar(y=own_counts.index, x=own_counts.values, orientation='h',
                                title="Building Ownership")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Building condition
                if "bldg_condition" in filtered_df.columns:
                    cond_counts = filtered_df["bldg_condition"].value_counts().head(10)
                    fig = px.bar(y=cond_counts.index, x=cond_counts.values, orientation='h',
                                title="Building Condition")
                    st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                # Construction type - Remove 2
                if "construct_type" in filtered_df.columns:
                    const_df = filtered_df[~filtered_df["construct_type"].astype(str).isin(["2", "2.0"])]
                    const_counts = const_df["construct_type"].value_counts().head(10)
                    fig = px.bar(y=const_counts.index, x=const_counts.values, orientation='h',
                                title="Construction Type")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Classroom distributions
                class_cols = ["total_rooms", "functional_classrooms", "dangerous_classrooms"]
                for col in class_cols:
                    if col in filtered_df.columns:
                        fig = px.histogram(filtered_df, x=col, nbins=30,
                                          title=col.replace("_", " ").title())
                        st.plotly_chart(fig, use_container_width=True)
                        break
            
            # Classroom distributions full
            st.subheader("📊 Classroom Distribution Analysis")
            class_cols_full = ["total_rooms", "functional_classrooms", "dangerous_classrooms"]
            class_present = [c for c in class_cols_full if c in filtered_df.columns]
            if class_present:
                selected_class_col = st.selectbox("Select classroom metric", class_present, key="class_select")
                fig = px.histogram(filtered_df, x=selected_class_col, nbins=40,
                                  title=selected_class_col.replace("_", " ").title())
                st.plotly_chart(fig, use_container_width=True)
        
        # ---------- UTILITIES ----------
        with eda_tabs[2]:
            st.header("💡 Utilities & Basic Amenities")
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                # Electricity
                elec_df = filtered_df[filtered_df["electricity"].isin([0, 1])]
                elec_counts = elec_df["electricity"].value_counts().sort_index()
                fig = px.pie(values=elec_counts.values, 
                            names=["No Electricity", "Available"][:len(elec_counts)],
                            title="Electricity Availability", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                # Drinking water
                water_df = filtered_df[filtered_df["drink_water"].isin([0, 1])]
                water_counts = water_df["drink_water"].value_counts().sort_index()
                fig = px.pie(values=water_counts.values,
                            names=["No Water", "Available"][:len(water_counts)],
                            title="Drinking Water", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            
            with c3:
                # Toilets
                if "toilets" in filtered_df.columns:
                    toilet_df = filtered_df[filtered_df["toilets"].isin([0, 1])]
                    toilet_counts = toilet_df["toilets"].value_counts().sort_index()
                    fig = px.pie(values=toilet_counts.values,
                                names=["No Toilets", "Available"][:len(toilet_counts)],
                                title="Toilet Availability", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Toilet condition summary
            total_t = filtered_df["total_toilets"].sum()
            usable_t = filtered_df["usable_toilets"].sum()
            repair_t = filtered_df["need_repairing_toilets"].sum() if "need_repairing_toilets" in filtered_df.columns else 0
            
            fig = px.bar(x=["Total Toilets", "Usable", "Need Repair"],
                        y=[total_t, usable_t, repair_t],
                        title="Toilet Condition Summary", color=["Total", "Usable", "Repair"])
            st.plotly_chart(fig, use_container_width=True)
            
            # Security features
            c1, c2, c3 = st.columns(3)
            
            with c1:
                bw_counts = filtered_df["boundary_wall_state"].value_counts()
                fig = px.bar(x=bw_counts.index.astype(str), y=bw_counts.values,
                            title="Boundary Wall State")
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                mg_counts = filtered_df["main_gate"].value_counts()
                fig = px.bar(x=mg_counts.index.astype(str), y=mg_counts.values,
                            title="Main Gate")
                st.plotly_chart(fig, use_container_width=True)
            
            with c3:
                if "sewerage" in filtered_df.columns:
                    sew_df = filtered_df[filtered_df["sewerage"].isin([0, 1])]
                    sew_counts = sew_df["sewerage"].value_counts().sort_index()
                    fig = px.bar(x=["No Sewerage", "Available"][:len(sew_counts)],
                                y=sew_counts.values, title="Sewerage System")
                    st.plotly_chart(fig, use_container_width=True)
            
            # ===== REASONS FOR NO ELECTRICITY =====
            st.markdown("---")
            st.subheader("⚡ Reasons for No Electricity")
            
            if "no_electricity_reason" in filtered_df.columns:
                # Filter schools without electricity
                df_no_elec = filtered_df[filtered_df["electricity"] == 0]
                
                # Clean invalid values
                df_no_elec_clean = df_no_elec[
                    (df_no_elec["no_electricity_reason"].notna()) &
                    (df_no_elec["no_electricity_reason"].astype(str).str.strip() != "") &
                    (~df_no_elec["no_electricity_reason"].astype(str).isin(["1", "2", "3", "0"]))
                ]
                
                if len(df_no_elec_clean) > 0:
                    reason_counts = df_no_elec_clean["no_electricity_reason"].value_counts()
                    fig = px.bar(x=reason_counts.values, y=reason_counts.index, orientation='h',
                                title="Reasons for No Electricity (Cleaned)",
                                color=reason_counts.values, color_continuous_scale="Oranges")
                    fig.update_layout(xaxis_title="Number of Schools", yaxis_title="Reason")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No valid electricity reason data available.")
            
            # ===== SCHOOL FUNCTIONALITY VS ELECTRICITY HEATMAP =====
            st.markdown("---")
            st.subheader("🔌 School Functionality vs Utilities")
            
            if "school_status" in filtered_df.columns:
                # Filter valid electricity values
                func_df = filtered_df[filtered_df["electricity"].isin([0, 1])]
                func_df = func_df[func_df["drink_water"].isin([0, 1])]
                
                hc1, hc2 = st.columns(2)
                
                with hc1:
                    # Electricity heatmap
                    crosstab_elec = pd.crosstab(func_df["school_status"], func_df["electricity"])
                    crosstab_elec.columns = ["No Electricity", "Has Electricity"]
                    
                    fig = go.Figure(go.Heatmap(
                        z=crosstab_elec.values,
                        x=crosstab_elec.columns.tolist(),
                        y=crosstab_elec.index.tolist(),
                        colorscale='Blues',
                        text=crosstab_elec.values,
                        texttemplate='%{text}',
                        textfont={"size": 12}
                    ))
                    fig.update_layout(title="School Status vs Electricity", height=350)
                    st.plotly_chart(fig, use_container_width=True)
                
                with hc2:
                    # Drinking water heatmap
                    crosstab_water = pd.crosstab(func_df["school_status"], func_df["drink_water"])
                    crosstab_water.columns = ["No Water", "Has Water"]
                    
                    fig = go.Figure(go.Heatmap(
                        z=crosstab_water.values,
                        x=crosstab_water.columns.tolist(),
                        y=crosstab_water.index.tolist(),
                        colorscale='Greens',
                        text=crosstab_water.values,
                        texttemplate='%{text}',
                        textfont={"size": 12}
                    ))
                    fig.update_layout(title="School Status vs Drinking Water", height=350)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Insight callout
                non_func_with_elec = len(func_df[(func_df["school_status"].str.lower().str.contains("non", na=False)) & 
                                                  (func_df["electricity"] == 1)])
                if non_func_with_elec > 0:
                    st.warning(f"⚠️ **Insight:** {non_func_with_elec:,} non-functional schools still have electricity available!")
            
            # ===== RESOURCE AVAILABILITY HEATMAP (AREA-WISE) =====
            st.markdown("---")
            st.subheader("🗺️ Resource Availability Matrix (Area-wise)")
            
            area_col_options = ["school_location", "district", "school_level"]
            area_col_present = [c for c in area_col_options if c in filtered_df.columns]
            
            if area_col_present:
                selected_area = st.selectbox("Group by", area_col_present, key="resource_area")
                
                resource_cols = ["electricity", "drink_water", "usable_toilets", "boundary_wall_state", "main_gate"]
                resource_present = [c for c in resource_cols if c in filtered_df.columns]
                
                if resource_present:
                    matrix = filtered_df.groupby(selected_area)[resource_present].mean()
                    
                    fig = go.Figure(go.Heatmap(
                        z=matrix.values,
                        x=[c.replace('_', ' ').title() for c in resource_present],
                        y=matrix.index.tolist(),
                        colorscale='Blues',
                        text=matrix.values.round(2),
                        texttemplate='%{text}',
                        colorbar=dict(title="Avg")
                    ))
                    fig.update_layout(title=f"Resource Availability by {selected_area.replace('_', ' ').title()}", 
                                     height=max(350, len(matrix) * 30))
                    st.plotly_chart(fig, use_container_width=True)
            
            # ===== RESOURCE CORRELATION WITH PERFORMANCE =====
            st.markdown("---")
            st.subheader("📊 Resource Correlation with Performance")
            
            corr_cols = ["electricity", "drink_water", "usable_toilets", "boundary_wall_state", 
                        "main_gate", "Infrastructure_Score", "Safety_Score", "Facilities_Score", "Total_Performance"]
            corr_present = [c for c in corr_cols if c in filtered_df.columns]
            
            if len(corr_present) >= 4:
                corr_matrix = filtered_df[corr_present].corr()
                
                fig = go.Figure(go.Heatmap(
                    z=corr_matrix.values,
                    x=[c.replace('_', ' ').title() for c in corr_present],
                    y=[c.replace('_', ' ').title() for c in corr_present],
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.values.round(2),
                    texttemplate='%{text}',
                    colorbar=dict(title="Correlation")
                ))
                fig.update_layout(title="Correlation of Resources with Performance Scores", height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        # ---------- SPORTS & LABS ----------
        with eda_tabs[3]:
            st.header("🏃 Sports & 🔬 Laboratory Facilities")
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Playground
                pg_counts = filtered_df["play_ground"].replace(2, 1).value_counts().sort_index()
                fig = px.pie(values=pg_counts.values,
                            names=["No Playground", "Available"][:len(pg_counts)],
                            title="Playground Availability", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
                
                # Sports radar
                sports_cols = ["cricket", "football", "hockey", "badminton", "volleyball", "table_tennis"]
                sports_present = [c for c in sports_cols if c in filtered_df.columns]
                if sports_present:
                    sports_sum = filtered_df[sports_present].sum()
                    fig = go.Figure(go.Scatterpolar(
                        r=sports_sum.values.tolist() + [sports_sum.values[0]],
                        theta=sports_sum.index.tolist() + [sports_sum.index[0]],
                        fill='toself', name='Sports'
                    ))
                    fig.update_layout(title="Sports Facilities Radar", height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                # Library
                lib_counts = filtered_df["library"].replace(2, 1).value_counts().sort_index()
                fig = px.pie(values=lib_counts.values,
                            names=["No Library", "Available"][:len(lib_counts)],
                            title="Library Availability", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
                
                # Library Condition Distribution
                if "library_condition" in filtered_df.columns:
                    lib_cond_df = filtered_df[~filtered_df["library_condition"].astype(str).isin(["0", "1", "2", "3", "", "nan"])]
                    lib_cond_counts = lib_cond_df["library_condition"].value_counts()
                    if len(lib_cond_counts) > 0:
                        fig = px.bar(x=lib_cond_counts.index, y=lib_cond_counts.values,
                                    title="Library Condition Distribution", color=lib_cond_counts.index)
                        fig.update_layout(xaxis_title="Library Condition", yaxis_title="Number of Schools")
                        st.plotly_chart(fig, use_container_width=True)
                
                # Lab availability
                lab_features = {
                    "Physics": "physics_lab", "Biology": "biology_lab",
                    "Chemistry": "chemistry_lab", "Home Econ": "home_economic_lab",
                    "Computer": "computer_lab"
                }
                lab_avail = {k: filtered_df[v].sum() for k, v in lab_features.items() if v in filtered_df.columns}
                fig = px.bar(x=list(lab_avail.keys()), y=list(lab_avail.values()),
                            title="Lab Availability", color=list(lab_avail.keys()))
                st.plotly_chart(fig, use_container_width=True)
            
            # Lab readiness
            readiness_order = ["Very Low", "Low", "Medium", "High", "Excellent"]
            readiness_counts = filtered_df["lab_readiness"].value_counts()
            readiness_counts = readiness_counts.reindex(readiness_order, fill_value=0)
            fig = px.bar(x=readiness_counts.index, y=readiness_counts.values,
                        title="Lab Readiness Distribution", color=readiness_counts.index)
            st.plotly_chart(fig, use_container_width=True)
            
            # Lab vs Apparatus (Enhanced with Combined Lab)
            st.subheader("🔬 Lab Infrastructure vs Apparatus Adequacy")
            apparatus_pairs = {
                "Physics": ("physics_lab", "physics_appratus"),
                "Biology": ("biology_lab", "biology_appratus"),
                "Chemistry": ("chemistry_lab", "chemistry_appratus"),
                "Home Econ": ("home_economic_lab", "home_economic_appratus"),
                "Combined Lab": ("combine_lab", "combine_appratus"),
            }
            adequacy_data = []
            for name, (lab, app) in apparatus_pairs.items():
                if lab in filtered_df.columns and app in filtered_df.columns:
                    adequacy_data.append({"Lab": name, "Has Lab": filtered_df[lab].sum(), "Has Apparatus": filtered_df[app].sum()})
            
            if adequacy_data:
                adequacy_df = pd.DataFrame(adequacy_data)
                fig = px.bar(adequacy_df, x="Lab", y=["Has Lab", "Has Apparatus"],
                            barmode="group", title="Lab Infrastructure vs Apparatus Availability")
                fig.update_layout(yaxis_title="Number of Schools")
                st.plotly_chart(fig, use_container_width=True)
        
        # ---------- STAFF & STUDENTS ----------
        with eda_tabs[4]:
            st.header("👩‍🏫 Staff & Student Analysis")
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Enrollment vs Teachers scatter
                sample = filtered_df.sample(n=min(3000, len(filtered_df)), random_state=42)
                fig = px.scatter(sample, x="Teachers", y="enrollment",
                                title="Enrollment vs Teachers", opacity=0.5)
                st.plotly_chart(fig, use_container_width=True)
                
                # Teacher-student ratio by level
                fig = px.box(filtered_df[filtered_df["ts_ratio"].notna()],
                            x="school_level", y="ts_ratio",
                            title="Teacher-Student Ratio by Level")
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                # Staff by enrollment group
                filtered_df["enrollment_group"] = pd.cut(
                    filtered_df["enrollment"], bins=[0, 200, 500, 1000, 10000],
                    labels=["0-200", "200-500", "500-1000", "1000+"]
                )
                group_stats = filtered_df.groupby("enrollment_group")[["Teachers", "NonTeachers"]].mean().reset_index()
                group_melt = group_stats.melt(id_vars="enrollment_group", var_name="Staff", value_name="Average")
                fig = px.bar(group_melt, x="enrollment_group", y="Average", color="Staff",
                            barmode="group", title="Average Staff by Enrollment Group")
                st.plotly_chart(fig, use_container_width=True)
                
            # Computer training - Full width with better visualization
            st.markdown("---")
            st.subheader("💻 Computer Training Analysis")
            
            if "total_computer_training_students" in filtered_df.columns:
                comp_df = filtered_df[
                    (filtered_df["total_computers"] > 0) & 
                    (filtered_df["total_computer_training_students"] > 0)
                ].copy()
                
                if len(comp_df) > 0:
                    # User options
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        max_computers = st.slider("Filter by max computers", 1, int(comp_df["total_computers"].max()), 
                                                 min(100, int(comp_df["total_computers"].max())), key="comp_slider")
                    with cc2:
                        color_by = st.selectbox("Color by", ["internet", "school_level", "school_location"], key="comp_color")
                    
                    comp_filtered = comp_df[comp_df["total_computers"] <= max_computers]
                    
                    # Grouped bar chart - Computers vs Students by category
                    if color_by in comp_filtered.columns:
                        grouped = comp_filtered.groupby(color_by).agg({
                            "total_computers": "sum",
                            "total_computer_training_students": "sum"
                        }).reset_index()
                        
                        fig = px.bar(grouped, x=color_by, 
                                    y=["total_computers", "total_computer_training_students"],
                                    barmode="group",
                                    title=f"Total Computers vs Students Trained by {color_by.replace('_', ' ').title()}",
                                    labels={"value": "Count", "variable": "Metric"})
                        fig.update_layout(height=450)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Also show the scatter for detailed view
                    with st.expander("📈 View Scatter Plot (Detailed)"):
                        sample = comp_filtered.sample(n=min(2000, len(comp_filtered)), random_state=42)
                        fig2 = px.scatter(sample, x="total_computers", y="total_computer_training_students",
                                        color=color_by if color_by in sample.columns else None,
                                        title="Computer Capacity vs Students Trained", opacity=0.6)
                        st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No computer training data available.")
        
        # ---------- TIMELINE ----------
        with eda_tabs[5]:
            st.header("📅 School Establishment & Upgrade Timeline")
            
            # Helper functions
            def clean_years(series, min_year=1947):
                s = pd.to_numeric(series, errors="coerce")
                return s[(s >= min_year) & (s <= 2030)]
            
            def bin_years(series):
                return (series // 5) * 5
            
            # Year columns
            year_cols = ["est_year", "upgrade_primary_year", "upgrade_middle_year", 
                        "upgrade_high_year", "upgrade_high_sec_year"]
            year_cols_present = [c for c in year_cols if c in filtered_df.columns]
            
            # User controls
            tc1, tc2 = st.columns(2)
            with tc1:
                min_year_filter = st.slider("Minimum Year", 1800, 2000, 1947, key="year_min")
            with tc2:
                selected_year_cols = st.multiselect("Year columns to display", 
                                                    year_cols_present, 
                                                    default=year_cols_present[:3] if len(year_cols_present) >= 3 else year_cols_present,
                                                    key="year_cols_select")
            
            # Combined line plot
            st.subheader("📈 Combined Timeline (5-Year Bins)")
            fig_combined = go.Figure()
            
            colors_timeline = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
            
            for i, col in enumerate(selected_year_cols):
                if col in filtered_df.columns:
                    cleaned = clean_years(filtered_df[col], min_year_filter)
                    if not cleaned.empty:
                        binned = bin_years(cleaned)
                        counts = binned.value_counts().sort_index()
                        fig_combined.add_trace(go.Scatter(
                            x=counts.index, y=counts.values,
                            mode='lines+markers',
                            name=col.replace('_', ' ').title(),
                            line=dict(color=colors_timeline[i % len(colors_timeline)])
                        ))
            
            fig_combined.update_layout(
                title="School Establishment & Upgrades Over Time",
                xaxis_title="Year (5-year bins)",
                yaxis_title="Number of Schools",
                height=450,
                hovermode='x unified'
            )
            st.plotly_chart(fig_combined, use_container_width=True)
            
            # Individual subplots
            st.subheader("📊 Individual Year Category Analysis")
            
            if len(selected_year_cols) > 0:
                n_cols = min(3, len(selected_year_cols))
                n_rows = (len(selected_year_cols) + n_cols - 1) // n_cols
                
                fig_subplots = make_subplots(
                    rows=n_rows, cols=n_cols,
                    subplot_titles=[c.replace('_', ' ').title() for c in selected_year_cols]
                )
                
                for idx, col in enumerate(selected_year_cols):
                    row = idx // n_cols + 1
                    col_num = idx % n_cols + 1
                    
                    if col in filtered_df.columns:
                        cleaned = clean_years(filtered_df[col], min_year_filter)
                        if not cleaned.empty:
                            binned = bin_years(cleaned)
                            counts = binned.value_counts().sort_index()
                            
                            fig_subplots.add_trace(
                                go.Scatter(x=counts.index, y=counts.values, 
                                          mode='lines+markers',
                                          showlegend=False,
                                          line=dict(color=colors_timeline[idx % len(colors_timeline)])),
                                row=row, col=col_num
                            )
                
                fig_subplots.update_layout(height=300 * n_rows, title_text="Year-wise Distribution")
                st.plotly_chart(fig_subplots, use_container_width=True)
            
            # Building condition vs year
            st.subheader("🏗️ Building Condition by Establishment Year")
            year_df = filtered_df[(filtered_df["est_year"] >= min_year_filter) & (filtered_df["est_year"] <= 2025)]
            if len(year_df) > 0 and "bldg_condition" in year_df.columns:
                fig = px.box(year_df, x="bldg_condition", y="est_year",
                            title="Establishment Year vs Building Condition")
                st.plotly_chart(fig, use_container_width=True)
        
        # ---------- PCA ----------
        with eda_tabs[6]:
            st.header("🔬 PCA Analysis of Facility Features")
            
            fac_cols = ["functional_classrooms", "usable_toilets_per_100", "computers_per_100"]
            fac_present = [c for c in fac_cols if c in filtered_df.columns]
            
            if len(fac_present) >= 2:
                pca_df = filtered_df[fac_present + ["enrollment", "school_level"]].dropna()
                
                if len(pca_df) > 50:
                    scaler = StandardScaler()
                    Xs = scaler.fit_transform(pca_df[fac_present])
                    pca = PCA(n_components=2)
                    Xp = pca.fit_transform(Xs)
                    
                    pca_df = pca_df.copy()
                    pca_df["PC1"] = Xp[:, 0]
                    pca_df["PC2"] = Xp[:, 1]
                    
                    # Sample for plotting
                    sample = pca_df.sample(n=min(3000, len(pca_df)), random_state=42)
                    
                    fig = px.scatter(sample, x="PC1", y="PC2", color="school_level",
                                    size=np.sqrt(sample["enrollment"] + 1),
                                    title="PCA of Facility Features (sized by enrollment)",
                                    opacity=0.7)
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info(f"Explained variance: PC1={pca.explained_variance_ratio_[0]:.2%}, PC2={pca.explained_variance_ratio_[1]:.2%}")
                else:
                    st.warning("Not enough data for PCA analysis")
            else:
                st.warning("Not enough facility columns for PCA")
    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center;color:gray;'>🏫 School Performance Dashboard | Data Visualization Project</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
