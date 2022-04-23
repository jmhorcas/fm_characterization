# Table of Contents
- [Table of Contents](#table-of-contents)
- [Variability in Data Visualization: a Software Product Line Approach](#variability-in-data-visualization-a-software-product-line-approach)
  - [Artifact description](#artifact-description)
  - [How to use it](#how-to-use-it)
    - [Requirements](#requirements)
    - [Download and install](#download-and-install)
    - [Execution](#execution)
    - [Results output](#results-output)
  - [Validation replication](#validation-replication)
  - [References and third-party software](#references-and-third-party-software)

# FM Characterization: A Fact Label for Feature Models
Characterization and visualization of feature models in a fact label similar to the [nutritions fact label](https://en.wikipedia.org/wiki/Nutrition_facts_label).

## Artifact description
Under construction :construction:

## How to use it
Under construction :construction:

## Deployment of the web application

### Requirements
- [Python 3.9+](https://www.python.org/)

### Download and install
1. Install [Python 3.9+](https://www.python.org/)
2. Clone this repository and enter into the main directory:

    `git clone https://github.com/jmhorcas/fm_characterization`

    `cd fm_characterization` 
3. Create a virtual environment: 
   
   `python -m venv env`
4. Activate the environment: 
   
   In Linux: `source env/bin/activate`

   In Windows: `.\env\Scripts\Activate`
5. Install the dependencies: 
   
   `pip install -r requirements.txt`

   ** In case that you are running Ubuntu, please install the package python3.9-dev and update wheel and setuptools with the command `pip  install --upgrade pip wheel setuptools` right after step 4.

### Execution
To run the server locally execute the following command:

   `python  run.py`

## References and third-party software
- [D3: Data-Driven Documents](https://d3js.org/)
- [Python framework for automated analysis of feature models](https://github.com/diverso-lab/core)
