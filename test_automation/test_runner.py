'''import subprocess
import sys
import os

def run_tests(test_type="all"):
    """Simple test runner for login automation tests"""
    
    # Ensure we're in the right directory
    if not os.path.exists("tests/test_login.py"):
        print("Error: test_login.py not found. Run from project root directory.")
        return False
    
    # Base command
    base_cmd = ["pytest", "tests/test_login.py", "-v", "--headed", "--screenshot=on"]
    
    # Test type selection
    if test_type == "positive":
        base_cmd.extend(["-m", "positive"])
    elif test_type == "negative":
        base_cmd.extend(["-m", "negative"])
    
    try:
        print(f"Running {test_type} tests...")
        result = subprocess.run(base_cmd, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    # Simple command line interface
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if test_type not in ["all", "positive", "negative"]:
        print("Usage: python test_runner.py [all|positive|negative]")
        sys.exit(1)
    
    success = run_tests(test_type)
    sys.exit(0 if success else 1)

import subprocess
import sys
import os

def run_tests(test_type="all"):
    """Enhanced test runner for all test modules"""

    # Ensure we're in the right directory
    if not os.path.exists("tests/"):
        print("Error: tests directory not found. Run from project root directory.")
        return False

    # Base command
    base_cmd = ["pytest", "-v", "--headed", "--screenshot=on"]

    # Test type selection
    if test_type == "login":
        base_cmd.extend(["tests/test_login.py"])
    elif test_type == "dashboard":
        base_cmd.extend(["tests/test_dashboard.py"])
    elif test_type == "claims":
        base_cmd.extend(["tests/test_claim_management.py"])
    elif test_type == "positive":
        base_cmd.extend(["-m", "positive"])
    elif test_type == "negative":
        base_cmd.extend(["-m", "negative"])
    elif test_type == "high":
        base_cmd.extend(["-m", "high"])
    elif test_type == "smoke":
        base_cmd.extend(["-m", "smoke"])
    elif test_type == "all":
        base_cmd.extend(["tests/"])
    else:
        print("Invalid test type. Available options:")
        print("- all: Run all tests")
        print("- login: Run only login tests")
        print("- dashboard: Run only dashboard tests")
        print("- claims: Run only claim management tests")
        print("- positive: Run only positive tests")
        print("- negative: Run only negative tests")
        print("- high: Run only high priority tests")
        print("- smoke: Run only smoke tests")
        return False

    try:
        print(f"Running {test_type} tests...")
        result = subprocess.run(base_cmd, capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    # Enhanced command line interface
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    success = run_tests(test_type)
    sys.exit(0 if success else 1)'''

import subprocess
import sys
import os
import json
import re
from datetime import datetime

def run_tests(test_type="all"):
    """Enhanced test runner with comprehensive reporting"""

    # Ensure we're in the right directory
    if not os.path.exists("tests/"):
        print("Error: tests directory not found. Run from project root directory.")
        return False

    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    # Base command - FIXED: Removed problematic JSON report arguments
    base_cmd = ["pytest", "-v", "--headed", "--screenshot=on"]

    # Test type selection
    if test_type == "login":
        base_cmd.extend(["tests/test_login.py"])
    elif test_type == "dashboard":
        base_cmd.extend(["tests/test_dashboard.py"])
    elif test_type == "claims":
        base_cmd.extend(["tests/test_claim_management.py"])
    elif test_type == "positive":
        base_cmd.extend(["-m", "positive"])
    elif test_type == "negative":
        base_cmd.extend(["-m", "negative"])
    elif test_type == "high":
        base_cmd.extend(["-m", "high"])
    elif test_type == "medium":
        base_cmd.extend(["-m", "medium"])
    elif test_type == "smoke":
        base_cmd.extend(["-m", "smoke"])
    elif test_type == "all":
        base_cmd.extend(["tests/"])
    else:
        print("Invalid test type. Available options:")
        print_test_options()
        return False

    try:
        print(f"🚀 Running {test_type} tests...")
        print(f"Command: {' '.join(base_cmd)}")
        print("="*70)
        
        result = subprocess.run(base_cmd, capture_output=True, text=True)
        
        print("\n" + "="*70)
        print(f"TEST EXECUTION COMPLETED - {test_type.upper()}")
        print("="*70)
        
        # Display console output
        print(result.stdout)
        
        if result.stderr:
            print("\nWarnings/Errors:")
            print(result.stderr)
        
        # Parse results and generate report immediately
        # The comprehensive report will be generated by conftest.py pytest_sessionfinish hook
        
        print("\n" + "="*70)
        print("📊 REPORTS GENERATED:")
        print("="*70)
        print("✅ Comprehensive HTML Report: reports/latest_test_report.html")
        print("📸 Screenshots: screenshots/ directory")
        print("="*70)
        print("\n🌐 Open reports/latest_test_report.html in your browser to view the comprehensive report!")
        
        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def print_test_options():
    """Display available test execution options"""
    print("\n=== AVAILABLE TEST OPTIONS ===")
    print("  login      - Login tests only")
    print("  dashboard  - Dashboard tests only") 
    print("  claims     - Claim management tests only")
    print("  positive   - All positive tests")
    print("  negative   - All negative tests")
    print("  high       - High priority tests")
    print("  medium     - Medium priority tests")
    print("  smoke      - Smoke tests")
    print("  all        - All tests (default)")

if __name__ == "__main__":
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if test_type in ["--help", "-h", "help"]:
        print_test_options()
        sys.exit(0)
    
    success = run_tests(test_type)
    sys.exit(0 if success else 1)