import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Carica dati ──────────────────────────────────────────────────────────────
df = pd.read_csv("fanta_project - dataset.csv")
df = df.sort_values("giornata")

# Gestisce valori mancanti nei gol
df["goal casa"] = pd.to_numeric(df["goal casa"], errors="coerce")
df["goal ospite"] = pd.to_numeric(df["goal ospite"], errors="coerce")
df = df.dropna(subset=["goal casa", "goal ospite"])

teams = sorted(set(df["squadra casa"]).union(set(df["squadra ospite"])))
giornate = sorted(df["giornata"].unique())

# ── Calcola punti cumulativi per ogni giornata ────────────────────────────────
current_points = {team: 0 for team in teams}
timeline = []  # lista di dict {team: pts} per ogni giornata

for g in giornate:
    matches = df[df["giornata"] == g]
    for _, row in matches.iterrows():
        gc = int(row["goal casa"])
        go = int(row["goal ospite"])
        if gc > go:
            current_points[row["squadra casa"]] += 3
        elif gc < go:
            current_points[row["squadra ospite"]] += 3
        else:
            current_points[row["squadra casa"]] += 1
            current_points[row["squadra ospite"]] += 1
    timeline.append((g, dict(current_points)))

# ── Palette colori ────────────────────────────────────────────────────────────
COLORS = [
    "#F0C040", "#E05A5A", "#5AB4E0", "#60D080",
    "#B060E0", "#E08040", "#40C0B0", "#E060A0",
    "#90C040", "#6080E0"
]
team_colors = {t: COLORS[i % len(COLORS)] for i, t in enumerate(teams)}

# ── Setup figura ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor("#0a0a0f")
ax.set_facecolor("#12121a")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(colors="#555570", labelsize=9)
ax.xaxis.label.set_color("#555570")

n_teams = len(teams)
y_positions = np.arange(n_teams)

def draw_frame(frame_idx):
    ax.clear()
    ax.set_facecolor("#12121a")
    for spine in ax.spines.values():
        spine.set_visible(False)

    giornata, pts = timeline[frame_idx]

    # Ordina per punti (crescente, la prima è quella con più punti in alto)
    sorted_teams = sorted(pts.items(), key=lambda x: x[1])
    max_pts = max(pts.values()) if max(pts.values()) > 0 else 1

    bar_colors = [team_colors[t] for t, _ in sorted_teams]
    values     = [p for _, p in sorted_teams]
    labels     = [t for t, _ in sorted_teams]

    bars = ax.barh(
        range(len(sorted_teams)),
        values,
        color=bar_colors,
        height=0.65,
        zorder=3
    )

    # Griglia verticale sottile
    ax.xaxis.grid(True, color="#1e1e2e", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    # Etichette squadra (sinistra) e punti (destra)
    for i, (bar, (team, p)) in enumerate(zip(bars, sorted_teams)):
        # Nome squadra
        ax.text(-0.5, i, team, va="center", ha="right",
                fontsize=10, fontweight="bold", color="#e8e8f0",
                fontfamily="monospace")
        # Punti
        ax.text(p + max_pts * 0.01, i, str(p), va="center", ha="left",
                fontsize=11, fontweight="bold",
                color=team_colors[team])

    # Highlight 1° posto
    leader_team, leader_pts = sorted_teams[-1]
    bars[-1].set_edgecolor("white")
    bars[-1].set_linewidth(1.5)

    # Titolo e giornata
    ax.set_title(
        "FANTACALCIO TRACKER",
        color="#F0C040", fontsize=18, fontweight="bold",
        fontfamily="monospace", pad=16, loc="left"
    )
    fig.text(0.88, 0.94,
             f"Giornata\n{int(giornata):02d} / {len(giornate):02d}",
             color="#e8e8f0", fontsize=14, fontweight="bold",
             ha="center", va="top", fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#1e1e2e", edgecolor="#F0C040", lw=1.2))

    ax.set_xlim(-18, max_pts * 1.12)
    ax.set_ylim(-0.7, n_teams - 0.3)
    ax.set_yticks([])
    ax.tick_params(axis="x", colors="#555570", labelsize=8)
    ax.set_xlabel("Punti", color="#555570", fontsize=9, labelpad=8)

    fig.tight_layout(rect=[0.18, 0.02, 1, 0.93])

# ── Animazione ────────────────────────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig,
    draw_frame,
    frames=len(timeline),
    interval=900,       # ms tra una giornata e l'altra
    repeat=False
)

# ── Salva come GIF e come MP4 (se ffmpeg disponibile) ────────────────────────
print("Salvataggio GIF in corso...")
ani.save("fantacalcio_tracker.gif", writer="pillow", fps=1, dpi=120)
print("✅ Salvato: fantacalcio_tracker.gif")

try:
    ani.save("fantacalcio_tracker.mp4", writer="ffmpeg", fps=1, dpi=150)
    print("✅ Salvato anche: fantacalcio_tracker.mp4")
except Exception:
    print("ℹ️  ffmpeg non trovato — solo GIF generata")

plt.show()
