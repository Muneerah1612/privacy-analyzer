# Privacy Analyzer

Privacy analyzer is a python package that allows users to check their transactions and give traceability reports. The privacy analyzer checks transactions based on certain heuristics, which include:
1. Address reuse
1. Largest amount output
1. Script type
1. Round number payment
1. Inputs from same transaction
1. Exact amount payment
1. Equal amount (coinjoin)

## Installation Instructions
### Install with pip

```shell
pip install privacy-analyzer
```
The following packages would be installed with the package

### Development Installation
1. Create a directory `mkdir working-directory`
1. Enter into the directory `cd working-directory`
1. Clone the repository `git clone https://github.com/toshmanuel/privacy-analyzer`
1. Enter into the cloned directory `cd privacy-analyzer`
1. Create a virtual environment with the virtualenv `virtualenv -p python3 venv/privacy-analyzer`
1. Install dependencies `pip install requirements.txt`

### Running Tests



## Some Examples