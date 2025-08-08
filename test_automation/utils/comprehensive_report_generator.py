import json
import os
from datetime import datetime
from utils.helpers import screenshot_to_base64

# Check if plotly is available
try:
    import plotly.graph_objs as go
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
    print("Plotly available - generating interactive charts")
except ImportError:
    print("Plotly not available - using CSS charts")
    PLOTLY_AVAILABLE = False

def generate_comprehensive_report(test_results):
    """Generate comprehensive HTML report with all features"""
    
    print("Generating comprehensive test report...")
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # Calculate statistics
    stats = calculate_test_statistics(test_results)
    
    # Generate charts (with fallback)
    if PLOTLY_AVAILABLE:
        charts_html = generate_interactive_charts(stats)
    else:
        charts_html = generate_css_charts(stats)
    
    # Generate detailed test logs
    test_logs_html = generate_detailed_test_logs(test_results)
    
    # Create comprehensive HTML report
    html_content = create_comprehensive_html(stats, charts_html, test_logs_html, PLOTLY_AVAILABLE)
    
    # Save the report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join("reports", f"comprehensive_test_report_{timestamp}.html")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Also create a latest report
    latest_report_path = os.path.join("reports", "latest_test_report.html")
    with open(latest_report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Comprehensive report generated: {report_path}")
    print(f"Latest report: {latest_report_path}")
    
    return latest_report_path

def calculate_test_statistics(test_results):
    """Calculate comprehensive test statistics"""
    total_tests = len(test_results)
    passed_tests = len([t for t in test_results if t['status'] == 'PASSED'])
    failed_tests = len([t for t in test_results if t['status'] == 'FAILED'])
    
    # Module-wise statistics
    modules = {}
    for test in test_results:
        module = test['module']
        if module not in modules:
            modules[module] = {'total': 0, 'passed': 0, 'failed': 0}
        modules[module]['total'] += 1
        if test['status'] == 'PASSED':
            modules[module]['passed'] += 1
        else:
            modules[module]['failed'] += 1
    
    # Priority-wise statistics
    priorities = {'high': {'total': 0, 'passed': 0, 'failed': 0},
                 'medium': {'total': 0, 'passed': 0, 'failed': 0},
                 'low': {'total': 0, 'passed': 0, 'failed': 0}}
    
    for test in test_results:
        for marker in test['markers']:
            if marker in priorities:
                priorities[marker]['total'] += 1
                if test['status'] == 'PASSED':
                    priorities[marker]['passed'] += 1
                else:
                    priorities[marker]['failed'] += 1
    
    # Calculate durations
    total_duration = sum(float(test['duration'].replace('s', '')) for test in test_results)
    avg_duration = total_duration / total_tests if total_tests > 0 else 0
    
    return {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
        'fail_rate': (failed_tests / total_tests * 100) if total_tests > 0 else 0,
        'total_duration': f"{total_duration:.2f}s",
        'avg_duration': f"{avg_duration:.2f}s",
        'modules': modules,
        'priorities': priorities,
        'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_interactive_charts(stats):
    """Generate interactive Plotly charts"""
    
    try:
        # 1. Main Results Pie Chart
        pie_chart = go.Figure(data=[go.Pie(
            labels=['Passed', 'Failed'],
            values=[stats['passed'], stats['failed']],
            hole=.4,
            marker_colors=['#28a745', '#dc3545'],
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        pie_chart.update_layout(
            title={
                'text': f"Overall Test Results ({stats['total']} tests)",
                'x': 0.5,
                'font': {'size': 18}
            },
            height=400,
            showlegend=True,
            font=dict(size=12)
        )
        
        # 2. Module-wise Bar Chart
        modules = list(stats['modules'].keys())
        passed_counts = [stats['modules'][m]['passed'] for m in modules]
        failed_counts = [stats['modules'][m]['failed'] for m in modules]
        
        bar_chart = go.Figure(data=[
            go.Bar(name='Passed', x=modules, y=passed_counts, marker_color='#28a745'),
            go.Bar(name='Failed', x=modules, y=failed_counts, marker_color='#dc3545')
        ])
        
        bar_chart.update_layout(
            title='Module-wise Test Results',
            xaxis_title='Test Modules',
            yaxis_title='Number of Tests',
            barmode='group',
            height=400,
            font=dict(size=12)
        )
        
        # Convert charts to HTML
        pie_html = pyo.plot(pie_chart, output_type='div', include_plotlyjs=False)
        bar_html = pyo.plot(bar_chart, output_type='div', include_plotlyjs=False)
        
        return {
            'pie_chart': pie_html,
            'bar_chart': bar_html,
            'priority_chart': '<div><p style="text-align: center; color: #666;">Priority distribution chart</p></div>'
        }
        
    except Exception as e:
        print(f"Error generating interactive charts: {e}")
        return generate_css_charts(stats)

def generate_css_charts(stats):
    """Generate CSS-based charts as fallback"""
    
    pass_percentage = stats['pass_rate']
    fail_percentage = stats['fail_rate']
    
    pie_chart_css = f"""
    <div class="css-pie-chart">
        <div class="pie-chart" style="background: conic-gradient(
            #28a745 0deg {pass_percentage * 3.6}deg,
            #dc3545 {pass_percentage * 3.6}deg 360deg
        );">
            <div class="pie-center">
                <div class="pie-title">Test Results</div>
                <div class="pie-stats">
                    <div class="stat-passed">✅ {stats['passed']} Passed</div>
                    <div class="stat-failed">❌ {stats['failed']} Failed</div>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Module bar chart
    bar_chart_html = '<div class="css-bar-chart"><h3>Module-wise Results</h3>'
    for module, data in stats['modules'].items():
        total = data['total']
        passed = data['passed']
        failed = data['failed']
        pass_width = (passed / total * 100) if total > 0 else 0
        fail_width = (failed / total * 100) if total > 0 else 0
        
        bar_chart_html += f"""
        <div class="module-bar">
            <div class="module-name">{module} ({total} tests)</div>
            <div class="bar-container">
                <div class="bar-passed" style="width: {pass_width}%">{passed}</div>
                <div class="bar-failed" style="width: {fail_width}%">{failed}</div>
            </div>
        </div>
        """
    
    bar_chart_html += '</div>'
    
    return {
        'pie_chart': pie_chart_css,
        'bar_chart': bar_chart_html,
        'priority_chart': '<div><p style="text-align: center; color: #666;">CSS-based priority distribution</p></div>'
    }

def generate_detailed_test_logs(test_results):
    """Generate detailed test logs with screenshots and error messages"""
    
    passed_tests_html = ""
    failed_tests_html = ""
    
    for test in test_results:
        # Clean test name for display
        display_name = test['test_name'].replace('[chromium]', '').replace('_', ' ').title()
        
        test_html = f"""
        <div class="test-log-item {'passed' if test['status'] == 'PASSED' else 'failed'}">
            <div class="test-header">
                <h4>
                    <span class="status-badge {'passed' if test['status'] == 'PASSED' else 'failed'}">
                        {test['status']}
                    </span>
                    {display_name}
                </h4>
                <div class="test-meta">
                    <span class="badge">📁 {test['module']}</span>
                    <span class="badge">⏱️ {test['duration']}</span>
                    <span class="badge">📅 {test['start_time']}</span>
                </div>
            </div>
            
            <div class="test-details">
                <div class="test-info">
                    <p><strong>Test File:</strong> {test['test_file']}</p>
                    <p><strong>Test ID:</strong> {test.get('test_id', 'N/A')}</p>
                    <p><strong>Duration:</strong> {test['duration']}</p>
                    <p><strong>Markers:</strong> {', '.join(test['markers']) if test['markers'] else 'None'}</p>
                </div>
        """
        
        if test['status'] == 'FAILED':
            # Clean error message
            error_msg = test['error_message'] if test['error_message'] else 'No error message available'
            # Truncate very long error messages
            if len(error_msg) > 2000:
                error_msg = error_msg[:2000] + "... [truncated]"
                
            test_html += f"""
                <div class="error-section">
                    <h5>❌ Error Details:</h5>
                    <div class="error-message">
                        <pre>{error_msg}</pre>
                    </div>
                </div>
            """
            
            if test['screenshot_path'] and os.path.exists(test['screenshot_path']):
                screenshot_base64 = screenshot_to_base64(test['screenshot_path'])
                if screenshot_base64:
                    test_html += f"""
                    <div class="screenshot-section">
                        <h5>📸 Failure Screenshot:</h5>
                        <div class="screenshot-container">
                            <img src="{screenshot_base64}" alt="Test failure screenshot" class="failure-screenshot" onclick="openModal(this)">
                            <p class="screenshot-caption">Click to enlarge • {os.path.basename(test['screenshot_path'])}</p>
                        </div>
                    </div>
                    """
                else:
                    test_html += f"""
                    <div class="screenshot-section">
                        <h5>📸 Screenshot:</h5>
                        <p>Screenshot available at: {test['screenshot_path']}</p>
                    </div>
                    """
        
        test_html += """
            </div>
        </div>
        """
        
        if test['status'] == 'PASSED':
            passed_tests_html += test_html
        else:
            failed_tests_html += test_html
    
    return {
        'passed_tests': passed_tests_html,
        'failed_tests': failed_tests_html
    }

def create_comprehensive_html(stats, charts_html, test_logs_html, plotly_available):
    """Create comprehensive HTML report"""
    
    plotly_js = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>' if plotly_available else ''
    
    css_chart_styles = """
    .css-pie-chart {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
    }
    
    .pie-chart {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .pie-center {
        width: 150px;
        height: 150px;
        background: white;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .pie-title {
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 1.1em;
    }
    
    .stat-passed, .stat-failed {
        font-size: 0.9em;
        margin: 2px 0;
    }
    
    .css-bar-chart {
        padding: 20px;
    }
    
    .module-bar {
        margin: 15px 0;
    }
    
    .module-name {
        font-weight: bold;
        margin-bottom: 8px;
        color: #333;
    }
    
    .bar-container {
        display: flex;
        height: 35px;
        background: #f0f0f0;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .bar-passed {
        background: linear-gradient(135deg, #28a745, #20c997);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9em;
        transition: all 0.3s ease;
    }
    
    .bar-failed {
        background: linear-gradient(135deg, #dc3545, #e74c3c);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9em;
        transition: all 0.3s ease;
    }
    """ if not plotly_available else ""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comprehensive Test Report - Eyther Application</title>
        {plotly_js}
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                color: white;
                padding: 40px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
                transform: rotate(-45deg);
                animation: shimmer 3s ease-in-out infinite;
            }}
            
            @keyframes shimmer {{
                0%, 100% {{ transform: translateX(-100%) rotate(-45deg); }}
                50% {{ transform: translateX(100%) rotate(-45deg); }}
            }}
            
            .header h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
            }}
            
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }}
            
            .nav-tabs {{
                display: flex;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 0 20px;
                overflow-x: auto;
            }}
            
            .nav-tab {{
                padding: 15px 25px;
                background: none;
                border: none;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
                color: #495057;
                border-bottom: 3px solid transparent;
                transition: all 0.3s ease;
                white-space: nowrap;
            }}
            
            .nav-tab.active {{
                color: #007bff;
                border-bottom-color: #007bff;
                background: white;
            }}
            
            .nav-tab:hover {{
                background: rgba(0,123,255,0.1);
                color: #007bff;
            }}
            
            .tab-content {{
                display: none;
                padding: 30px;
                animation: fadeIn 0.3s ease-in;
            }}
            
            .tab-content.active {{
                display: block;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .summary-card {{
                background: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border-left: 5px solid;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .summary-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}
            
            .summary-card.total {{ border-left-color: #007bff; }}
            .summary-card.passed {{ border-left-color: #28a745; }}
            .summary-card.failed {{ border-left-color: #dc3545; }}
            .summary-card.duration {{ border-left-color: #17a2b8; }}
            
            .summary-card h2 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
            }}
            
            .summary-card p {{
                font-size: 1.1em;
                color: #666;
                position: relative;
                z-index: 1;
            }}
            
            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            
            .test-log-item {{
                background: white;
                margin-bottom: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                overflow: hidden;
                border-left: 5px solid;
                transition: all 0.3s ease;
            }}
            
            .test-log-item.passed {{ border-left-color: #28a745; }}
            .test-log-item.failed {{ border-left-color: #dc3545; }}
            
            .test-log-item:hover {{
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                transform: translateY(-2px);
            }}
            
            .test-header {{
                padding: 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }}
            
            .test-header h4 {{
                margin-bottom: 10px;
                font-size: 1.2em;
                display: flex;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .status-badge {{
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .status-badge.passed {{ background: #28a745; color: white; }}
            .status-badge.failed {{ background: #dc3545; color: white; }}
            
            .test-meta {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .badge {{
                background: #e9ecef;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.85em;
                color: #495057;
            }}
            
            .test-details {{
                padding: 20px;
            }}
            
            .test-info p {{
                margin-bottom: 8px;
                color: #666;
            }}
            
            .error-section {{
                background: #fff5f5;
                border: 1px solid #fed7d7;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }}
            
            .error-section h5 {{
                color: #c53030;
                margin-bottom: 10px;
            }}
            
            .error-message {{
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 15px;
                max-height: 300px;
                overflow-y: auto;
            }}
            
            .error-message pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 0.85em;
                line-height: 1.4;
                color: #e53e3e;
                margin: 0;
            }}
            
            .screenshot-section {{
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }}
            
            .screenshot-section h5 {{
                color: #2d3748;
                margin-bottom: 10px;
            }}
            
            .screenshot-container {{
                text-align: center;
            }}
            
            .failure-screenshot {{
                max-width: 100%;
                height: auto;
                max-height: 400px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                cursor: pointer;
                transition: transform 0.3s ease;
            }}
            
            .failure-screenshot:hover {{
                transform: scale(1.02);
            }}
            
            .screenshot-caption {{
                margin-top: 10px;
                font-size: 0.9em;
                color: #666;
                font-style: italic;
            }}
            
            .modal {{
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.9);
            }}
            
            .modal-content {{
                display: block;
                margin: auto;
                max-width: 95%;
                max-height: 95%;
                margin-top: 2%;
                border-radius: 8px;
            }}
            
            .close {{
                position: absolute;
                top: 15px;
                right: 35px;
                color: #f1f1f1;
                font-size: 40px;
                font-weight: bold;
                cursor: pointer;
                transition: color 0.3s;
            }}
            
            .close:hover {{
                color: #bbb;
            }}
            
            .stats-highlight {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: center;
            }}
            
            .stats-highlight h3 {{
                margin-bottom: 15px;
                font-size: 1.5em;
            }}
            
            .stats-row {{
                display: flex;
                justify-content: space-around;
                gap: 20px;
                flex-wrap: wrap;
            }}
            
            .stat-item {{
                text-align: center;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                display: block;
            }}
            
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            
            {css_chart_styles}
            
            @media (max-width: 768px) {{
                .summary-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .header h1 {{
                    font-size: 2em;
                }}
                
                .stats-row {{
                    flex-direction: column;
                    gap: 15px;
                }}
                
                .test-header h4 {{
                    font-size: 1em;
                }}
                
                .container {{
                    margin: 10px;
                    border-radius: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Comprehensive Test Report</h1>
                <p>Eyther Application Test Suite</p>
                <p>Generated on: {stats['execution_time']}</p>
            </div>
            
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="showTab('overview')">📊 Overview</button>
                <button class="nav-tab" onclick="showTab('charts')">📈 Analytics</button>
                <button class="nav-tab" onclick="showTab('passed')">✅ Passed ({stats['passed']})</button>
                <button class="nav-tab" onclick="showTab('failed')">❌ Failed ({stats['failed']})</button>
            </div>
            
            <!-- Overview Tab -->
            <div id="overview" class="tab-content active">
                <div class="summary-grid">
                    <div class="summary-card total">
                        <h2>{stats['total']}</h2>
                        <p>Total Tests</p>
                    </div>
                    <div class="summary-card passed">
                        <h2>{stats['passed']}</h2>
                        <p>Passed ({stats['pass_rate']:.1f}%)</p>
                    </div>
                    <div class="summary-card failed">
                        <h2>{stats['failed']}</h2>
                        <p>Failed ({stats['fail_rate']:.1f}%)</p>
                    </div>
                    <div class="summary-card duration">
                        <h2>{stats['total_duration']}</h2>
                        <p>Total Duration</p>
                    </div>
                </div>
                
                <div class="stats-highlight">
                    <h3>📋 Execution Summary</h3>
                    <div class="stats-row">
                        <div class="stat-item">
                            <span class="stat-value">{stats['pass_rate']:.1f}%</span>
                            <span class="stat-label">Success Rate</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">{stats['avg_duration']}</span>
                            <span class="stat-label">Avg Duration</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">{len(stats['modules'])}</span>
                            <span class="stat-label">Modules</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Tab -->
            <div id="charts" class="tab-content">
                <div class="chart-container">
                    <h3>📊 Overall Test Results</h3>
                    {charts_html['pie_chart']}
                </div>
                <div class="chart-container">
                    <h3>📈 Module-wise Performance</h3>
                    {charts_html['bar_chart']}
                </div>
            </div>
            
            <!-- Passed Tests Tab -->
            <div id="passed" class="tab-content">
                <h2>✅ Passed Tests ({stats['passed']} tests)</h2>
                <div class="test-logs">
                    {test_logs_html['passed_tests'] if test_logs_html['passed_tests'] else '<p style="text-align: center; color: #666; font-style: italic;">No passed tests to display.</p>'}
                </div>
            </div>
            
            <!-- Failed Tests Tab -->
            <div id="failed" class="tab-content">
                <h2>❌ Failed Tests ({stats['failed']} tests)</h2>
                <div class="test-logs">
                    {test_logs_html['failed_tests'] if test_logs_html['failed_tests'] else '<p style="text-align: center; color: #666; font-style: italic;">No failed tests to display.</p>'}
                </div>
            </div>
        </div>
        
        <!-- Screenshot Modal -->
        <div id="screenshotModal" class="modal">
            <span class="close" onclick="closeModal()">&times;</span>
            <img class="modal-content" id="modalImage">
        </div>
        
        <script>
            function showTab(tabName) {{
                const tabContents = document.querySelectorAll('.tab-content');
                tabContents.forEach(tab => tab.classList.remove('active'));
                
                const tabs = document.querySelectorAll('.nav-tab');
                tabs.forEach(tab => tab.classList.remove('active'));
                
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }}
            
            function openModal(img) {{
                const modal = document.getElementById('screenshotModal');
                const modalImg = document.getElementById('modalImage');
                modal.style.display = 'block';
                modalImg.src = img.src;
            }}
            
            function closeModal() {{
                const modal = document.getElementById('screenshotModal');
                modal.style.display = 'none';
            }}
            
            window.onclick = function(event) {{
                const modal = document.getElementById('screenshotModal');
                if (event.target == modal) {{
                    modal.style.display = 'none';
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content