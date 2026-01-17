"""
Test runner script for the NYC Taxi Data Pipeline

This script runs all tests with various options and generates reports.
"""

import subprocess
import sys
from pathlib import Path


def run_all_tests(verbose=True, coverage=True):
    """Run all tests"""
    cmd = ["pytest", "test/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=pipeline", "--cov-report=html", "--cov-report=term"])
    
    return subprocess.run(cmd, cwd=Path(__file__).parent)


def run_unit_tests():
    """Run only unit tests"""
    return subprocess.run(
        ["pytest", "test/test_pipeline.py", "-v"],
        cwd=Path(__file__).parent
    )


def run_database_tests():
    """Run only database tests"""
    return subprocess.run(
        ["pytest", "test/test_database.py", "-v"],
        cwd=Path(__file__).parent
    )


def run_integration_tests():
    """Run only integration tests"""
    return subprocess.run(
        ["pytest", "test/", "-m", "integration", "-v"],
        cwd=Path(__file__).parent
    )


def run_tests_with_markers(marker):
    """Run tests with specific marker"""
    return subprocess.run(
        ["pytest", "test/", "-m", marker, "-v"],
        cwd=Path(__file__).parent
    )


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Running all tests with coverage...")
        result = run_all_tests()
    else:
        command = sys.argv[1]
        
        if command == "all":
            print("Running all tests...")
            result = run_all_tests()
        elif command == "unit":
            print("Running unit tests...")
            result = run_unit_tests()
        elif command == "database":
            print("Running database tests...")
            result = run_database_tests()
        elif command == "integration":
            print("Running integration tests...")
            result = run_integration_tests()
        elif command == "quick":
            print("Running tests without coverage...")
            result = run_all_tests(coverage=False)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: all, unit, database, integration, quick")
            return 1
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
