# fantacalcio-tracker
# ⚽ Fantacalcio League Tracker

Project by **Marco Nasuelli**

This project generates a dynamic ranking graph for my 10-team fantasy football league.

The script reads match results from a CSV file and automatically:

* Calculates points (3 win / 1 draw / 0 loss)
* Builds cumulative standings
* Generates a graph showing the evolution of the league table over time

---

## 📂 Project Structure

```
fantacalcio-tracker/
│
├── fanta_project.csv
├── classifica.py
└── README.md
```

---

## 📊 Dataset Format

The CSV file must have the following columns:

```
Giornata,Squadra Casa,Gol Casa,Squadra Ospite,Gol Ospite
```

Example:

```
1,River Ple,2,Pescaramanzia,1
1,SAMBUCA JUNIORS,1,Pro VerCella,1
```

---

## 🚀 How to Run the Project

1. Install dependencies:

```
pip install pandas matplotlib
```

2. Run the script:

```
python classifica.py
```

The program will generate a graph showing the evolution of the league standings.

---

## 🎯 Project Goals

* Practice Python data handling
* Work with CSV files
* Build cumulative calculations
* Generate data visualizations
* Apply programming to a real-life use case

---

## 🔜 Future Improvements

* Export graph as PNG
* Add goal difference tracking
* Build an interactive dashboard
* Automate weekly updates

---

## 👤 Author

Marco Nasuelli
AI & Conversational Tech Professional
LinkedIn: https://www.linkedin.com/in/marconasuelli1992/
