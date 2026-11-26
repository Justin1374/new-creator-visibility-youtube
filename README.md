# DEL03: Final Computational Inquiry

## 1. Project Overview and Reference to DEL03.1

This repository contains the DEL03 computational model examining how changing the popularity weight in YouTube Home-page long-form video recommendations affects new-creator visibility, viewer topic alignment, and realized viewer engagement over repeated recommendation rounds.

The model compares two ranking arrangements using the same synthetic agents and run conditions:

- **Baseline (interest-weighted):** `w_pop = 0.10`, so viewer topic interest contributes 90% of the ranking score and creator popularity contributes 10%.
- **Alternative (popularity-weighted):** `w_pop = 0.90`, so creator popularity contributes 90% of the ranking score and viewer topic interest contributes 10%.

The ranking rule is `S_i(t) = w_pop * p_i(t) + (1 - w_pop) * I_i(t)`. In each of 50 rounds, one viewer is selected, the 100 candidate creators are ranked, and the top 10 recommendations are placed in the simulated Home-page slate. Engagement is probabilistic and depends on whether a recommended creator's topic matches the active viewer's preference. Realized engagement increases creator popularity, while all creators also experience gradual baseline popularity decay.

**DEL03 changes from DEL02:** The model now includes 200 explicit `ViewerAgent` entities distributed across five topics (Tech, Gaming, Education, Lifestyle, and Music); topic-based interest scores and engagement probabilities; popularity gains only when engagement occurs; gradual popularity decay; additional measures for topic match, engagement, and unique creator reach; and reproducible random seeds. The primary comparison uses seed `42`, with an additional 20-seed robustness sweep using seeds `0–19`.

The model is a bounded, synthetic representation of selected Home-page recommendation dynamics. It does not reproduce YouTube's proprietary ranking algorithm or use real YouTube user, creator, clickstream, or watch-time data.

## 2. Repository Contents and Model Locations

- **Preserved Mesa example:** The original, unchanged **Civil Violence** example used as the provisional Mesa analogy is preserved in `src/civil_violence/`. The `SOURCE.md` file in that folder contains the original URL and attribution.
- **DEL03 project model:** The adapted recommendation simulation is located in `src/project_model/`:
  - `model.py` contains the creator and viewer agents, recommendation ranking logic, engagement process, popularity updates, and model data collection.
  - `run.py` executes the baseline and alternative conditions, including the primary seed-42 runs and the 20-seed robustness sweep.
- **Evidence records:** `docs/evidence/` contains project evidence and input records, including the DEL01 formative feedback record (E3) and the synthetic agent population and parameter specification (E6).
- **Ecosystem map:** The DEL03 ecosystem map is stored in `docs/figures/`. It shows the broader YouTube Home-page recommendation arrangement and identifies the bounded computational representation within it.
- **DEL03 outputs:** Running the model generates the following files in `outputs/`:
  - `del03_baseline_raw_visibility_by_round.csv` — round-by-round results for the baseline condition (`w_pop = 0.10`, seed `42`).
  - `del03_alternative_raw_visibility_by_round.csv` — round-by-round results for the alternative condition (`w_pop = 0.90`, seed `42`).
  - `del03_multiseed_summary.csv` — aggregated comparison measures across seeds `0–19` for both conditions.
  - `del03_comparison_visibility_by_round.png` — time-series comparison of new-creator slot share and realized engagement rate across the 50 rounds for seed `42`.
  - `del03_comparison_summary_distribution.png` — comparison of new-creator slot share, viewer topic match rate, and realized viewer engagement rate across the 20 seeds.
- **Preserved DEL02 outputs:** The original DEL02 reference outputs remain unchanged in `outputs/`: `baseline_raw_00_visibility_by_round.csv`, `baseline_processed_00_visibility_by_round.png`, `alternative_raw_00_visibility_by_round.csv`, and `alternative_processed_00_visibility_by_round.png`.

## 3. Software Requirements & Installation

This project requires Python 3.11.9+ and the following packages (listed in `requirements.txt`):
* `mesa Version 3.3.1`
* `pandas`
* `matplotlib`

**Installation Steps:**
1. Open your terminal and navigate to the root directory of this repository.
2. (Optional but recommended) Create and activate a virtual environment. Do this by navigating to the project root folder, then run python -m venv venv. (Note: If python doesn't work, try python3 -m venv venv)
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

## 4. How To Run
1. Open a command prompt or terminal and navigate to the main folder of the project (the folder that contains src/, outputs/, and README.md).
2. Install dependencies if you haven't already. Make sure your virtual environment (if used) is activated, then install the required packages by doing: pip install mesa pandas matplotlib.
3. Execute the run script by pointing to its location inside the src folder. From the root directory, run the following command: python src/project_model/run.py


**Verification:**

After the script finishes, confirm that the following five DEL03 output files have been created in `outputs/`:

1. `outputs/del03_baseline_raw_visibility_by_round.csv`
2. `outputs/del03_alternative_raw_visibility_by_round.csv`
3. `outputs/del03_multiseed_summary.csv`
4. `outputs/del03_comparison_visibility_by_round.png`
5. `outputs/del03_comparison_summary_distribution.png`

No external data files or command-line arguments are required. The script runs the seed-42 baseline and alternative conditions, performs the 20-seed sweep (seeds `0–19`) for both conditions, and writes the five DEL03 output files listed above.