import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import sys
import traceback

st.set_page_config(
    page_title="Python Data Skills Playground",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
app_mode = st.sidebar.selectbox("Choose Workspace", [
    "🚀 Curriculum Roadmap (4-8 Weeks)",
    "🧹 Dataset Hub & Cleaner",
    "📈 Visualisation Workbench",
    "💻 Python Code Sandbox",
    "🎯 Guided Challenge Lab"
])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Upload your own CSV dataset in the *Dataset Hub* or use the built-in sample dataset to get started instantly!")

# ---------------------------------------------------------
# 1. CURRICULUM ROADMAP
# ---------------------------------------------------------
if app_mode == "🚀 Curriculum Roadmap (4-8 Weeks)":
    st.markdown('<div class="main-header">Python Data Skills Playground</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intermediate–Advanced Data Science & Analytics Curriculum (4–8 Weeks)</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Curriculum Modules", "8 Weeks", "Intermediate to Advanced")
    with col2:
        st.metric("Supported Libraries", "pandas, NumPy, Plotly, Seaborn", "Production Grade")
    with col3:
        st.metric("Interactive Environments", "Live Sandbox & Cleaner", "Real-time Execution")

    st.markdown("### 🗓️ Program Structure & Weekly Breakdown")
    
    weeks_data = [
        ("Weeks 1–2: Advanced Data Wrangling & Pandas Mastery", "Multi-index dataframes, advanced groupby operations, window functions, merging, joining, and memory optimization for large datasets."),
        ("Weeks 3–4: Robust Data Cleaning & Missing Value Strategies", "Imputation techniques, outlier detection (IQR, Z-score), string manipulation, regular expressions, and type coercion."),
        ("Weeks 5–6: Exploratory Data Analysis & Statistical Modeling", "Hypothesis testing, correlation analysis, distribution fitting, feature engineering, and statistical aggregation."),
        ("Weeks 7–8: Interactive Visualization & Web App Deployment", "Building publication-grade charts with Seaborn/Plotly, dashboarding with Streamlit, and packaging for production deployment.")
    ]

    for title, desc in weeks_data:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATASET HUB & CLEANER
# ---------------------------------------------------------
elif app_mode == "🧹 Dataset Hub & Cleaner":
    st.markdown('<div class="main-header">Dataset Hub & Cleaning Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Load, inspect, clean missing values, and transform your tabular datasets in real time.</div>', unsafe_allow_html=True)

    data_source = st.radio("Select Data Source", ["Use Built-in Sample Dataset", "Upload CSV File"])
    
    @st.cache_data
    def load_sample():
        return pd.read_csv("sample_data.csv")

    if data_source == "Use Built-in Sample Dataset":
        df = load_sample()
        st.success("Loaded built-in employee performance sample dataset successfully!")
    else:
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded `{uploaded_file.name}`!")
        else:
            st.info("Please upload a CSV file or switch to the built-in sample dataset.")
            st.stop()

    st.subheader("🔍 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")
    st.subheader("🛠️ Data Cleaning & Transformation Toolkit")

    col_a, col_b = st.columns(2)
    with col_a:
        drop_duplicates = st.checkbox("Remove Duplicate Rows", value=False)
        fill_na_option = st.selectbox("Missing Value Strategy", ["None", "Drop rows with missing values", "Fill numeric with Mean", "Fill numeric with Median", "Fill with Custom Value"])
    with col_b:
        selected_cols_to_drop = st.multiselect("Drop Unwanted Columns", options=df.columns.tolist())

    cleaned_df = df.copy()

    if drop_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()

    if selected_cols_to_drop:
        cleaned_df = cleaned_df.drop(columns=selected_cols_to_drop)

    if fill_na_option == "Drop rows with missing values":
        cleaned_df = cleaned_df.dropna()
    elif fill_na_option == "Fill numeric with Mean":
        num_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        cleaned_df[num_cols] = cleaned_df[num_cols].fillna(cleaned_df[num_cols].mean())
    elif fill_na_option == "Fill numeric with Median":
        num_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        cleaned_df[num_cols] = cleaned_df[num_cols].fillna(cleaned_df[num_cols].median())
    elif fill_na_option == "Fill with Custom Value":
        val = st.text_input("Enter custom fill value", "0")
        cleaned_df = cleaned_df.fillna(val)

    st.subheader("✨ Cleaned Dataset Preview")
    st.dataframe(cleaned_df.head(10), use_container_width=True)

    # Export cleaned data
    csv_bytes = cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=csv_bytes,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# 3. VISUALISATION WORKBENCH
# ---------------------------------------------------------
elif app_mode == "📈 Visualisation Workbench":
    st.markdown('<div class="main-header">Exploratory Visualisation Workbench</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create interactive Plotly charts and publication-grade Seaborn/Matplotlib plots instantly.</div>', unsafe_allow_html=True)

    @st.cache_data
    def load_sample():
        return pd.read_csv("sample_data.csv")

    df = load_sample()

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()

    viz_type = st.selectbox("Select Visualisation Type", [
        "Interactive Scatter Plot (Plotly)",
        "Interactive Bar Chart (Plotly)",
        "Correlation Heatmap (Seaborn)",
        "Distribution Histogram (Plotly)"
    ])

    if viz_type == "Interactive Scatter Plot (Plotly)":
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X-axis", numeric_cols, index=0)
            y_col = st.selectbox("Y-axis", numeric_cols, index=1)
            color_col = st.selectbox("Color Grouping", [None] + categorical_cols + numeric_cols)
            
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for a scatter plot.")

    elif viz_type == "Interactive Bar Chart (Plotly)":
        if categorical_cols and numeric_cols:
            cat_col = st.selectbox("Category (X-axis)", categorical_cols)
            num_col = st.selectbox("Metric (Y-axis)", numeric_cols)
            agg_func = st.selectbox("Aggregation", ["mean", "sum", "count", "max", "min"])
            
            grouped = df.groupby(cat_col)[num_col].agg(agg_func).reset_index()
            fig = px.bar(grouped, x=cat_col, y=num_col, title=f"{agg_func.capitalize()} of {num_col} by {cat_col}", template="plotly_white", color=cat_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dataset requires both categorical and numeric columns.")

    elif viz_type == "Correlation Heatmap (Seaborn)":
        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots(figsize=(8, 6))
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns for correlation analysis.")

    elif viz_type == "Distribution Histogram (Plotly)":
        if numeric_cols:
            num_col = st.selectbox("Select Numeric Column", numeric_cols)
            bins = st.slider("Number of Bins", 5, 50, 20)
            fig = px.histogram(df, x=num_col, nbins=bins, title=f"Distribution of {num_col}", template="plotly_white", marginal="box")
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 4. PYTHON CODE SANDBOX
# ---------------------------------------------------------
elif app_mode == "💻 Python Code Sandbox":
    st.markdown('<div class="main-header">Interactive Python Code Sandbox</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Write and execute custom pandas & NumPy queries in a secure, sandboxed environment.</div>', unsafe_allow_html=True)

    @st.cache_data
    def load_sample():
        return pd.read_csv("sample_data.csv")

    df = load_sample()

    st.info("The sample dataframe is loaded into memory as variable `df`. You can manipulate, query, and analyze `df` directly using Python.")

    default_code = """# Example: Calculate average salary by department
result = df.groupby('department')['salary'].mean().reset_index()
print(result)
"""

    user_code = st.text_area("Python Code Editor", value=default_code, height=200)

    if st.button("🚀 Run Code"):
        st.subheader("📤 Execution Output")
        
        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Safe execution namespace
        local_namespace = {"df": df, "pd": pd, "np": np}

        try:
            exec(user_code, {}, local_namespace)
            output = new_stdout.getvalue()
            if output:
                st.code(output, language="text")
            else:
                st.success("Code executed successfully with no printed output.")
            
            # Check if 'result' or modified df was created
            if 'result' in local_namespace:
                res = local_namespace['result']
                if isinstance(res, pd.DataFrame):
                    st.subheader("📊 Result DataFrame")
                    st.dataframe(res, use_container_width=True)
        except Exception as e:
            tb_str = traceback.format_exc()
            st.error("Error during execution:\n" + tb_str)
        finally:
            sys.stdout = old_stdout

# ---------------------------------------------------------
# 5. GUIDED CHALLENGE LAB
# ---------------------------------------------------------
elif app_mode == "🎯 Guided Challenge Lab":
    st.markdown('<div class="main-header">Guided Challenge Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test your data science skills with hands-on coding challenges and instant validation.</div>', unsafe_allow_html=True)

    challenge = st.selectbox("Select Challenge", [
        "Challenge 1: High Earners Filtering",
        "Challenge 2: Departmental Payroll Sum",
        "Challenge 3: Experience Quartile Grouping"
    ])

    @st.cache_data
    def load_sample():
        return pd.read_csv("sample_data.csv")

    df = load_sample()

    if challenge == "Challenge 1: High Earners Filtering":
        st.markdown("**Objective:** Filter the dataset to find all employees with a salary greater than $90,000 and a performance score >= 4.0.")
        user_filter_salary = st.number_input("Minimum Salary ($)", value=90000)
        user_filter_perf = st.slider("Minimum Performance Score", 1.0, 5.0, 4.0)

        expected_df = df[(df['salary'] > user_filter_salary) & (df['performance_score'] >= user_filter_perf)]
        st.markdown(f"**Matching Employees:** {len(expected_df)}")
        st.dataframe(expected_df, use_container_width=True)

    elif challenge == "Challenge 2: Departmental Payroll Sum":
        st.markdown("**Objective:** Compute the total payroll expenditure (sum of salaries) for each department.")
        payroll = df.groupby('department')['salary'].sum().reset_index()
        payroll.columns = ['Department', 'Total Payroll ($)']
        st.dataframe(payroll, use_container_width=True)

    elif challenge == "Challenge 3: Experience Quartile Grouping":
        st.markdown("**Objective:** Categorize employees into experience brackets based on their years of experience.")
        bins = [-1, 3, 10, 50]
        labels = ['Junior (0-3 yrs)', 'Mid-Level (4-10 yrs)', 'Senior (10+ yrs)']
        df_copy = df.copy()
        df_copy['Experience_Bracket'] = pd.cut(df_copy['experience_years'], bins=bins, labels=labels)
        
        st.dataframe(df_copy[['name', 'department', 'experience_years', 'Experience_Bracket']], use_container_width=True)
