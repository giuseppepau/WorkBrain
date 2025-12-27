# WorkBrain

Python project for computational modeling of brain connectivity and turbulence dynamics, developed during my internship at the **Polytechnic University of Girona**.

---

## Overview

This repository contains the `WorkBrain` project, including code for:  

- Analysis of Structural Connectivity (SC) and long-range connections (Clong)  
- Calculation of EDR (Exponential Distance Rule) and related metrics  
- Visualization of connectivity matrices and turbulence-related plots  

---

## Dependencies

This project relies on two external libraries that are **not included** in this repository:

1. **LibBrain** – for data loading and processing  
   - Repository or installation instructions should be obtained separately.  
2. **neuronumba** – for distance rules and observables  
   - Only the `distance_rule.py` file was modified; the rest of the library is assumed to be available.  

Make sure these libraries are installed and available in your Python environment, otherwise the code will not run.

---

## Installation

1. Clone this repository:  

```bash
git clone https://github.com/giuseppepau/WorkBrain.git
cd WorkBrain
