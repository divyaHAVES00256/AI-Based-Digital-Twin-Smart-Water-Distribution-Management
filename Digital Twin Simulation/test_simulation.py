import pandas as pd
import matplotlib.pyplot as plt
from simulation import run_simulation


# -------------------------------------------------
# 1. Load ANN Prediction Data
# -------------------------------------------------
def load_predictions(file_path):
    data = pd.read_csv(file_path)
    return data["predicted_demand"].values


# -------------------------------------------------
# 2. Run Simulation
# -------------------------------------------------
def run_tests(demands):

    print("Running simulations...")

    results = {
        "normal": run_simulation(demands, scenario="normal"),
        "high_demand": run_simulation(demands, scenario="high_demand"),
        "pump_failure": run_simulation(demands, scenario="pump_failure"),
        "demand_spike": run_simulation(demands, scenario="demand_spike"),
    }

    print("Simulation completed.\n")

    # Sample output check
    print("Sample Tank Levels:", results["normal"]["tank_levels"][:10])
    print("Sample Pressures:", results["normal"]["pressures"][:10])

    return results


# -------------------------------------------------
# 3. Save Results to CSV
# -------------------------------------------------
def save_results(results, filename):

    df = pd.DataFrame({
        "timestep": range(len(results["tank_levels"])),
        "demand": results["demands"],
        "tank_level": results["tank_levels"],
        "pressure": results["pressures"]
    })

    df.to_csv(filename, index=False)


def export_all(results):

    save_results(results["normal"], "normal_operation.csv")
    save_results(results["high_demand"], "high_demand.csv")
    save_results(results["pump_failure"], "pump_failure.csv")
    save_results(results["demand_spike"], "demand_spike.csv")

    print("Scenario CSV files saved.")


# -------------------------------------------------
# 4. Plot Tank Level Comparison
# -------------------------------------------------
def plot_results(results):

    plt.figure(figsize=(12, 6))

    plt.plot(results["normal"]["tank_levels"], label="Normal")
    plt.plot(results["high_demand"]["tank_levels"], label="High Demand")
    plt.plot(results["pump_failure"]["tank_levels"], label="Pump Failure")

    plt.title("Tank Level Comparison")
    plt.xlabel("Timestep")
    plt.ylabel("Tank Level")

    plt.legend()
    plt.grid(True)
    plt.show()


# -------------------------------------------------
# 5. Main Execution
# -------------------------------------------------
def main():

    demands = load_predictions("test_ann_predictions_2500_rows.csv")

    results = run_tests(demands)

    export_all(results)

    plot_results(results)


if __name__ == "__main__":
    main()
