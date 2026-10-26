# Himalayan Mountaineering Expeditions (2020–2024)

Exploratory data analysis and an interactive Streamlit dashboard on 868 Himalayan climbing expeditions, to find what helps an expedition reach the summit safely.

## Dataset
- **Title:** The History of Himalayan Mountaineering Expeditions
- **Source:** [TidyTuesday, 2025-01-21](https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-01-21)
- **Years:** 2020–2024
- **Files:** `exped_tidy.csv` (882 expeditions, 69 columns) and `peaks_tidy.csv` (480 mountains, 29 columns)
- **After cleaning:** 868 expeditions and 16 columns (`app/clean_data.csv`)

## Problem
About 3 in 10 Himalayan expeditions don't reach the summit, and some end with deaths. This project looks at what makes the difference between a successful, safe expedition and a failed or dangerous one.

### Main questions
1. Does using oxygen increase the chance of success?
2. Are bigger teams more successful than smaller teams?
3. Do hired guides (Sherpas) help expeditions succeed?
4. Which season is the best for climbing, and which is the most dangerous?
5. Are higher mountains harder and more dangerous to climb?
6. Which climbing companies have the best results?
7. What are the main reasons expeditions fail?

## Target Audience
Climbers who are planning a Himalayan expedition. The dashboard helps them choose the mountain and season, decide on the team size, the number of guides and oxygen, and check their own plan against past expeditions.

## Key Insights
- **Oxygen is the biggest factor:** 89% of expeditions with oxygen succeeded vs 55% without. Above 8000m it is 89% vs only 14%.
- **Spring is the best season (76%)**, but also the most dangerous, because most spring expeditions are on 8000m mountains.
- **8000m mountains are much more dangerous:** 34 of the 37 expeditions with a death were above 8000m.
- **Hired staff help:** 76% success with staff vs 43% without.
- **The biggest company is not the best:** Seven Summit Treks has the most expeditions but came 9th in success rate.
- **Nature stops most failed expeditions:** about half failed because of bad weather or bad conditions.


## Project Structure
```
├── Data/                        raw data files
├── notebook/
│   └── himalayan_eda.ipynb      data cleaning, EDA, model and insights
├── app/
│   ├── app.py                   Streamlit dashboard
│   ├── style.py                 dashboard design (colors, cards, banner)
│   ├── clean_data.csv           cleaned data
│   └── .streamlit/config.toml   dashboard theme
└── README.md
```
