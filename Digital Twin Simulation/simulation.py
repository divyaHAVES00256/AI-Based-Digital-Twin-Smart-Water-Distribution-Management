import numpy as np


def simulate_step(predicted_demand, tank_level, base_pump, tank_max, leak_probability=0):

    # Adaptive pump control
    if tank_level < 30:
        pump_input = base_pump + 20
    elif tank_level > 80:
        pump_input = base_pump - 10
    else:
        pump_input = base_pump

    # Leak model (extra demand caused by leakage)
    leak_loss = leak_probability * 10

    effective_demand = predicted_demand + leak_loss

    # Tank balance equation
    tank_next = tank_level + pump_input - effective_demand

    # Tank constraints
    tank_next = max(0, min(tank_next, tank_max))

    # Pressure model
    pressure = round(0.4 * tank_next, 2)

    return tank_next, pressure, leak_loss


def run_simulation(
    demands,
    leak_probability=0,
    tank_initial=50,
    pump_input=60,
    tank_max=100,
    scenario="normal"
):

    tank = tank_initial

    tank_levels = []
    pressures = []
    demands_used = []
    leak_losses = []

    for i, demand in enumerate(demands):

        base_pump = pump_input

        # Scenario logic
        if scenario == "high_demand":
            demand = demand * 1.3

        if scenario == "pump_failure":
            base_pump = 20

        if scenario == "demand_spike" and 800 < i < 850:
            demand = demand * 1.8

        tank, pressure, leak_loss = simulate_step(
            predicted_demand=demand,
            tank_level=tank,
            base_pump=base_pump,
            tank_max=tank_max,
            leak_probability=leak_probability
        )
        if tank < 10:
            alert = "Low Tank Level"
        elif leak_probability > 0.6:
            alert = "Possible Leak Detected"
        else:
            alert = None

        tank_levels.append(tank)
        pressures.append(pressure)
        demands_used.append(demand)
        leak_losses.append(leak_loss)

        print(alert) if alert else None

    return {
        "tank_levels": tank_levels,
        "pressures": pressures,
        "demands": demands_used,
        "leak_losses": leak_losses
    }
