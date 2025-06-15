# 🚀 JMeter Performance Testing Suite

> **JMeter performance testing framework for QA & SDET portfolio validation**

Apache JMeter testing suite demonstrating advanced load testing capabilities, comprehensive monitoring, and reporting for [Marvin Marzon's QA & SDET Portfolio](https://marvinmarzon.netlify.app).

## 🎯 Quick Overview

This repository showcases **performance engineering expertise** through a comprehensive JMeter testing framework that validates:

- ✅ **Load Testing** (up to 500 concurrent users)
- ✅ **Stress Testing** (breaking point analysis)
- ✅ **Spike Testing** (traffic surge simulation)
- ✅ **Volume Testing** (large data sets)
- ✅ **Endurance Testing** (extended duration stability)

## 🚦 Quick Start

### Prerequisites
```bash
# Install Java 8 or higher
java -version

# Download Apache JMeter 5.6.3
wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.zip
unzip apache-jmeter-5.6.3.zip

# Set JMETER_HOME environment variable
export JMETER_HOME=/path/to/apache-jmeter-5.6.3
export PATH=$JMETER_HOME/bin:$PATH
```

### Run Tests
```bash
# GUI Mode (for test development)
jmeter -t test-plans/load-test.jmx

# Non-GUI Mode (for execution)
jmeter -n -t test-plans/load-test.jmx -l results/load-test-results.jtl -e -o reports/load-test-report

# Run all test suites
./scripts/run-all-tests.sh
```

### Docker Execution
```bash
# Build and run with Docker
docker-compose up jmeter-tests

# Specific test execution
docker run --rm -v $(pwd):/tests justb4/jmeter -n -t /tests/test-plans/load-test.jmx -l /tests/results/results.jtl
```

## 📊 Test Scenarios

| Test Type | Duration | Max Users | Ramp-up | Purpose |
|-----------|----------|-----------|---------|---------|
| **Load** | 20min | 100 | 5min | Normal traffic simulation |
| **Stress** | 30min | 500 | 10min | Breaking point identification |
| **Spike** | 15min | 1000 | 30s | Traffic surge handling |
| **Volume** | 45min | 50 | 2min | Large data processing |
| **Endurance** | 120min | 75 | 10min | Long-term stability |

## 🎯 Performance Targets

- **Response Time**: 95th percentile < 2000ms
- **Throughput**: > 100 requests/second sustained
- **Error Rate**: < 1% failed requests
- **Availability**: > 99.5% uptime during tests

## 📈 Features

### 🔧 **Test Plans**
- Modular test plan architecture
- Parameterized test data management
- Dynamic user simulation patterns
- Advanced correlation and assertions
- Custom Java samplers for complex scenarios

### 📊 **Advanced Reporting**
- HTML dashboard reports with charts
- Real-time monitoring integration
- Performance trend analysis
- SLA compliance validation
- Executive summary generation

### 🚀 **CI/CD Integration**
- Jenkins pipeline integration
- Docker containerization
- Automated report generation
- Performance regression detection
- Slack/Teams notifications

## 📁 Project Structure

```
jmeter-performance-tests/
├── 📋 test-plans/
│   ├── load-test.jmx           # Normal load simulation
│   ├── stress-test.jmx         # Breaking point analysis
│   ├── spike-test.jmx          # Traffic surge testing
│   ├── volume-test.jmx         # Large data processing
│   └── endurance-test.jmx      # Long-term stability
├── 📊 test-data/
│   ├── users.csv               # Test user data
│   ├── search-terms.csv        # Search scenarios
│   └── contact-data.csv        # Contact form data
├── 🔧 scripts/
│   ├── run-all-tests.sh        # Execute all test suites
│   ├── generate-reports.sh     # Create HTML reports
│   └── performance-analysis.py # Advanced analytics
├── 📈 reports/                 # Generated test reports
├── 📊 results/                 # Raw test results (JTL files)
├── 🐳 docker/                  # Container configurations
└── 📚 docs/                    # Comprehensive documentation
```

## 🔄 CI/CD Pipeline

### Jenkins Integration
```groovy
pipeline {
    agent any
    stages {
        stage('Performance Tests') {
            steps {
                sh './scripts/run-all-tests.sh'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'index.html',
                    reportName: 'JMeter Performance Report'
                ])
            }
        }
    }
}
```

### GitHub Actions
```yaml
name: JMeter Performance Tests
on: [push, schedule]
jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run JMeter Tests
        run: |
          docker run --rm -v $(pwd):/tests \
            justb4/jmeter -n -t /tests/test-plans/load-test.jmx \
            -l /tests/results/results.jtl -e -o /tests/reports
```

## 📊 Sample Results

### Load Test Summary
```
🔥 JMETER LOAD TEST COMPLETED
==============================
Environment: Production
URL: https://marvinmarzon.netlify.app
Virtual Users: 100 (peak)
Duration: 20 minutes
Total Samples: 12,847
Throughput: 10.7 req/s
Error Rate: 0.02%

Performance Metrics:
- Average Response Time: 1,156ms
- 90th Percentile: 1,789ms
- 95th Percentile: 2,134ms
- 99th Percentile: 2,876ms

Status: ✅ PASSED
```

## 🛠️ Technology Stack

- **Testing Framework**: [Apache JMeter 5.6.3](https://jmeter.apache.org/)
- **Scripting**: Java, Groovy, BeanShell
- **Containerization**: Docker & Docker Compose
- **CI/CD**: Jenkins, GitHub Actions
- **Reporting**: HTML dashboards, InfluxDB, Grafana
- **Monitoring**: Custom listeners and plugins

## 📚 Documentation

- **[Test Plan Documentation](docs/test-plans.md)** - Detailed test scenarios
- **[Performance Metrics Guide](docs/metrics-guide.md)** - KPI explanations
- **[CI/CD Integration](docs/cicd-integration.md)** - Pipeline setup
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues

## 🎯 Professional Value

### For QA Engineers
- **Industry Standards**: Apache JMeter best practices
- **Scalable Framework**: Professional-ready test architecture
- **Comprehensive Coverage**: Multiple testing methodologies

### For Development Teams
- **Performance Validation**: Early bottleneck detection
- **Capacity Planning**: Infrastructure sizing guidance
- **Quality Gates**: Automated performance thresholds

### For Business Stakeholders
- **Risk Mitigation**: Performance-related issue prevention
- **User Experience**: Optimal application responsiveness
- **Cost Optimization**: Efficient resource utilization

## 🤝 Contributing

This framework demonstrates QA engineering capabilities. For questions or collaboration opportunities:

**Marvin Marzon** - QA & SDET Professional
- 📧 **Email**: marvinmarzon@outlook.com
- 💼 **LinkedIn**: [Marvin Marzon](https://www.linkedin.com/in/mmarzon/)
- 🌐 **Portfolio**: [https://marvinmarzon.netlify.app](https://marvinmarzon.netlify.app)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🚀 Performance Testing Excellence with Apache JMeter**

*Demonstrating professional QA engineering capabilities through comprehensive performance validation*

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-blue?style=for-the-badge)](https://marvinmarzon.netlify.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/mmarzon/)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:marvinmarzon@outlook.com)

</div>
