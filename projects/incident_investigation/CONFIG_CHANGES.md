# Configuration Updates - Environment Variables

## Summary

All agents now load API keys and configuration from a `.env` file instead of hardcoded values.

## Changes Made

### 1. Created `.env.example` Template
- Contains all configuration options
- Includes OpenAI API keys, database URLs, email settings
- User copies to `.env` and fills in their values

### 2. Created `.gitignore`
- Ensures `.env` files are not committed to version control
- Protects sensitive API keys and credentials
- Ignores output files, logs, and temporary data

### 3. Created `config.py` Module
- Centralized configuration management
- Loads settings from `.env` using python-dotenv
- Provides validation and helper methods
- Includes paths for outputs, reports, diagrams, evidence

### 4. Updated All Agents

**Orchestrator Agent (`orchestrator.py`)**
- Imports `config` module
- Gets API key from `config.OPENAI_API_KEY`
- Uses `config.validate()` to ensure keys are present
- Supports legacy config file parameter for backward compatibility

**Evidence Analysis Agent (`evidence_analyzer.py`)**
- Imports `config` module
- Gets OpenAI configuration from `config.get_openai_client_config()`
- Falls back to environment variables if config not available
- Supports legacy api_key parameter

**Root Cause Analysis Agent (`root_cause_analyzer.py`)**
- Imports `config` module
- Loads API key and model settings from config
- Falls back to environment variables if config not available
- Prints configuration on initialization

**Example Script (`complete_investigation_example.py`)**
- Validates configuration before running
- Shows user-friendly error if API key missing
- Displays loaded configuration settings
- Guides user to create `.env` file

### 5. Updated README.md
- Changed installation instructions to use `.env.example`
- Updated usage examples to show config validation
- Removed hardcoded API key exports

## Usage

### For Users

1. **Copy example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**:
   ```bash
   # Add your API key
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. **Run the system**:
   ```bash
   python examples/complete_investigation_example.py
   ```

### For Developers

The config module provides:

```python
from config import config

# Validate configuration
config.validate()  # Raises ValueError if API key missing

# Get OpenAI settings
openai_config = config.get_openai_client_config()
# Returns: {'api_key': '...', 'model': 'gpt-4o', 'temperature': 0.2}

# Check environment
if config.is_production():
    # Production logic
    pass

# Access paths
config.REPORTS_DIR  # Path to reports directory
config.DIAGRAMS_DIR  # Path to diagrams directory
```

## Security Benefits

✅ API keys not hardcoded in source code  
✅ `.env` file automatically ignored by git  
✅ Separate configurations per environment (dev/prod)  
✅ Centralized credential management  
✅ Validation ensures required keys are present  

## Backward Compatibility

All agents still support the legacy `api_key` parameter:

```python
# Still works, but deprecated
agent = EvidenceAnalysisAgent(api_key="sk-...")

# Recommended: use .env file instead
agent = EvidenceAnalysisAgent()  # Loads from config
```

## Files Modified

- ✅ `config.py` - Created
- ✅ `.env.example` - Created
- ✅ `.gitignore` - Created  
- ✅ `agents/orchestrator.py` - Updated
- ✅ `agents/evidence_analyzer.py` - Updated
- ✅ `agents/root_cause_analyzer.py` - Updated
- ✅ `examples/complete_investigation_example.py` - Updated
- ✅ `README.md` - Updated

## Testing

To test the configuration:

```python
from config import config

# This will raise an error if OPENAI_API_KEY is not set
config.validate()

print(f"API Key loaded: {config.OPENAI_API_KEY[:10]}...")
print(f"Model: {config.OPENAI_MODEL}")
print(f"Environment: {config.ENVIRONMENT}")
```
