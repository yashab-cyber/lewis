# Test Data

This directory contains sample data files for testing LEWIS functionality.

## Sample Files

- `sample_logs.txt` - Sample log files for analysis testing
- `sample_config.yaml` - Sample configuration files
- `sample_commands.txt` - Sample command inputs
- `sample_threats.json` - Sample threat intelligence data

## Usage

Test files in this directory are used by the LEWIS test suite to:
- Validate parsing and analysis functionality
- Test threat detection algorithms
- Verify report generation
- Test data import/export features

## Adding Test Data

When adding new test data:
1. Use realistic but non-sensitive data
2. Document the purpose in comments
3. Keep files small (< 1MB each)
4. Follow naming convention: `sample_<purpose>.<extension>`
