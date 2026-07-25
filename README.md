# 📊 Quote Turnaround Time Dashboard

A comprehensive Streamlit dashboard for tracking and analyzing Request for Quote (RFQ) turnaround times for Standard Manufacturing & Engineering organizations.

## 📋 Overview

This dashboard helps manufacturing and engineering teams monitor, analyze, and optimize their quote generation process. It tracks the time required to complete RFQ reviews, considering multiple factors that impact turnaround time:

- **RFQ Complexity** (Low, Medium, High, Very High)
- **Engineering Review Requirements**
- **Missing Documentation**
- **Current Workload & Queue Size**
- **Competing Priorities & Expedite Requests**

## ✨ Features

### 1. **Dashboard View**
- **Key Metrics**: Real-time averages, total quotes, completed vs. in-progress
- **Complexity Analysis**: Average turnaround time by complexity level
- **Department Performance**: Breakdown by mechanical, electrical, manufacturing, quality teams
- **Impact Analysis**: Visual comparison of how different factors affect turnaround time
- **Trend Visualization**: 7-day rolling average trend chart
- **Distribution Chart**: Histogram of all turnaround times
- **Detailed Data Table**: Sortable and filterable quote records

### 2. **Add New Quote**
- Input form to manually add new RFQ records
- Track key attributes: complexity, department, documentation status, expedite flags
- Automatically calculate completion dates

### 3. **Advanced Analytics**
- **Summary Statistics**: Median, max, min turnaround times
- **Complexity Impact Analysis**: Detailed breakdown by complexity level
- **Department Performance Metrics**: Performance per team with engineering request percentages
- **Heatmap**: Complexity vs. Department cross-analysis
- **Factor Impact Summary**: Quantified impact of each factor on turnaround time

### 4. **Interactive Filters**
- Date range filtering
- Filter by complexity level
- Filter by department
- Real-time dashboard updates

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- `uv` package manager

### Installation & Running

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the dashboard:**
   ```bash
   uv run streamlit run streamlit_app.py
   ```

3. **Access the dashboard:**
   - Open your browser to `http://localhost:8501`

## 📊 Dashboard Sections

### Key Metrics Panel
Shows at-a-glance KPIs:
- Average turnaround time (days)
- Total quotes processed
- Completed quotes
- Quotes in progress

### Turnaround Analysis by Dimensions
- **By Complexity**: Visual comparison of how quote complexity affects turnaround time
- **By Department**: Performance metrics across teams
- **By Engineering Needs**: Impact of engineering review requirements
- **By Documentation**: Impact of missing documentation on timelines
- **By Expedite Requests**: How priority requests affect turnaround

### Trend Analysis
- Historical turnaround time trends
- 7-day rolling average to smooth out daily variations
- Identify process improvements or declining performance

### Advanced Analytics
- **Summary Statistics**: Statistical measures of turnaround distribution
- **Complexity Breakdown**: Mean, median, std dev, min/max by complexity
- **Department Performance**: Team-specific KPIs and metrics
- **Heatmap Analysis**: Two-dimensional view of complexity × department performance
- **Factor Impact**: Quantified impact of each contributing factor

## 📁 File Structure

```
.
├── streamlit_app.py       # Main dashboard application
├── pyproject.toml         # Project dependencies and configuration
├── README.md              # This file
└── LICENSE                # License information
```

## 🔧 Technologies Used

- **Streamlit**: Web app framework for data dashboards
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

## 💡 Sample Data

The dashboard includes sample data from 2024 with 100+ quotes to demonstrate functionality. The data includes:
- Realistic complexity distributions
- Varied turnaround times based on complexity
- Random assignment of factors (engineering review, missing docs, expedite requests)
- Multiple departments and queue positions

## 📈 Key Insights Provided

1. **Complexity Impact**: How much does each complexity level add to turnaround time?
2. **Department Efficiency**: Which departments handle quotes most quickly?
3. **Factor Analysis**: What's the combined impact of engineering reviews and missing documentation?
4. **Workload Trends**: Are turnaround times increasing or decreasing over time?
5. **Distribution Patterns**: What's the typical range of turnaround times?

## 🎯 Use Cases

- **Process Improvement**: Identify bottlenecks and inefficiencies
- **Capacity Planning**: Understand workload and queue management
- **SLA Tracking**: Monitor compliance with turnaround time targets
- **Performance Metrics**: Compare department and team performance
- **Trend Analysis**: Detect seasonal patterns or process changes
- **Decision Making**: Data-driven insights for process optimization

## 🔄 Future Enhancements

Potential features to add:
- Database integration for persistent data storage
- Export functionality (PDF, Excel reports)
- Predictive analytics for quote duration estimation
- Department-specific dashboards
- Real-time alerts for overdue quotes
- Integration with existing ERP/CRM systems
- Custom SLA threshold definitions
- Root cause analysis tools

## 📝 Notes

- Sample data is generated fresh with each session
- All data is stored in Streamlit session state (not persistent)
- For production use, integrate with a database backend
- Customize complexity levels and departments to match your organization

## 📞 Support

For questions or feature requests, please contact your manufacturing operations team.

---

**Last Updated**: 2024
**Version**: 1.0.0
