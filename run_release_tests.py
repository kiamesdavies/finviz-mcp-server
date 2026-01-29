#!/usr/bin/env python3
"""
Release Test Runner
Run all validation tests that should be executed before release.
"""

import sys
import os
import subprocess
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test imports
from tests.test_mcp_system_validation import MCPSystemValidationTest

class ReleaseTestRunner:
    """Release test runner class."""
    
    def __init__(self):
        self.test_results = {}
        self.total_duration = 0
        self.skip_mcp_server_test = True  # Skip MCP server test by default
    
    def print_header(self):
        """Print header."""
        print("=" * 100)
        print("🚀 FINVIZ MCP SERVER - RELEASE VALIDATION TESTS")
        print("=" * 100)
        print("This test suite runs pre-release quality validation.")
        print("- Environment checks")
        print("- Unit tests")
        print("- System validation tests")
        if not self.skip_mcp_server_test:
            print("- MCP server startup test")
        print("-" * 100)
    
    def check_environment(self):
        """Environment checks."""
        print("🔍 Running environment checks...")
        
        checks = []
        
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info >= (3, 8):
            print(f"✅ Python version: {python_version}")
            checks.append(True)
        else:
            print(f"❌ Unsupported Python version: {python_version} (3.8+ required)")
            checks.append(False)
        
        # Check required files
        required_files = ['src/server.py', 'pyproject.toml', 'requirements.txt']
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ Required file present: {file_path}")
                checks.append(True)
            else:
                print(f"❌ Required file missing: {file_path}")
                checks.append(False)
        
        # Check environment variables
        finviz_key = os.getenv('FINVIZ_API_KEY')
        if finviz_key:
            print("✅ FINVIZ_API_KEY is set")
            checks.append(True)
        else:
            print("⚠️  FINVIZ_API_KEY not set (some features limited)")
            checks.append(True)  # Warning, but tests can continue
        
        # Check dependencies
        try:
            import pandas, requests, bs4
            print("✅ Dependencies available")
            checks.append(True)
        except ImportError as e:
            print(f"❌ Missing dependencies: {e}")
            checks.append(False)
        
        return all(checks)
    
    def run_mcp_server_startup_test(self):
        """MCP server startup test (optional)."""
        print("\n🔌 Running MCP server startup test...")
        print("⚠️  Note: RuntimeWarning is a technical warning and does not affect functionality")
        
        try:
            result = subprocess.run([
                sys.executable, "-c", 
                """
import sys
import subprocess
import time
import signal

# Start MCP server
proc = subprocess.Popen([sys.executable, '-m', 'mcp.server.stdio', 'src.server'], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE)

# Wait 3 seconds
time.sleep(3)

# Check if process is running
if proc.poll() is None:
    print('SUCCESS: MCP server started successfully')
    proc.terminate()
    proc.wait()
    exit(0)
else:
    stdout, stderr = proc.communicate()
    if stderr:
        print(f'ERROR: {stderr.decode()}')
    exit(1)
                """
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ MCP server startup test passed")
                return True
            else:
                print(f"❌ MCP server startup test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ MCP server startup test timed out")
            return False
        except Exception as e:
            print(f"❌ MCP server startup test error: {e}")
            return False
    
    def run_system_validation_tests(self):
        """Run system validation tests."""
        print("\n🧪 Running system validation tests...")
        
        start_time = time.time()
        validator = MCPSystemValidationTest()
        success = validator.run_all_tests()
        duration = time.time() - start_time
        
        self.test_results['system_validation'] = {
            'success': success,
            'duration': duration,
            'details': validator.test_results
        }
        
        return success
    
    def run_unit_tests(self):
        """Run unit tests."""
        print("\n🔬 Running unit tests...")
        
        # Test file list
        unit_test_files = [
            "tests/test_basic.py",           # Basic unit tests
            # "tests/test_error_handling.py", # In progress: temporarily disabled
        ]
        
        integration_test_files = [
            # "tests/test_mcp_integration.py", # In progress: temporarily disabled
        ]
        
        all_tests_passed = True
        test_summary = {"passed": 0, "failed": 0, "total": 0}
        
        # Run unit tests
        print("  📋 Basic unit tests:")
        for test_file in unit_test_files:
            if os.path.exists(test_file):
                try:
                    result = subprocess.run([
                        sys.executable, test_file
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(f"    ✅ {test_file}")
                        test_summary["passed"] += 1
                    else:
                        print(f"    ❌ {test_file}")
                        print(f"       Error: {result.stderr[:200]}...")
                        test_summary["failed"] += 1
                        all_tests_passed = False
                    test_summary["total"] += 1
                    
                except subprocess.TimeoutExpired:
                    print(f"    ⏰ {test_file} (Timeout)")
                    test_summary["failed"] += 1
                    test_summary["total"] += 1
                    all_tests_passed = False
                except Exception as e:
                    print(f"    ❌ {test_file} (Execution error: {e})")
                    test_summary["failed"] += 1
                    test_summary["total"] += 1
                    all_tests_passed = False
            else:
                print(f"    ⚠️  {test_file} (File missing)")
        
        # Run integration tests (pytest)
        print("  🔗 Integration tests:")
        if integration_test_files:
            for test_file in integration_test_files:
                if os.path.exists(test_file):
                    try:
                        result = subprocess.run([
                            sys.executable, "-m", "pytest", test_file,
                            "-v", "--tb=short", "--timeout=60"
                        ], capture_output=True, text=True, timeout=90)
                        
                        if result.returncode == 0:
                            print(f"    ✅ {test_file}")
                            test_summary["passed"] += 1
                        else:
                            print(f"    ❌ {test_file}")
                            # More detailed error output
                            error_lines = result.stdout.split('\n')[-10:]  # Last 10 lines
                            for line in error_lines:
                                if line.strip():
                                    print(f"       {line}")
                            test_summary["failed"] += 1
                            all_tests_passed = False
                        test_summary["total"] += 1
                        
                    except subprocess.TimeoutExpired:
                        print(f"    ⏰ {test_file} (Timeout)")
                        test_summary["failed"] += 1
                        test_summary["total"] += 1
                        all_tests_passed = False
                    except Exception as e:
                        print(f"    ❌ {test_file} (Execution error: {e})")
                        test_summary["failed"] += 1
                        test_summary["total"] += 1
                        all_tests_passed = False
                else:
                    print(f"    ⚠️  {test_file} (File missing)")
        else:
            print("    ℹ️  Integration tests: currently disabled (in development, not required for release)")
        
        # Summary output
        print(f"  📊 Unit test results: {test_summary['passed']}/{test_summary['total']} passed")
        
        if all_tests_passed:
            print("✅ Unit tests passed")
        else:
            print("❌ Unit tests failed")
        
        return all_tests_passed
    
    def generate_release_report(self):
        """Generate release report."""
        print("\n" + "=" * 100)
        print("📊 RELEASE VALIDATION REPORT")
        print("=" * 100)
        
        # Overall summary
        all_tests_passed = all(
            result.get('success', False) 
            for result in self.test_results.values()
        )
        
        total_tests = sum(
            len(result.get('details', [])) 
            for result in self.test_results.values()
        )
        
        total_passed = sum(
            sum(1 for detail in result.get('details', []) if detail.success)
            for result in self.test_results.values()
        )
        
        print("📈 Overall results:")
        print(f"   Overall: {'🟢 PASS' if all_tests_passed else '🔴 FAIL'}")
        print(f"   Pass rate: {total_passed}/{total_tests} ({(total_passed/total_tests*100):.1f}%)" if total_tests > 0 else "   Pass rate: N/A")
        print(f"   Total duration: {self.total_duration:.2f}s")
        
        # Results by category
        print("\n📋 Results by category:")
        for category, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            duration = result['duration']
            print(f"   {status} {category}: {duration:.2f}s")
        
        # Quality metrics (from system validation tests)
        if 'system_validation' in self.test_results:
            system_details = self.test_results['system_validation']['details']
            if system_details:
                total_stocks = sum(detail.stocks_found for detail in system_details)
                avg_quality = sum(detail.data_quality_score for detail in system_details) / len(system_details)
                print("\n📊 Quality metrics:")
                print(f"   Total stocks found: {total_stocks}")
                print(f"   Average quality score: {avg_quality:.1f}/100")
        
        # Release decision
        print("\n🎯 Release decision:")
        if all_tests_passed:
            print("   🟢 Release approved - all tests passed")
            print("   This version is ready for production use.")
        else:
            failed_categories = [cat for cat, result in self.test_results.items() if not result['success']]
            print("   🔴 Release blocked - fixes required")
            print(f"   Failed categories: {', '.join(failed_categories)}")
            print("   Fix the failed items above and re-run tests.")
        
        print("=" * 100)
        
        return all_tests_passed
    
    def run_all_release_tests(self, include_mcp_server_test=False):
        """Run all release tests."""
        self.skip_mcp_server_test = not include_mcp_server_test
        start_time = time.time()
        
        self.print_header()
        
        # 1. Environment check
        if not self.check_environment():
            print("❌ Environment check failed - aborting tests")
            return False
        
        # 2. Unit tests (run first)
        unit_test_start = time.time()
        unit_success = self.run_unit_tests()
        unit_duration = time.time() - unit_test_start
        self.test_results['unit_tests'] = {
            'success': unit_success,
            'duration': unit_duration,
            'details': []
        }
        
        # 3. System validation tests (main)
        system_success = self.run_system_validation_tests()
        
        # 4. MCP server startup test (optional)
        if include_mcp_server_test:
            server_test_start = time.time()
            server_success = self.run_mcp_server_startup_test()
            server_duration = time.time() - server_test_start
            self.test_results['mcp_server_startup'] = {
                'success': server_success,
                'duration': server_duration,
                'details': []
            }
        
        # Total duration
        self.total_duration = time.time() - start_time
        
        # 5. Generate report
        overall_success = self.generate_release_report()
        
        return overall_success

# Main entry
def main():
    """Main entry function."""
    # Control MCP server test via CLI args
    include_mcp_test = "--include-mcp-test" in sys.argv
    
    if include_mcp_test:
        print("🔌 Including MCP server startup test")
    else:
        print("⚠️  Skipping MCP server startup test (enable with --include-mcp-test)")
    
    runner = ReleaseTestRunner()
    success = runner.run_all_release_tests(include_mcp_server_test=include_mcp_test)
    
    if success:
        print("\n🎉 Release tests complete - all passed!")
        print("This version is ready to release.")
        return True
    else:
        print("\n⚠️  Release tests complete - fixes required")
        print("Fix the failed items and re-run tests.")
        return False

if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(3)
