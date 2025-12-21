# Unit Tests for Agentic AI Projects

This directory contains comprehensive unit tests for all newly added agent projects.

## Test Coverage

### 1. Autonomous SDR (`projects/autonomous_sdr/tests/`)
- **test_lead_discovery.py** (8 tests)
  - Lead scraping and data validation
  - Lead scoring and ranking
  - Duplicate detection
  - Data quality checks
  
- **test_message_composer.py** (8 tests)
  - Message personalization
  - Tone and style validation
  - CTA generation
  - Spam prevention
  
- **test_workflow.py** (8 tests)
  - End-to-end workflow
  - Message sending and tracking
  - Meeting scheduling
  - Rate limiting

### 2. Carbon ESG (`projects/carbon_esg/tests/`)
- **test_data_ingestion.py** (9 tests)
  - CSV/Excel parsing
  - PDF extraction (OCR)
  - Data validation and cleaning
  - Unit conversions
  
- **test_emissions_calc.py** (10 tests)
  - Scope 1, 2, 3 calculations
  - Emission factor application
  - Intensity metrics
  - Uncertainty ranges
  
- **test_report_generation.py** (9 tests)
  - Executive summary
  - Chart generation
  - PDF export
  - Audit trail

### 3. Text2SQL (`projects/external_tools/text2sql/tests/`)
- **test_text2sql_workflow.py** (10 tests)
  - Question to SQL conversion
  - SQL execution
  - DataFrame generation
  - Chart type selection
  - SQL injection prevention

### 4. Draft Generator (`projects/external_tools/Draft_generator/tests/`)
- **test_draft_generator.py** (10 tests)
  - Draft generation
  - Reflection and critique
  - Revision workflow
  - DraftWorkflow class
  - Error handling

## Installation

Install required test dependencies:

```bash
pip install pytest pytest-cov pytest-mock responses
```

## Running Tests

### Run all tests
```bash
cd /path/to/Agentic-AI
pytest
```

### Run tests for specific project
```bash
# Autonomous SDR
pytest projects/autonomous_sdr/tests/

# Carbon ESG
pytest projects/carbon_esg/tests/

# Text2SQL
pytest projects/external_tools/text2sql/tests/

# Draft Generator
pytest projects/external_tools/Draft_generator/tests/
```

### Run specific test file
```bash
pytest projects/autonomous_sdr/tests/test_lead_discovery.py
```

### Run with coverage report
```bash
pytest --cov=projects --cov-report=html
```

This generates an HTML report in `htmlcov/index.html`

### Run with verbose output
```bash
pytest -v
```

### Run only tests matching a pattern
```bash
pytest -k "test_lead"
```

## Test Structure

Each test file follows this pattern:

```python
import pytest
from unittest.mock import Mock, patch

class TestFeatureName:
    """Test suite for feature."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing test data."""
        return {...}
    
    def test_specific_behavior(self, sample_data):
        """Test description.
        
        Verifies:
        - Point 1
        - Point 2
        """
        # Arrange
        # Act
        # Assert
```

## Mocking External Dependencies

Tests use mocking to avoid:
- Real API calls (OpenAI, LinkedIn, etc.)
- Actual database operations
- File system operations
- Network requests

Example:
```python
@patch('openai.ChatCompletion.create')
def test_with_mock(self, mock_openai):
    mock_openai.return_value = Mock(...)
    # Test code
```

## Coverage Goals

- **Target: 80%+ coverage** for all new code
- Critical paths must have 100% coverage
- Edge cases and error conditions must be tested

## CI/CD Integration

Tests run automatically on:
- Every pull request
- Every commit to main branch
- Before deployment

GitHub Actions workflow (`.github/workflows/test.yml`):
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=projects
```

## Writing New Tests

When adding new functionality:

1. **Create test file** in appropriate `tests/` directory
2. **Add fixtures** for common test data
3. **Write test cases** covering:
   - Happy path (normal usage)
   - Edge cases (boundary conditions)
   - Error cases (invalid inputs)
4. **Mock external dependencies**
5. **Run tests** and verify coverage

## Common Issues

### Import errors
If you see `Import "pytest" could not be resolved`:
```bash
pip install pytest
```

### Mock not working
Ensure you're patching the correct import path:
```python
# Patch where it's used, not where it's defined
@patch('my_module.external_api.call')  # ✅ Correct
@patch('external_api.call')            # ❌ Wrong
```

### Tests failing locally
1. Check Python version (3.10+ required)
2. Verify all dependencies installed
3. Ensure `.env` file is configured
4. Run `pytest -v` for verbose output

## Test Maintenance

- **Update tests** when changing functionality
- **Remove obsolete tests** when removing features
- **Keep tests focused** - one behavior per test
- **Use descriptive names** - test name should explain what it tests

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Mock Guide](https://pytest-mock.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

## Summary

- **Total test files**: 10
- **Total test cases**: ~70+
- **Coverage target**: 80%+
- **Run time**: < 1 minute (with mocks)

All tests are fully documented in English with clear explanations of what they test and why.
