import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Quote Turnaround Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'quotes_data' not in st.session_state:
    # Sample data for demonstration
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    sample_data = []
    
    complexities = ['Low', 'Medium', 'High', 'Very High']
    departments = ['Mechanical', 'Electrical', 'Manufacturing', 'Quality']
    statuses = ['Completed', 'In Progress']
    
    for _ in range(100):
        rfq_date = np.random.choice(dates)
        complexity = np.random.choice(complexities)
        dept = np.random.choice(departments)
        
        # Turnaround time varies by complexity
        if complexity == 'Low':
            turnaround = np.random.randint(1, 3)
        elif complexity == 'Medium':
            turnaround = np.random.randint(3, 7)
        elif complexity == 'High':
            turnaround = np.random.randint(7, 14)
        else:
            turnaround = np.random.randint(14, 30)
        
        sample_data.append({
            'RFQ_ID': f'RFQ-2024-{np.random.randint(1000, 9999)}',
            'RFQ_Date': rfq_date,
            'Complexity': complexity,
            'Engineering_Required': np.random.choice([True, False]),
            'Missing_Documentation': np.random.choice([True, False]),
            'Department': dept,
            'Queue_Position': np.random.randint(1, 15),
            'Expedite_Request': np.random.choice([True, False]),
            'Turnaround_Days': turnaround,
            'Status': np.random.choice(statuses),
            'Quote_Completion_Date': rfq_date + timedelta(days=turnaround)
        })
    
    st.session_state.quotes_data = pd.DataFrame(sample_data)

# Title and header
st.title("📊 Quote Turnaround Times Dashboard")
st.markdown("Standard Manufacturing & Engineering Organization - RFQ Process Tracking")
st.divider()

