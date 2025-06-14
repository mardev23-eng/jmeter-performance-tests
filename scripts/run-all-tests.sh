#!/bin/bash

# JMeter Enterprise Performance Testing Suite
# Run all test scenarios for Marvin Marzon's Portfolio

echo "🚀 Starting JMeter Enterprise Performance Testing Suite"
echo "====================================================="
echo "Target: https://marvinmarzon.netlify.app"
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if JMeter is installed
if ! command -v jmeter &> /dev/null; then
    echo -e "${RED}❌ JMeter is not installed or not in PATH${NC}"
    echo "Please install Apache JMeter and ensure it's in your PATH"
    exit 1
fi

# Create directories
mkdir -p results reports logs

# Function to run JMeter test
run_jmeter_test() {
    local test_name=$1
    local test_file=$2
    local result_file=$3
    local report_dir=$4
    
    echo -e "${BLUE}Running $test_name...${NC}"
    
    # Run JMeter in non-GUI mode
    jmeter -n \
        -t "$test_file" \
        -l "$result_file" \
        -e -o "$report_dir" \
        -Jbase.url=https://marvinmarzon.netlify.app \
        -j "logs/${test_name,,}-$(date +%Y%m%d_%H%M%S).log"
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ $test_name COMPLETED${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        return 1
    fi
}

# Test execution array
declare -a tests=(
    "Load Test:test-plans/load-test.jmx:results/load-test-results.jtl:reports/load-test"
    "Stress Test:test-plans/stress-test.jmx:results/stress-test-results.jtl:reports/stress-test"
)

passed_tests=0
total_tests=${#tests[@]}

# Run all tests
for test in "${tests[@]}"; do
    IFS=':' read -r test_name test_file result_file report_dir <<< "$test"
    
    if run_jmeter_test "$test_name" "$test_file" "$result_file" "$report_dir"; then
        ((passed_tests++))
    fi
    
    echo ""
done

# Generate consolidated report
echo -e "${BLUE}Generating consolidated performance report...${NC}"
if command -v python3 &> /dev/null; then
    python3 scripts/generate-consolidated-report.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Consolidated report generated successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Consolidated report generation failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Python3 not found, skipping consolidated report${NC}"
fi

# Final summary
echo ""
echo "====================================================="
echo -e "${BLUE}🏁 JMETER TEST EXECUTION SUMMARY${NC}"
echo "====================================================="
echo "Total Tests: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $((total_tests - passed_tests))"

if [ $passed_tests -eq $total_tests ]; then
    echo -e "${GREEN}🎉 ALL TESTS COMPLETED SUCCESSFULLY!${NC}"
    echo ""
    echo "📊 Reports generated in:"
    echo "  - reports/load-test/index.html"
    echo "  - reports/stress-test/index.html"
    echo "  - reports/consolidated-report.html"
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo ""
    echo "📋 Check logs in the 'logs' directory for details"
    exit 1
fi