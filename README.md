# Parameter-Calculator-for-CCA
An empirical parameter calculator for Compositionally Complex Alloys

### Authors
Zhipeng Li (u6766505@anu.edu.au), Will Nash

## Installation
1. Clone this repository. 
   ```
   $ git clone https://github.com/ZhipengGaGa/Parameter-Calculator-for-CCA.git
   ```
2. Download and install python 3.7 or any version released after python 3.7 (https://www.python.org/downloads/)

3. Install virtualenv:
   ```
   $ pip install virtualenv
   ```
4. Create and activate a virtual environment named 'epcalc'
   ```
   $ python -m venv epcalc
   (for Windows)
      $ epcalc\Scripts\activate.bat
   (for MacOS)
      $ cd epcalc
      $ source bin/activate
      $ cd ..
   ```
5. Change to the project directory and install the required python packages  
   ```
   $ cd Parameter-Calculator-for-CCA
   $ pip install -r requirements
   ```
6. Run the empirical parameter calculator user interface  
   ```
   $ python calculator_UI.py
   ```
   
## Instruction
1. This application supports calculations for 14 empirical parameters of any given compositionally complex alloys. 

   The parameters are: 
   * entropy of mixing (ΔS)
   * average atomic radius (a)
   * atomic size difference (δ)
   * enthalpy of mixing (ΔH)
   * standard deviation of enthalpy (std H)
   * average melting point (Tm)
   * standard deviation of melting point (ΔTm)
   * average electronegativity (X)
   * standard deviation of electronagativity (ΔX)
   * valence electron concentration (VEC)
   * standard deviation of valence electron concentration (ΔVEC)
   * the unitless parameter Omega (Ω)
   * density
   * market price (retrieved from http://www.leonland.de/elements_by_price/en/list)
   
2. When calculating parameters for individual alloys, please enter the element names and molar ratios into the given entries, then click 'Show Empirical Properties' button. 

3. To do batch calculation, from 'File' click 'Batch Calculation', select the input and output file path, then hit 'Start Calculation'.
   * The input file should be either a '.csv' or '.xlsx' file. 
   * The chemical formulas of the alloys must be in the same format as 'test_dataset.xlsx'.
   
   A '.csv' file named 'batch_calculation_results.csv' will be created in the selected output directory. 
   
  