# Sidebar for filters and options
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # Tab for different views
    tab_option = st.radio("Select View:", ["Dashboard", "Add New Quote", "Analytics"])
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", st.session_state.quotes_data['RFQ_Date'].min().date())
    with col2:
        end_date = st.date_input("End Date", st.session_state.quotes_data['RFQ_Date'].max().date())
    
    # Filter by complexity
    selected_complexity = st.multiselect(
        "Filter by Complexity:",
        ['Low', 'Medium', 'High', 'Very High'],
        default=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Filter by department
    selected_dept = st.multiselect(
        "Filter by Department:",
        st.session_state.quotes_data['Department'].unique(),
        default=st.session_state.quotes_data['Department'].unique()
    )

# Apply filters
filtered_data = st.session_state.quotes_data[
    (st.session_state.quotes_data['RFQ_Date'].dt.date >= start_date) &
    (st.session_state.quotes_data['RFQ_Date'].dt.date <= end_date) &
    (st.session_state.quotes_data['Complexity'].isin(selected_complexity)) &
    (st.session_state.quotes_data['Department'].isin(selected_dept))
]

# --- DASHBOARD TAB ---
if tab_option == "Dashboard":
    # Key Metrics Row
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_turnaround = filtered_data['Turnaround_Days'].mean()
        st.metric("Average Turnaround", f"{avg_turnaround:.1f} days")
    
    with col2:
        total_quotes = len(filtered_data)
        st.metric("Total Quotes", total_quotes)
    
    with col3:
        completed = len(filtered_data[filtered_data['Status'] == 'Completed'])
        st.metric("Completed", completed)
    
    with col4:
        in_progress = len(filtered_data[filtered_data['Status'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    
    st.divider()
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Turnaround Time by Complexity")
        complexity_data = filtered_data.groupby('Complexity')['Turnaround_Days'].agg(['mean', 'count']).reset_index()
        complexity_data = complexity_data.sort_values('mean', ascending=False)
        
        fig_complexity = px.bar(
            complexity_data,
            x='Complexity',
            y='mean',
            color='Complexity',
            title="Average Days by Complexity Level",
            labels={'mean': 'Average Turnaround (Days)', 'Complexity': 'Complexity Level'},
            text_position='outside'
        )
        fig_complexity.update_traces(texttemplate='%{text:.1f}')
        st.plotly_chart(fig_complexity, use_container_width=True)
    
    with col2:
        st.subheader("👥 Turnaround Time by Department")
        dept_data = filtered_data.groupby('Department')['Turnaround_Days'].agg(['mean', 'count']).reset_index()
        dept_data = dept_data.sort_values('mean', ascending=False)
        
        fig_dept = px.bar(
            dept_data,
            x='Department',
            y='mean',
            color='Department',
            title="Average Days by Department",
            labels={'mean': 'Average Turnaround (Days)', 'Department': 'Department'},
            text_position='outside'
        )
        fig_dept.update_traces(texttemplate='%{text:.1f}')
        st.plotly_chart(fig_dept, use_container_width=True)
    
    st.divider()
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Impact: Engineering Review Required")
        eng_data = filtered_data.groupby('Engineering_Required')['Turnaround_Days'].mean().reset_index()
        eng_data['Engineering_Required'] = eng_data['Engineering_Required'].map({True: 'Yes', False: 'No'})
        
        fig_eng = px.bar(
            eng_data,
            x='Engineering_Required',
            y='Turnaround_Days',
            color='Engineering_Required',
            title="Impact of Engineering Review on Turnaround Time",
            labels={'Turnaround_Days': 'Average Days', 'Engineering_Required': 'Engineering Required'},
            text_position='outside'
        )
        fig_eng.update_traces(texttemplate='%{y:.1f}')
        st.plotly_chart(fig_eng, use_container_width=True)
    
    with col2:
        st.subheader("📋 Impact: Missing Documentation")
        doc_data = filtered_data.groupby('Missing_Documentation')['Turnaround_Days'].mean().reset_index()
        doc_data['Missing_Documentation'] = doc_data['Missing_Documentation'].map({True: 'Yes', False: 'No'})
        
        fig_doc = px.bar(
            doc_data,
            x='Missing_Documentation',
            y='Turnaround_Days',
            color='Missing_Documentation',
            title="Impact of Missing Documentation on Turnaround Time",
            labels={'Turnaround_Days': 'Average Days', 'Missing_Documentation': 'Missing Documentation'},
            text_position='outside'
        )
        fig_doc.update_traces(texttemplate='%{y:.1f}')
        st.plotly_chart(fig_doc, use_container_width=True)
    
    st.divider()
    
    # Charts Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚡ Impact: Expedite Requests")
        exp_data = filtered_data.groupby('Expedite_Request')['Turnaround_Days'].mean().reset_index()
        exp_data['Expedite_Request'] = exp_data['Expedite_Request'].map({True: 'Yes', False: 'No'})
        
        fig_exp = px.bar(
            exp_data,
            x='Expedite_Request',
            y='Turnaround_Days',
            color='Expedite_Request',
            title="Impact of Expedite Requests",
            labels={'Turnaround_Days': 'Average Days', 'Expedite_Request': 'Expedite Request'},
            text_position='outside'
        )
        fig_exp.update_traces(texttemplate='%{y:.1f}')
        st.plotly_chart(fig_exp, use_container_width=True)
    
    with col2:
        st.subheader("📊 Turnaround Time Distribution")
        fig_dist = px.histogram(
            filtered_data,
            x='Turnaround_Days',
            nbins=15,
            title="Distribution of Turnaround Times",
            labels={'Turnaround_Days': 'Turnaround (Days)', 'count': 'Number of Quotes'}
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.divider()
    
    # Trend over time
    st.subheader("📈 Turnaround Time Trend Over Time")
    trend_data = filtered_data.sort_values('RFQ_Date').copy()
    trend_data['Rolling_Avg'] = trend_data['Turnaround_Days'].rolling(window=7, min_periods=1).mean()
    
    fig_trend = px.line(
        trend_data,
        x='RFQ_Date',
        y='Turnaround_Days',
        title="Quote Turnaround Time Trend (with 7-day rolling average)",
        labels={'RFQ_Date': 'Date', 'Turnaround_Days': 'Turnaround (Days)'},
        opacity=0.6
    )
    fig_trend.add_scatter(x=trend_data['RFQ_Date'], y=trend_data['Rolling_Avg'], 
                          mode='lines', name='7-Day Avg', line=dict(color='red', width=3))
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.divider()
    
    # Data table
    st.subheader("📋 Detailed Quote Data")
    st.dataframe(
        filtered_data[['RFQ_ID', 'RFQ_Date', 'Complexity', 'Department', 
                       'Engineering_Required', 'Missing_Documentation', 
                       'Expedite_Request', 'Turnaround_Days', 'Status']].sort_values('RFQ_Date', ascending=False),
        use_container_width=True,
        hide_index=True
    )

# --- ADD NEW QUOTE TAB ---
elif tab_option == "Add New Quote":
    st.subheader("➕ Add New Quote Request")
    
    with st.form("new_quote_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            rfq_id = st.text_input("RFQ ID", placeholder="RFQ-2024-XXXX")
            rfq_date = st.date_input("RFQ Date")
            complexity = st.selectbox("Complexity Level", ['Low', 'Medium', 'High', 'Very High'])
            department = st.selectbox("Primary Department", ['Mechanical', 'Electrical', 'Manufacturing', 'Quality'])
        
        with col2:
            queue_position = st.number_input("Queue Position", min_value=1, step=1)
            engineering_required = st.checkbox("Engineering Review Required")
            missing_documentation = st.checkbox("Missing Documentation")
            expedite_request = st.checkbox("Expedite Request")
        
        turnaround_days = st.slider("Estimated Turnaround (Days)", 1, 30, 5)
        status = st.selectbox("Status", ['Completed', 'In Progress'])
        
        submitted = st.form_submit_button("Add Quote", use_container_width=True)
        
        if submitted:
            if rfq_id:
                new_quote = {
                    'RFQ_ID': rfq_id,
                    'RFQ_Date': pd.Timestamp(rfq_date),
                    'Complexity': complexity,
                    'Engineering_Required': engineering_required,
                    'Missing_Documentation': missing_documentation,
                    'Department': department,
                    'Queue_Position': queue_position,
                    'Expedite_Request': expedite_request,
                    'Turnaround_Days': turnaround_days,
                    'Status': status,
                    'Quote_Completion_Date': pd.Timestamp(rfq_date) + timedelta(days=turnaround_days)
                }
                st.session_state.quotes_data = pd.concat(
                    [st.session_state.quotes_data, pd.DataFrame([new_quote])],
                    ignore_index=True
                )
                st.success(f"Quote {rfq_id} added successfully!")
            else:
                st.error("Please enter an RFQ ID")

# --- ANALYTICS TAB ---
elif tab_option == "Analytics":
    st.subheader("📊 Advanced Analytics")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Median Turnaround", f"{filtered_data['Turnaround_Days'].median():.1f} days")
    with col2:
        st.metric("Max Turnaround", f"{filtered_data['Turnaround_Days'].max()} days")
    with col3:
        st.metric("Min Turnaround", f"{filtered_data['Turnaround_Days'].min()} days")
    
    st.divider()
    
    # Complexity impact analysis
    st.subheader("🎯 Complexity Impact Analysis")
    complexity_analysis = filtered_data.groupby('Complexity').agg({
        'Turnaround_Days': ['mean', 'median', 'std', 'min', 'max', 'count']
    }).round(2)
    complexity_analysis.columns = ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Count']
    st.dataframe(complexity_analysis, use_container_width=True)
    
    st.divider()
    
    # Department performance
    st.subheader("🏢 Department Performance")
    dept_analysis = filtered_data.groupby('Department').agg({
        'Turnaround_Days': ['mean', 'median', 'count'],
        'Engineering_Required': lambda x: (x.sum() / len(x) * 100).round(1)
    }).round(2)
    dept_analysis.columns = ['Avg Turnaround', 'Median', 'Quote Count', '% Eng Required']
    st.dataframe(dept_analysis, use_container_width=True)
    
    st.divider()
    
    # Heatmap: Complexity vs Department
    st.subheader("🔥 Heatmap: Complexity vs Department")
    heatmap_data = filtered_data.pivot_table(
        values='Turnaround_Days',
        index='Complexity',
        columns='Department',
        aggfunc='mean'
    )
    
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Department", y="Complexity", color="Avg Days"),
        title="Average Turnaround Time by Complexity and Department",
        color_continuous_scale="YlOrRd"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.divider()
    
    # Factors impact summary
    st.subheader("📊 Factors Impact Summary")
    
    factors_impact = {
        'Factor': [
            'Engineering Review Required',
            'Missing Documentation',
            'Expedite Request'
        ],
        'With Factor (Days)': [
            filtered_data[filtered_data['Engineering_Required']]['Turnaround_Days'].mean(),
            filtered_data[filtered_data['Missing_Documentation']]['Turnaround_Days'].mean(),
            filtered_data[filtered_data['Expedite_Request']]['Turnaround_Days'].mean()
        ],
        'Without Factor (Days)': [
            filtered_data[~filtered_data['Engineering_Required']]['Turnaround_Days'].mean(),
            filtered_data[~filtered_data['Missing_Documentation']]['Turnaround_Days'].mean(),
            filtered_data[~filtered_data['Expedite_Request']]['Turnaround_Days'].mean()
        ]
    }
    
    factors_df = pd.DataFrame(factors_impact)
    factors_df['Impact (Days)'] = factors_df['With Factor (Days)'] - factors_df['Without Factor (Days)']
    factors_df = factors_df.round(2)
    
    st.dataframe(factors_df, use_container_width=True, hide_index=True)
    
    fig_impact = px.bar(
        factors_df,
        x='Factor',
        y='Impact (Days)',
        title="Impact of Key Factors on Turnaround Time",
        labels={'Impact (Days)': 'Additional Days'},
        color='Impact (Days)'
    )
    st.plotly_chart(fig_impact, use_container_width=True)
