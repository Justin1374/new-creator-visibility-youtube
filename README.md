# DEL02.2: Initial Computational Prototype

## 1. Project Overview and Reference to DEL02.1
This repository contains the Initial Computational Prototype for Deliverable 2. It simulates a simplified YouTube Home page recommendation feed to explore differences in visibility between new and established creators under different popularity weighting conditions.

**For the full project rationale, representation explanation and interpretation of the outputs, refer to the DEL02.1 Initial Computational Prototype Report (located in `docs/DEL02.1_Initial_Computational_Prototype_Report.md`).** The report explains why these specific agents and rules were chosen and what the results do (and do not) mean for actual platform behaviour.

## 2. Model Locations

* **Preserved Mesa Example:** Used the **Civil Violence** model as the provisional Mesa analogy. The complete, unchanged source code for this example is preserved in `src/civil_violence/`. The `SOURCE.md` file in that folder contains the original URL and attribution.
* **Adapted Project Model:** The targeted slice of the simulation is located in `src/project_model/`. It contains `model.py` (the agent and model logic) and `run.py` (the execution script).

## 3. Software Requirements & Installation

This project requires Python 3.9+ and the following packages (listed in `requirements.txt`):
* `mesa Version 3.3.1`
* `pandas`
* `matplotlib`

**Installation Steps:**
1. Open your terminal and navigate to the root directory of this repository.
2. (Optional but recommended) Create and activate a virtual environment. Do this by navigating to the project root folder, then run python -m venv venv. (Note: If python doesn't work, try python3 -m venv venv)
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt

## 4. How To Run
1. Open a command prompt or terminal and navigate to the main folder of the project (the folder that contains src/, outputs/, and README.md).
2. Install dependencies if you haven't already. Make sure your virtual environment (if used) is activated, then install the required packages by doing: pip install mesa pandas matplotlib.
3. Execute the run script by pointing to its location inside the src folder. From the root directory, run the following command: python src/project_model/run.py

**Verification:**
The terminal should print four confirmation lines:
1. Saved raw data: outputs/baseline_raw_00_visibility_by_round.csv
2. Saved processed graph: outputs/baseline_processed_00_visibility_by_round.png
3. Saved raw data: outputs/alternative_raw_00_visibility_by_round.csv
4. Saved processed graph: outputs/alternative_processed_00_visibility_by_round.png