import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patheffects as pe
import numpy as np
from IPython.display import HTML, display
from google.colab import files

# ══════════════════════════════════════════════════════════════
#   FANTACALCIO TRACKER — Line Chart Race  (Google Colab)
# ══════════════════════════════════════════════════════════════

# ── 1. Carica CSV ─────────────────────────────────────────────
CSV_PATH = "fanta_project - dataset.csv"

# Opzione upload interattivo (decommenta se preferisci):
# uploaded = files.upload()
# CSV_PATH = list(uploaded.keys())[0]

df = pd.read_csv(CSV_PATH)
df["goal casa"]   = pd.to_numeric(df["goal casa"],   errors="coerce")
df["goal ospite"] = pd.to_numeric(df["goal ospite"], errors="coerce")
df = df.dropna(subset=["goal casa", "goal ospite"]).sort_values("giornata")

print(f"✅ {len(df)} partite · {df['giornata'].nunique()} giornate")

# ── 2. Calcola punti cumulativi ───────────────────────────────
teams    = sorted(set(df["squadra casa"]) | set(df["squadra ospite"]))
giornate = sorted(df["giornata"].unique())

current_pts = {t: 0 for t in teams}
timeline    = []  # [(giornata, {team: pts})]

for g in giornate:
    for _, row in df[df["giornata"] == g].iterrows():
        gc, go = int(row["goal casa"]), int(row["goal ospite"])
        if gc > go:
            current_pts[row["squadra casa"]]  += 3
        elif gc < go:
            current_pts[row["squadra ospite"]] += 3
        else:
            current_pts[row["squadra casa"]]  += 1
            current_pts[row["squadra ospite"]] += 1
    timeline.append((g, dict(current_pts)))

# Matrice punti: rows=giornate, cols=squadre
pts_matrix = np.array([[snap[t] for t in teams] for _, snap in timeline])
n_giornate = len(timeline)
n_teams    = len(teams)

# ── 3. Palette + iniziali ─────────────────────────────────────
PALETTE = [
    "#F0C040","#E05A5A","#5AB4E0","#60D080",
    "#B060E0","#E08040","#40C0B0","#E060A0",
    "#90C040","#6080E0"
]
team_colors = {t: PALETTE[i % len(PALETTE)] for i, t in enumerate(teams)}

def initials(name):
    """Es: 'Te bele vint' → 'TBV'  |  'River Plè' → 'RP'"""
    parts = name.split()
    if len(parts) == 1:
        return name[:3].upper()
    return "".join(p[0] for p in parts).upper()

team_abbr = {t: initials(t) for t in teams}
print("Abbreviazioni squadre:")
for t, a in team_abbr.items():
    print(f"  {a:6s} → {t}")

# ── 4. Setup figura ───────────────────────────────────────────
BG      = "#0a0a0f"
SURFACE = "#12121a"
GRID    = "#1a1a2a"
TEXT    = "#e8e8f0"
MUTED   = "#555570"

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(SURFACE)

for spine in ax.spines.values():
    spine.set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=8)
ax.xaxis.label.set_color(MUTED)
ax.yaxis.label.set_color(MUTED)

# Griglia
ax.set_xlim(1, n_giornate)
ax.set_ylim(-2, pts_matrix.max() + 8)
ax.xaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
ax.set_xticks(range(1, n_giornate + 1))
ax.set_xlabel("Giornata", color=MUTED, fontsize=9, labelpad=8)
ax.set_ylabel("Punti",    color=MUTED, fontsize=9, labelpad=8)

ax.set_title("FANTACALCIO TRACKER", color="#F0C040", fontsize=18,
             fontweight="bold", fontfamily="monospace", pad=16, loc="left")

# Testo giornata corrente
round_text = ax.text(0.98, 0.97, "", transform=ax.transAxes,
                     ha="right", va="top", fontsize=28,
                     fontweight="bold", color=TEXT, fontfamily="monospace",
                     alpha=0.15)  # watermark di sfondo

round_text2 = fig.text(0.91, 0.93, "", ha="center", va="top",
                       fontsize=13, fontweight="bold", color=TEXT,
                       fontfamily="monospace",
                       bbox=dict(boxstyle="round,pad=0.4",
                                 facecolor=SURFACE,
                                 edgecolor="#F0C040", lw=1.2))

# ── 5. Oggetti grafici per ogni squadra ───────────────────────
lines      = {}   # linea principale
dots       = {}   # pallino in cima alla linea
labels     = {}   # etichetta con iniziali

for t in teams:
    c = team_colors[t]

    # Linea
    line, = ax.plot([], [], color=c, linewidth=2.2, zorder=3,
                    solid_capstyle="round")
    line.set_path_effects([
        pe.Stroke(linewidth=4, foreground=BG),   # alone scuro
        pe.Normal()
    ])
    lines[t] = line

    # Pallino animato (fine della linea)
    dot, = ax.plot([], [], "o", color=c, markersize=9, zorder=5,
                   markeredgecolor=BG, markeredgewidth=1.5)
    dots[t] = dot

    # Badge con iniziali
    label = ax.text(0, 0, team_abbr[t],
                    fontsize=7.5, fontweight="bold",
                    color=BG, zorder=6,
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.25",
                              facecolor=c, edgecolor="none",
                              alpha=0.95))
    labels[t] = label

# ── 6. Funzione di aggiornamento ──────────────────────────────
x_all = [g for g, _ in timeline]

def update(frame):
    # frame va da 0 a n_giornate-1
    x_visible = x_all[:frame + 1]

    for i, t in enumerate(teams):
        y_visible = pts_matrix[:frame + 1, i]

        # Aggiorna linea
        lines[t].set_data(x_visible, y_visible)

        # Aggiorna pallino e label sull'ultimo punto
        x_last = x_visible[-1]
        y_last = y_visible[-1]
        dots[t].set_data([x_last], [y_last])
        labels[t].set_position((x_last, y_last + 3.2))

    # Watermark giornata
    g_num = int(x_all[frame])
    round_text.set_text(f"{g_num:02d}")
    round_text2.set_text(f"Giornata\n{g_num:02d} / {n_giornate:02d}")

    # Highlight leader
    leader_idx = np.argmax(pts_matrix[frame])
    for i, t in enumerate(teams):
        alpha = 1.0 if i == leader_idx else 0.55
        lines[t].set_alpha(alpha)
        dots[t].set_alpha(alpha)
        labels[t].set_alpha(alpha)

    return list(lines.values()) + list(dots.values()) + list(labels.values())

# ── 7. Animazione ─────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_giornate,
    interval=800,          # ← ms tra una giornata e l'altra
    blit=True,
    repeat=False
)

plt.tight_layout()
plt.close()

# ── 8. Mostra nel notebook ────────────────────────────────────
print("⏳ Rendering animazione (può richiedere qualche secondo)...")
display(HTML(ani.to_jshtml()))
print("✅ Pronta!")

# ── 9. Salva GIF e scarica ────────────────────────────────────
print("💾 Salvataggio GIF...")
ani.save("fantacalcio_linechart.gif", writer="pillow", fps=1, dpi=110)
files.download("fantacalcio_linechart.gif")
print("✅ fantacalcio_linechart.gif scaricata!")
