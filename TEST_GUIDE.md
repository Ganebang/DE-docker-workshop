# Testing Guide - NYC Taxi Data Pipeline

Complete guide to testing the data ingestion pipeline.

## Overview

The test suite provides comprehensive coverage of:
- **Argument parsing** (test_pipeline.py)
- **Argument validation** (test_pipeline.py)
- **Database operations** (test_database.py)
- **Configuration management** (test_database.py)
- **Error handling** (test_pipeline.py and test_database.py)

## Test Structure

```
test/
├── test_pipeline.py          # CLI and configuration tests (~350 lines)
├── test_database.py          # Database operation tests (~250 lines)
├── conftest.py              # Pytest fixtures (if needed)
└── __init__.py              # Test package marker
```

## Prerequisites

### Required Packages

```bash
cd pipeline
uv sync  # Installs all dependencies including pytest
```

Or install pytest directly:

```bash
pip install pytest pytest-cov
```

### Optional for Full Coverage

```bash
pip install pytest-mock pytest-xdist
```

## Running Tests

### Option 1: Using run_tests.py Script

```bash
# Run all tests with coverage report
python run_tests.py

# Run only unit tests
python run_tests.py unit

# Run only database tests
python run_tests.py database

# Run tests without coverage (faster)
python run_tests.py quick
```

### Option 2: Using pytest Directly

```bash
# Run all tests
pytest test/ -v

# Run specific test file
pytest test/test_pipeline.py -v

# Run specific test class
pytest test/test_pipeline.py::TestArgumentParsing -v

# Run specific test
pytest test/test_pipeline.py::TestArgumentParsing::test_parse_arguments_defaults -v

# Run with coverage
pytest test/ --cov=pipeline --cov-report=html

# Run in parallel (faster)
pytest test/ -n auto

# Stop on first failure
pytest test/ -x

# Show print statements
pytest test/ -s

# Only show failures
pytest test/ --tb=short
```

### Option 3: Using VS Code

1. Install Python extension
2. Install pytest
3. Click "Test" in activity bar
4. Right-click test file and select "Run Tests"

## Test Organization

### test_pipeline.py - CLI & Configuration Tests

**TestArgumentParsing** - Command-line argument parsing
- `test_parse_arguments_defaults` - Default values
- `test_parse_arguments_custom_values` - Custom parameters
- `test_parse_arguments_database_params` - Database parameters
- `test_parse_arguments_log_levels` - Log level parsing
- `test_parse_arguments_help` - Help text
- `test_parse_arguments_invalid_argument` - Invalid args

**TestArgumentValidation** - Argument value validation
- `test_validate_year_valid_range` - Year range 2009-2025
- `test_validate_year_too_early` - Year < 2009
- `test_validate_year_too_late` - Year > 2025
- `test_validate_month_valid` - Months 1-12
- `test_validate_month_invalid_low` - Month < 1
- `test_validate_month_invalid_high` - Month > 12
- `test_validate_chunk_size_valid` - Positive chunk sizes
- `test_validate_chunk_size_invalid_zero` - Zero chunk size
- `test_validate_chunk_size_invalid_negative` - Negative chunk size
- `test_validate_log_level_valid` - Valid log levels
- `test_validate_log_level_invalid` - Invalid log levels

**TestDatabaseURLConstruction** - Database URL building
- `test_build_database_url_basic` - Local database
- `test_build_database_url_remote` - Remote host
- `test_build_database_url_special_characters` - Special chars in password
- `test_build_database_url_custom_port` - Custom port

**TestDataURLGeneration** - Data source URL building
- `test_build_data_url_2021_january` - Specific date
- `test_build_data_url_2020_december` - Year boundary
- `test_build_data_url_format` - URL format validation

**TestEnvironmentVariableHandling** - Environment variable support
- `test_db_host_from_environment` - DB_HOST variable
- `test_db_user_from_environment` - DB_USER variable
- `test_db_password_from_environment` - DB_PASSWORD variable
- `test_environment_variable_override` - CLI overrides env vars

**TestConfigurationDefaults** - Default values
- `test_default_database_values` - Database defaults
- `test_default_chunk_size` - Chunk size default
- `test_default_table_name` - Table name default
- `test_default_log_level` - Log level default

**TestIntegration** - Integration scenarios
- `test_valid_configuration_flow` - Full configuration
- `test_error_in_validation` - Error handling
- `test_multiple_months_processing` - Batch processing

**TestErrorHandling** - Edge cases
- `test_invalid_year_type` - Invalid type handling
- `test_invalid_month_type` - Invalid type handling
- `test_invalid_chunk_size_type` - Invalid type handling
- `test_boundary_year_values` - Boundary values
- `test_boundary_month_values` - Boundary values

### test_database.py - Database & Configuration Tests

**TestDatabaseConnection** - Database connectivity
- `test_database_engine_creation` - Engine creation
- `test_database_connection_string_format` - URL format
- `test_database_config_from_args` - Config from args

**TestTableCreation** - Table schema tests
- `test_create_table_schema` - Schema validation

**TestDataIngestion** - Data ingestion logic
- `test_data_types_configuration` - Data type setup
- `test_parse_dates_configuration` - Date parsing setup
- `test_chunked_reading_simulation` - Chunked reading

**TestLoggingConfiguration** - Logging setup
- `test_logging_setup` - Logger creation
- `test_log_level_setting` - Log level configuration

**TestDataURLConstruction** - URL construction
- `test_github_release_url_format` - GitHub URL format
- `test_all_months_url_generation` - All months
- `test_historical_year_url_generation` - Historical years

