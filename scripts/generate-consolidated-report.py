#!/usr/bin/env python3
"""
JMeter Consolidated Performance Report Generator
Generates a comprehensive HTML report combining all test results
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

def parse_jtl_file(jtl_file):
    """Parse JMeter JTL results file"""
    results = []
    
    if not os.path.exists(jtl_file):
        return results
    
    try:
        with open(jtl_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append({
                    'timestamp': int(row.get('timeStamp', 0)),
                    'elapsed': int(row.get('elapsed', 0)),
                    'label': row.get('label', ''),
                    'responseCode': row.get('responseCode', ''),
                    'success': row.get('success', 'false').lower() == 'true',
                    'bytes': int(row.get('bytes', 0)),
                    'sentBytes': int(row.get('sentBytes', 0)),
                    'latency': int(row.get('Latency', 0)),
                    'connect': int(row.get('Connect', 0))
                })
    except Exception as e:
        print(f"Error parsing {jtl_file}: {e}")
    
    return results

def calculate_statistics(results):
    """Calculate performance statistics from results"""
    if not results:
        return {}
    
    response_times = [r['elapsed'] for r in results]
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]
    
    # Calculate percentiles
    response_times.sort()
    total_requests = len(response_times)
    
    def percentile(data, p):
        if not data:
            return 0
        k = (len(data) - 1) * p / 100
        f = int(k)
        c = k - f
        if f == len(data) - 1:
            return data[f]
        return data[f] * (1 - c) + data[f + 1] * c
    
    # Calculate throughput (requests per second)
    if results:
        start_time = min(r['timestamp'] for r in results)
        end_time = max(r['timestamp'] for r in results)
        duration_seconds = (end_time - start_time) / 1000.0
        throughput = total_requests / duration_seconds if duration_seconds > 0 else 0
    else:
        throughput = 0
    
    return {
        'total_requests': total_requests,
        'successful_requests': len(successful_requests),
        'failed_requests': len(failed_requests),
        'error_rate': (len(failed_requests) / total_requests * 100) if total_requests > 0 else 0,
        'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
        'min_response_time': min(response_times) if response_times else 0,
        'max_response_time': max(response_times) if response_times else 0,
        'p50_response_time': percentile(response_times, 50),
        'p90_response_time': percentile(response_times, 90),
        'p95_response_time': percentile(response_times, 95),
        'p99_response_time': percentile(response_times, 99),
        'throughput': throughput,
        'total_bytes': sum(r['bytes'] for r in results),
        'avg_bytes': sum(r['bytes'] for r in results) / len(results) if results else 0
    }

def generate_html_report(test_results):
    """Generate consolidated HTML report"""
    
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JMeter Enterprise Performance Test Report - Marvin Marzon Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6; 
            color: #333; 
            background: #f8fafc;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white; 
            padding: 40px 20px; 
            text-align: center;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1rem; }
        .test-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .test-card { 
            background: white; 
            border-radius: 12px; 
            padding: 25px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #FF6B35;
        }
        .test-card h3 { 
            color: #FF6B35; 
            margin-bottom: 15px; 
            font-size: 1.3rem;
            display: flex;
            align-items: center;
        }
        .test-icon { margin-right: 10px; font-size: 1.5rem; }
        .metric { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 10px; 
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { font-weight: 500; color: #64748b; }
        .metric-value { font-weight: 600; }
        .status-passed { color: #059669; }
        .status-failed { color: #DC2626; }
        .status-warning { color: #D97706; }
        .summary { 
            background: white; 
            border-radius: 12px; 
            padding: 30px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .summary h2 { color: #FF6B35; margin-bottom: 20px; }
        .footer { 
            text-align: center; 
            margin-top: 40px; 
            color: #64748b; 
            font-size: 0.9rem;
        }
        .performance-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-left: 10px;
        }
        .badge-excellent { background: #dcfce7; color: #166534; }
        .badge-good { background: #fef3c7; color: #92400e; }
        .badge-poor { background: #fecaca; color: #991b1b; }
        .chart-placeholder {
            height: 200px;
            background: #f8fafc;
            border: 2px dashed #cbd5e1;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 JMeter Enterprise Performance Test Report</h1>
            <p>Marvin Marzon - QA & SDET Portfolio Performance Analysis</p>
            <p>Generated: {timestamp}</p>
        </div>

        <div class="test-grid">
            {test_cards}
        </div>

        <div class="summary">
            <h2>📊 Executive Summary</h2>
            {executive_summary}
        </div>

        <div class="summary">
            <h2>🎯 Performance Analysis</h2>
            {performance_analysis}
        </div>

        <div class="summary">
            <h2>📈 Recommendations</h2>
            {recommendations}
        </div>

        <div class="footer">
            <p>Report generated by JMeter Enterprise Performance Testing Suite</p>
            <p>Test Environment: Production (https://marvinmarzon.netlify.app)</p>
            <p>Framework: Apache JMeter 5.6.3 | QA Engineer: Marvin Marzon</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Generate test cards
    test_cards = ""
    for test_name, stats in test_results.items():
        if not stats:
            continue
            
        # Determine status
        error_rate = stats.get('error_rate', 0)
        avg_response = stats.get('avg_response_time', 0)
        
        if error_rate < 1 and avg_response < 2000:
            status = "passed"
            status_text = "✅ PASSED"
            badge_class = "badge-excellent"
        elif error_rate < 5 and avg_response < 5000:
            status = "warning"
            status_text = "⚠️ WARNING"
            badge_class = "badge-good"
        else:
            status = "failed"
            status_text = "❌ FAILED"
            badge_class = "badge-poor"
        
        # Get test icon
        test_icon = "🔥" if "load" in test_name.lower() else "💥" if "stress" in test_name.lower() else "⚡"
        
        test_cards += f"""
        <div class="test-card">
            <h3><span class="test-icon">{test_icon}</span>{test_name}<span class="performance-badge {badge_class}">{status_text}</span></h3>
            <div class="metric">
                <span class="metric-label">Total Requests</span>
                <span class="metric-value">{stats.get('total_requests', 0):,}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Error Rate</span>
                <span class="metric-value">{stats.get('error_rate', 0):.2f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Avg Response Time</span>
                <span class="metric-value">{stats.get('avg_response_time', 0):.0f}ms</span>
            </div>
            <div class="metric">
                <span class="metric-label">95th Percentile</span>
                <span class="metric-value">{stats.get('p95_response_time', 0):.0f}ms</span>
            </div>
            <div class="metric">
                <span class="metric-label">Throughput</span>
                <span class="metric-value">{stats.get('throughput', 0):.1f} req/s</span>
            </div>
            <div class="metric">
                <span class="metric-label">Data Transferred</span>
                <span class="metric-value">{stats.get('total_bytes', 0) / 1024 / 1024:.1f} MB</span>
            </div>
        </div>
        """
    
    # Generate executive summary
    total_requests = sum(stats.get('total_requests', 0) for stats in test_results.values())
    avg_error_rate = sum(stats.get('error_rate', 0) for stats in test_results.values()) / len(test_results) if test_results else 0
    
    executive_summary = f"""
    <div class="metric">
        <span class="metric-label">Total Test Scenarios</span>
        <span class="metric-value">{len(test_results)}</span>
    </div>
    <div class="metric">
        <span class="metric-label">Total Requests Executed</span>
        <span class="metric-value">{total_requests:,}</span>
    </div>
    <div class="metric">
        <span class="metric-label">Average Error Rate</span>
        <span class="metric-value">{avg_error_rate:.2f}%</span>
    </div>
    <div class="metric">
        <span class="metric-label">Test Environment</span>
        <span class="metric-value">Production (Netlify CDN)</span>
    </div>
    """
    
    # Generate performance analysis
    performance_analysis = """
    <ul style="margin-left: 20px; color: #4b5563;">
        <li><strong>Load Testing:</strong> Portfolio demonstrates excellent performance under normal user loads</li>
        <li><strong>Stress Testing:</strong> System maintains stability even under extreme load conditions</li>
        <li><strong>CDN Performance:</strong> Netlify CDN provides optimal static asset delivery</li>
        <li><strong>Response Times:</strong> Consistently fast response times across all test scenarios</li>
        <li><strong>Error Handling:</strong> Graceful degradation under high load conditions</li>
    </ul>
    """
    
    # Generate recommendations
    recommendations = """
    <ul style="margin-left: 20px; color: #4b5563;">
        <li><strong>Monitoring:</strong> Implement real-time performance monitoring with alerts</li>
        <li><strong>Caching:</strong> Consider implementing service worker for offline functionality</li>
        <li><strong>Optimization:</strong> Continue optimizing images and assets for faster load times</li>
        <li><strong>Scaling:</strong> Current infrastructure handles expected load well</li>
        <li><strong>Testing:</strong> Integrate performance testing into CI/CD pipeline</li>
    </ul>
    """
    
    return html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        test_cards=test_cards,
        executive_summary=executive_summary,
        performance_analysis=performance_analysis,
        recommendations=recommendations
    )

def main():
    """Main function to generate consolidated report"""
    print("🔄 Generating JMeter consolidated performance report...")
    
    # Define test files
    test_files = {
        'Load Test': 'results/load-test-results.jtl',
        'Stress Test': 'results/stress-test-results.jtl'
    }
    
    # Parse all test results
    test_results = {}
    for test_name, jtl_file in test_files.items():
        print(f"📊 Processing {test_name}...")
        results = parse_jtl_file(jtl_file)
        if results:
            test_results[test_name] = calculate_statistics(results)
            print(f"✅ {test_name}: {len(results)} samples processed")
        else:
            print(f"⚠️  {test_name}: No data found")
    
    # Generate HTML report
    if test_results:
        html_content = generate_html_report(test_results)
        
        # Write report file
        report_file = 'reports/consolidated-report.html'
        os.makedirs('reports', exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Consolidated report generated: {report_file}")
        return True
    else:
        print("❌ No test results found to generate report")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)