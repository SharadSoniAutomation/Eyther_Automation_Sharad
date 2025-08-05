import subprocess
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