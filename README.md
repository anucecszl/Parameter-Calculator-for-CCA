# Parameter-Calculator-for-CCA
An empirical parameter calculator for Compositionally Complex Alloys

## Installation (in your command prompt)
1. git clone this repository. 
   ```
   $ git clone https://github.com/ZhipengGaGa/Parameter-Calculator-for-CCA.git
   ```
2. download and install python 3.7 or any version released after python 3.7 (https://www.python.org/downloads/windows/)
3. install virtualenv:
   ```
   $ pip install virtualenv
   ```
4. create and activate a virtual environment 
   ```
   $ python -m venv ep-calculator
   $ ep-calculator\Scripts\activate.bat
   ```
5. open the project and install the required python packages  
   ```
   $ cd Parameter-Calculator-for-CCA
   $ pip install -r requirements
   ```
6. run the empirical parameter calculator user interface  
   ```
   $ python calculator_UI.py
   ```
   
## Instruction
1. This application supports calculations for 14 empirical parameters of any given compositionally complex alloys. 
   The parameters are: 
   *entropy of mixing (ΔS)
   *average atomic radius (a)
   *atomic size difference (δ)
   *enthalpy of mixing (ΔH)
   *standard deviation of enthalpy (std H)
   *average melting point (Tm)
   *standard deviation of melting point (ΔTm)
   *average electronegativity (X)
   *standard deviation of electronagativity (ΔX)
   *valence electron concentration (VEC)
   *standard deviation of valence electron concentration (ΔVEC)
   *density of the given alloy (density)
   *market price (retrieved from http://www.leonland.de/elements_by_price/en/list)
2. When calculating parameters for individual alloys, please enter the element names and molar ratios into the given entries, then click    'Show Empirical Properties' button. 
3. To do batch calculation, from 'File' click 'Batch Calculation', select the input and output file path, then hit 'Start Calculation'.
   * The input file should be either a .csv or . xlsx file. 
   * And the chemical formulas of the alloys must be in the same format as 'test_dataset.xlsx'.
