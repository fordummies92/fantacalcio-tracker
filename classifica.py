import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("fanta_project - dataset.csv")

teams = set(df["squadra casa"]).union(set(df["squadra ospite"]))
points = {team: [] for team in teams}
current_points = {team: 0 for team in teams}

df = df.sort_values("giornata")

for giornata in sorted(df["giornata"].unique()):
    matches = df[df["giornata"] == giornata]
    
    for _, row in matches.iterrows():
        casa = row["squadra casa"]
        ospite = row["squadra ospite"]
        gol_casa = row["goal casa"]
        gol_ospite = row["goal ospite"]
        
        if gol_casa > gol_ospite:
            current_points[casa] += 3
        elif gol_casa < gol_ospite:
            current_points[ospite] += 3
        else:
            current_points[casa] += 1
            current_points[ospite] += 1
    
    for team in teams:
        points[team].append(current_points[team])

plt.figure()

for team, pts in points.items():
    plt.plot(range(1, len(pts) + 1), pts, label=team)

plt.xlabel("Giornate")
plt.ylabel("Punti")
plt.title("Andamento Classifica Fantacalcio")
plt.legend()
plt.xticks(range(1, len(pts) + 1))
plt.show()