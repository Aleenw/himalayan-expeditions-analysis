# Himalayan Mountaineering Expeditions (2020–2024)

Exploratory data analysis and an interactive Streamlit dashboard on 882 Himalayan climbing expeditions, to find what makes an expedition succeed

## Dataset
- **Title:** The History of Himalayan Mountaineering Expeditions
- **Source:** (https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-01-21)
- **Original data:** [The Himalayan Database](https://www.himalayandatabase.com)
- **Years:** 2020–2024
- **Files:** `exped_tidy.csv` (882 expeditions, 69 columns) and `peaks_tidy.csv` (480 mountains, 29 columns)

## Problem Definition

### What is the dataset about?
The dataset contains records of mountaineering expeditions in the Nepal Himalaya, including Mount Everest. Each expedition has its season, team size, climbing company, hired guides, oxygen use, result and deaths. A second file describes each mountain, such as its name and height.

About 3 in 10 expeditions fail, and some end in deaths.
This project finds what makes the difference between a successful, safe expedition and a failed or dangerous one.

### Main questions
1. Does using oxygen increase the chance of success?
2. Are bigger teams more successful than smaller teams?
3. Do hired guides (Sherpas) help expeditions succeed?
4. Which season is the best for climbing, and which is the most dangerous?
5. Are higher mountains harder and more dangerous to climb?
6. Which climbing companies have the best results?
7. What are the main reasons expeditions fail?

### Expected insights
Oxygen use, team size and the number of guides are expected to be strongly related to success. Weather is expected to be the main reason for failure, and higher mountains are expected to have more deaths.

## Target Audience
Climbers who are planning a Himalayan expedition. The dashboard helps them decide which mountain, season and company to choose, how big their team should be, how many guides to hire and whether to use oxygen, based on the results of past expeditions.

## Project Structure
├── data/ raw data files
├── notebook/ EDA notebook
└── README.md