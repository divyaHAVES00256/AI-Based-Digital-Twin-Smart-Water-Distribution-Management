import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("digital_twin_output.csv")

plt.figure(figsize=(12, 5))
plt.plot(data["tank_level"])
plt.title("Tank Level")
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(data["pressure"])
plt.title("Pressure")
plt.show()
