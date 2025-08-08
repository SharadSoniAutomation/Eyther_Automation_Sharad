import json
import os
from datetime import datetime

try:
    import plotly.graph_objs as go
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def generate_test_report(results_data):
    """Generate HTML report with or without charts based on available dependencies"""
    
    if PLOTLY_AVAILABLE:
        return generate_enhanced_report(results_data)
    else:
        return generate_basic_report(results_data)

def generate_enhanced_report(results_data):
    """Generate HTML report with interactive charts"""
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    
    # Parse results
    total_tests = results_data.get("total", 0)
    passed = results_data.get("passed", 0)
    failed = results_data.get("failed", 0)
    errors = results_data.get("errors", 0)
    skipped = results_data.get("skipped", 0)
    
    # Create pie chart for test results
    pie_chart = go.Figure(data=[go.Pie(
        labels=['Passed', 'Failed', 'Errors', 'Skipped'],
        values=[passed, failed, errors, skipped],
        hole=.3,
        marker_colors=['#28a745', '#dc3545', '#ffc107', '#6c757d']
    )])
    
    pie_chart.update_layout(
        title="Test Results Overview",
        font=dict(size=14),
        showlegend=True
    )
    
    # Save chart as HTML
    pie_chart_html = pyo.plot(pie_chart, output_type='div', include_plotlyjs=True)
    
    # Generate HTML content with charts
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enhanced Test Automation Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            .summary {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin-bottom: 30px; }}
            .summary-card {{ background: white; padding: 15px; border-radius: 5px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .summary-card.passed {{ border-left: 4px solid #28a745; }}
            .summary-card.failed {{ border-left: 4px solid #dc3545; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Enhanced Test Automation Report</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{total_tests}</h3>
                <p>Total Tests</p>
            </div>
            <div class="summary-card passed">
                <h3>{passed}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card failed">
                <h3>{failed}</h3>
                <p>Failed</p>
            </div>
        </div>
        
        <div class="chart-container">
            {pie_chart_html}
        </div>
    </body>
    </html>
    """
    
    # Save report
    report_path = "reports/enhanced_test_report.html"
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    return report_path

def generate_basic_report(results_data):
    """Generate basic HTML report without external dependencies"""
    # Fallback to simple HTML report
    print("Plotly not available. Generating basic HTML report...")
    return "reports/basic_report.html"