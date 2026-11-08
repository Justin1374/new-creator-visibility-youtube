import os
import matplotlib.pyplot as plt
import pandas as pd
from model import RecommendationModel

def run_and_save_condition(weight, condition_name, steps=50):
    # Initialize the model with the given popularity weight
    model = RecommendationModel(weight=weight)
    
    # Run the simulation loop
    for _ in range(steps):
        model.step()
        
    # Extract the collected data
    data = model.datacollector.get_model_vars_dataframe()
    
    # Define the exact output paths pointing to the main outputs/ folder
    csv_filename = f"outputs/{condition_name}_processed_00_visibility_by_round.csv"
    png_filename = f"outputs/{condition_name}_processed_00_visibility_by_round.png"
    
    # Export CSV
    data.to_csv(csv_filename, index_label="Round")
    
    # Generate and export PNG Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Percent_New_Creators_Recommended"], 
             label=f"Popularity Weight: {weight}", color="#1f77b4" if weight == 0.1 else "#d62728")
    
    plt.title(f"{condition_name.capitalize()} Condition: New Creator Visibility Over Time")
    plt.xlabel("Simulation Round")
    plt.ylabel("Percent of New Creators Recommended (%)")
    plt.ylim(0, 100)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    
    plt.savefig(png_filename, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"Successfully generated: {csv_filename}")
    print(f"Successfully generated: {png_filename}")

if __name__ == "__main__":
    # Ensure the outputs directory exists at the root level before saving
    os.makedirs("outputs", exist_ok=True)
    
    print("Running Baseline Condition...")
    run_and_save_condition(weight=0.1, condition_name="baseline")
    
    print("\nRunning Alternative Condition...")
    run_and_save_condition(weight=0.9, condition_name="alternative")
    
    print("\nSimulation complete. Check the 'outputs' folder in your main project directory.")