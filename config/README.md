# Configuration

YAML configuration files.

## Files

- data_sources.yaml - API URLs
- calculation_params.yaml - Constants (H_now, tolerances)

## Usage

Load in Python:
import yaml
with open('config/data_sources.yaml') as f:
    config = yaml.safe_load(f)