**TestConfigurationManagement** - Configuration structure
- `test_default_config_structure` - Config structure
- `test_database_config_keys` - Database config keys
- `test_default_values_are_reasonable` - Value validation

## Test Statistics

- **Total Tests**: 60+
- **Test Files**: 2
- **Lines of Test Code**: 600+
- **Coverage Target**: >80% of pipeline code

### Breakdown by Category

| Category | Count | File |
|----------|-------|------|
| Argument Parsing | 6 | test_pipeline.py |
| Argument Validation | 13 | test_pipeline.py |
| Database URL | 4 | test_pipeline.py |
| Data URL | 3 | test_pipeline.py |
| Environment Variables | 4 | test_pipeline.py |
| Configuration | 4 | test_pipeline.py |
| Integration | 3 | test_pipeline.py |
| Error Handling | 5 | test_pipeline.py |
| Database Connection | 3 | test_database.py |
| Table Creation | 1 | test_database.py |
| Data Ingestion | 3 | test_database.py |
| Logging | 2 | test_database.py |
| URL Construction | 3 | test_database.py |
| Config Management | 3 | test_database.py |

## Example Test Runs

### Run All Tests

```bash
$ pytest test/ -v

test/test_pipeline.py::TestArgumentParsing::test_parse_arguments_defaults PASSED
test/test_pipeline.py::TestArgumentParsing::test_parse_arguments_custom_values PASSED
test/test_pipeline.py::TestArgumentValidation::test_validate_year_valid_range PASSED
test/test_pipeline.py::TestArgumentValidation::test_validate_year_too_early FAILED
...

======= 60 passed in 2.34s =======
```

### Run with Coverage

```bash
$ pytest test/ --cov=pipeline --cov-report=html

coverage: platform linux -- Python 3.13.11, pytest-7.0.0, pluggy-1.0.0
------------ coverage: 85% ------------

Name                        Stmts   Miss  Cover
─────────────────────────────────────────────
pipeline/simple_data_ingestion.py   150     25    83%
pipeline/pipeline.py                 45      8    82%
─────────────────────────────────────────────
TOTAL                              195     33    83%

====== 60 passed in 3.12s ======
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.13
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-cov
        cd pipeline
        uv sync
    
    - name: Run tests
      run: pytest test/ --cov=pipeline
```

## Writing New Tests

### Test File Template

```python
"""Test module description"""

import pytest
from unittest.mock import Mock, patch

# Import what you're testing
from simple_data_ingestion import function_to_test


class TestMyFeature:
    """Test class description"""
    
    def test_basic_case(self):
        """Test description"""
        # Arrange
        input_data = "test"
        expected = "result"
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected
    
    def test_error_case(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            function_to_test("invalid")
```

### Mocking Example

```python
from unittest.mock import patch, MagicMock

@patch('simple_data_ingestion.create_engine')
def test_with_mock(mock_engine):
    """Test with mocked dependency"""
    mock_engine.return_value = MagicMock()
    
    # Your test code here
    assert mock_engine.called
```

## Debugging Tests

### Run with Output

```bash
# Show print statements
pytest test/ -s

# Show local variables on failure
pytest test/ -l

# Full traceback
pytest test/ --tb=long
```

### Debug Single Test

```bash
# Run one test with debugging
pytest test/test_pipeline.py::TestArgumentParsing::test_parse_arguments_defaults -s

# Use pdb debugger
pytest test/test_pipeline.py -k test_name --pdb
```

## Performance Optimization

### Run Tests in Parallel

```bash
# Requires: pip install pytest-xdist

pytest test/ -n auto     # Use all CPU cores
pytest test/ -n 4        # Use 4 workers
```

### Profile Test Execution

```bash
# Show slowest tests
pytest test/ --durations=10

# Show test execution duration
pytest test/ --durations=0
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:

```bash
# Ensure you're in the right directory
cd /workspaces/DE-docker-workshop

# Verify pytest is installed
pip list | grep pytest

# Reinstall dependencies
pip install pytest pytest-cov
```

### Database Tests Failing

Database tests use mocking and don't require a running database. If they fail:

```bash
# Check if mocking is working
pytest test/test_database.py -v

# Verify sqlalchemy is installed
pip list | grep sqlalchemy
```

### Timeout Issues

```bash
# Increase timeout
pytest test/ --timeout=300

# Run without timeout (not recommended)
pytest test/ -p no:timeout
```

## Best Practices

1. **Keep tests independent** - Each test should run standalone
2. **Use descriptive names** - Test names should describe what they test
3. **Follow AAA pattern** - Arrange, Act, Assert
4. **Mock external dependencies** - Don't rely on real database/network
5. **Test edge cases** - Boundary values, invalid inputs, errors
6. **Keep tests fast** - Aim for < 1s per test
7. **Review coverage** - Aim for > 80% coverage

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/how-to-use-fixtures.html)
- [Pytest Plugins](https://docs.pytest.org/en/stable/plugins.html)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest test/` | Run all tests |
| `pytest test/ -v` | Verbose output |
| `pytest test/ -s` | Show print statements |
| `pytest test/ -k keyword` | Run matching tests |
| `pytest test/ --cov` | Generate coverage |
| `pytest test/ -x` | Stop on first failure |
| `pytest test/ --tb=short` | Short traceback |
| `python run_tests.py` | Run with script |
| `python run_tests.py unit` | Run unit tests |
| `python run_tests.py quick` | Fast run (no coverage) |

---

**Happy Testing! 🧪**
