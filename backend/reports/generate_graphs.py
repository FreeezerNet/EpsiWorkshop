import pandas as pd
import matplotlib.pyplot as plt

from database.mysql_client import get_connection

conn = get_connection

df = pd.read_sql(
    "SELECT * FROM measurements",
    conn
)

plt.plot(
    df["timestamp"],
    df["production_watts"]
)

plt.title(
    "Production History"
)

plt.savefig(
    "reports/production_history.png"
)