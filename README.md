# Table of Contents
- [Table of Contents](#table-of-contents)
- [FM Fact Label: A Configurable and Interactive Visualization of Feature Model Characterizations](#fm-fact-label-a-configurable-and-interactive-visualization-of-feature-model-characterizations)
  - [Available online](#available-online)
  - [Artifact description](#artifact-description)
  - [How to use it](#how-to-use-it)
  - [Deployment of the web application](#deployment-of-the-web-application)
    - [Requirements](#requirements)
    - [Download and install](#download-and-install)
    - [Execution](#execution)
  - [References and third-party software](#references-and-third-party-software)

# FM Fact Label: A Configurable and Interactive Visualization of Feature Model Characterizations
A tool to generate visualizations of feature model characterizations as a fact label similar to the [nutritions fact label](https://en.wikipedia.org/wiki/Nutrition_facts_label).

## Available online
- [FM Fact Label (UMA)](https://fmfactlabel.adabyron.uma.es/)
- [FM Fact Label (US)](https://web.diverso-lab.us.es/fmfactlabel/)


## Artifact description
*FM Fact Label* is an online web-based application that builds an FM characterization and generates its visualization as a fact label.

It offers a web service providing an online form to upload the FM and its metadata. Currently, UVL and FeatureIDE formats are supported.
At this date, the FM characterization provides up to 46 measures, including metrics and analysis results, and it is open to extension with further metrics from the SPL literature.
The fact label visualization is automatically generated using [D3](https://d3js.org/). D3 relies on web standards (HTML, CSS, JavaScript, SVG, and JSON) to combine visualization components and a data-driven approach that allows binding arbitrary data to a Document Object Model (DOM), and then applying data-driven transformations to the DOM. The tool benefits from D3 to provide an interactive and configurable visualization of the FM characterization.

## How to use it
The tool is currently deployed and available online in the following link: 

https://fmfactlabel.adabyron.uma.es/

The main use case of the tool is uploading an FM and automatically generates a visualization of its characterization which can be customized and exported. The use case can be described with the following steps:
- Upload an FM and provide metadata.
- Build the FM characterization and generate the FM fact label.
- Interact with the FM fact label.
- Customize the FM fact label.
- Export the FM fact label and the FM characterization.

<video width="320" height="240" controls>
  <source src="video_demo.mp4" type="video/mp4">
</video>



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

   ** In case that you are running Ubuntu, please install the package python3.9-dev and update wheel and setuptools with the command `pip  install --upgrade pip wheel setuptools` right after step 4.
   
5. Install the dependencies: 
   
   `pip install -r requirements.txt`

   

### Execution
To run the server locally execute the following command:

   `python  run.py`

Access to the web service in the localhost:

http://127.0.0.1:5000 or http://10.141.0.170:5000

## Video

https://user-images.githubusercontent.com/1789503/172726157-11ebe212-41f6-47a1-9ab7-ee378ed1aab7.mp4


## References and third-party software
- [D3: Data-Driven Documents](https://d3js.org/)
- [Python framework for automated analysis of feature models](https://github.com/diverso-lab/core)
