# Add Unit Tests for New Agent Projects

## Description
We need comprehensive unit tests for the recently added agent projects to ensure code quality, reliability, and ease of maintenance.

## Projects Missing Tests

### 1. Autonomous SDR (`projects/autonomous_sdr/`)
- [ ] Test lead discovery and filtering logic
- [ ] Test message personalization and template rendering
- [ ] Test scoring/ranking algorithms
- [ ] Mock external API calls (LinkedIn, email providers)

### 2. Carbon ESG (`projects/carbon_esg/`)
- [ ] Test data ingestion and normalization
- [ ] Test emissions calculation logic with known inputs
- [ ] Test emission factor lookups and unit conversions
- [ ] Test report generation pipeline
- [ ] Mock file uploads and database operations

### 3. Text2SQL Workflow (`projects/external_tools/text2sql/`)
- [ ] Test `question_to_sql()` with various question types
- [ ] Test `run_sql_to_df()` with sample SQLite database
- [ ] Test `df_to_chart()` with different DataFrame shapes
- [ ] Test edge cases (empty results, malformed SQL, etc.)

### 4. Draft Generator (`projects/external_tools/Draft_generator/`)
- [ ] Test `DraftWorkflow.generate_draft()` 
- [ ] Test `DraftWorkflow.reflect_on_draft()`
- [ ] Test `DraftWorkflow.revise_draft()`
- [ ] Test `run_full_workflow()` end-to-end
- [ ] Mock OpenAI API calls to avoid cost and rate limits
- [ ] Test standalone functions for backward compatibility

## Testing Standards

### Required Coverage
- Minimum 80% code coverage for all new modules
- All public functions and methods must have tests
- Edge cases and error conditions must be tested

### Test Structure
```
projects/
  autonomous_sdr/
    tests/
      __init__.py
      test_lead_discovery.py
      test_message_composer.py
      test_workflow.py
  carbon_esg/
    tests/
      __init__.py
      test_data_ingestion.py
      test_emissions_calc.py
      test_report_generation.py
  external_tools/
    text2sql/
      tests/
        __init__.py
        test_text2sql_workflow.py
    Draft_generator/
      tests/
        __init__.py
        test_draft_generator.py
```

### Dependencies
- pytest
- pytest-cov (for coverage reports)
- pytest-mock (for mocking external APIs)
- responses or httpretty (for HTTP mocking)

## Implementation Plan

1. **Phase 1: Setup**
   - Create test directory structure
   - Add pytest configuration in `pyproject.toml` or `pytest.ini`
   - Set up GitHub Actions workflow for automated testing

2. **Phase 2: Core Tests**
   - Draft Generator tests (highest priority - most complete code)
   - Text2SQL workflow tests
   - Carbon ESG calculation tests
   - Autonomous SDR tests

3. **Phase 3: Integration & Coverage**
   - End-to-end workflow tests
   - Achieve 80%+ coverage
   - Add CI/CD quality gates

## Acceptance Criteria
- [ ] All new projects have test files
- [ ] Tests run successfully with `pytest`
- [ ] Coverage report shows ≥80% for new code
- [ ] GitHub Actions workflow runs tests on every PR
- [ ] README files updated with test running instructions

## Additional Context
These tests are critical for:
- Safe refactoring and feature additions
- Catching regressions early
- Documenting expected behavior
- Onboarding new contributors

## Related Files
- `Agentic-AI/TESTING_GUIDE.md` (existing testing patterns)
- `Agentic-AI/projects/customer_support/test_support_agent.py` (example test structure)

## Priority
**High** - These are production-ready agents that need quality assurance before wider deployment.

---

**Labels:** `testing`, `enhancement`, `good first issue` (for contributors)
**Assignee:** (assign to appropriate team member)
**Milestone:** Q1 2026 Testing Sprint
