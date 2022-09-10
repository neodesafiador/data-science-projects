from cProfile import label
from tkinter.ttk import Style
from turtle import color
from matplotlib import colors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load Database
epl_df = pd.read_csv('/Users/katsuike/Documents/EPL-data-analysis/EPL_20_21.csv')
# print(epl_df.head())
# print(epl_df.describe())
# print(epl_df.isna().sum())

# Create 2 new columns
epl_df['MinsPerMatch'] = (epl_df['Mins'] / epl_df['Matches']).astype(int)
epl_df['GoalsPerMatch'] = (epl_df['Goals'] / epl_df['Matches']).astype(float)
print(epl_df.head())

# Total Goals
total_goals = epl_df['Goals'].sum()
print(f"\nTotal Goals are {total_goals}.")

# Total Penalty Goals
total_penalty_goals = epl_df['Penalty_Goals'].sum()
print(f"Total Penalty Goals are {total_penalty_goals}.")

# Penalty Attempts
total_penalty_attempts = epl_df['Penalty_Attempted'].sum()
print(f"Total Penalty Attempts are {total_penalty_attempts}.\n")

# 1st chart
# Pie chart for penalties missed vs scored
plt.figure(figsize=(13, 6))
pl_not_scored = epl_df['Penalty_Attempted'].sum() - total_penalty_goals
data = [pl_not_scored, total_penalty_goals]
labels = ['Penalties Missed', 'Penalties Scored']
color = sns.color_palette('Set2')
plt.pie(data, labels=labels, colors=color, autopct='%.0f%%')
plt.show()

# Unique Positions
# print(epl_df['Position'].unique())

# Total FW players
# print(epl_df[epl_df['Position'] == 'FW'])

# Players from different nations
# print(np.size(epl_df['Nationality'].unique()))

# 2nd chart
# # Most players from which countries
nationality = epl_df.groupby('Nationality').size().sort_values(ascending=False)
nationality.head(10).plot(kind='bar', figsize=(12,6), color=sns.color_palette("magma"))
plt.show()

# 3rd chart
# Clubs with Maximum players in their squad
epl_df['Club'].value_counts().nlargest(5).plot(kind='bar', fontsize=6, color=sns.color_palette("viridis"))
plt.show()

# 4th chart
# Clubs with least players in their squad
epl_df['Club'].value_counts().nsmallest(5).plot(kind='bar', fontsize=6, color=sns.color_palette("viridis"))
plt.show()

# 5th chart
# Players based on age group
under20 = epl_df[epl_df['Age'] <= 20]
age20_25 = epl_df[(epl_df['Age'] > 20) & (epl_df['Age'] <= 25)]
age25_30 = epl_df[(epl_df['Age'] > 25) & (epl_df['Age'] <= 30)]
above30 = epl_df[epl_df['Age'] > 30]

x = np.array([under20['Name'].count(), age20_25['Name'].count(), age25_30['Name'].count(), above30['Name'].count()])
mylabels = ["<=20", "20< & <=25", "25< & <=30", "30<"]
plt.title("Total Players with Age Groups", fontsize=16)
plt.pie(x, labels=mylabels, autopct="%.1f%%")
plt.show()

# 6th chart
# Total under-20 players in each club
players_under_20 = epl_df[epl_df['Age'] <= 20]
players_under_20['Club'].value_counts().plot(kind='bar', fontsize=6, color=sns.color_palette("cubehelix"))
plt.show()

# Under-20 players in ManU
print("Under-20 players in ManU\n")
print(players_under_20[players_under_20["Club"] == "Manchester U"])

# 7th chart
# Average age of players in each club
plt.figure(figsize=(12, 6))
sns.boxplot(x='Club', y='Age', data=epl_df)
plt.xticks(fontsize=6, rotation=90)
plt.show()

num_player = epl_df.groupby('Club').size()
data = (epl_df.groupby('Club')['Age'].sum()) / num_player
print("\nAverage Age for each Club")
print(data.sort_values(ascending=False))

# 8th chart
# Total assists from each club
assists_by_clubs = pd.DataFrame(epl_df.groupby('Club', as_index=False)['Assists'].sum())
sns.set_theme(style="whitegrid", color_codes=True)
ax = sns.barplot(x='Club', y='Assists', data=assists_by_clubs.sort_values(by="Assists"), palette='Set2')
ax.set_xlabel("Club", fontsize=16)
ax.set_ylabel("Assists", fontsize=16)
plt.xticks(fontsize=6, rotation=75)
plt.rcParams["figure.figsize"] = (20, 8)
plt.title("Plot of Clubs vs Total Assists", fontsize=20)
plt.show()

# Top 10 Assists
top_10_assists = epl_df[["Name", "Club", "Assists", "Matches"]].nlargest(n=10, columns="Assists")
print("\n")
print(top_10_assists)

# 9th chart
# Total goals from each club
goals_by_clubs = pd.DataFrame(epl_df.groupby('Club', as_index=False)['Goals'].sum())
sns.set_theme(style="whitegrid", color_codes=True)
ax = sns.barplot(x='Club', y='Goals', data=goals_by_clubs.sort_values(by="Goals"), palette='rocket')
ax.set_xlabel("Club", fontsize=16)
ax.set_ylabel("Goals", fontsize=16)
plt.xticks(fontsize=6, rotation=75)
plt.rcParams["figure.figsize"] = (20, 8)
plt.title("Plot of Clubs vs Total Goals", fontsize=20)
plt.show()

# Most goals by players
top_10_goals = epl_df[["Name", "Club", "Goals", "Matches"]].nlargest(n=10, columns="Goals")
print("\n")
print(top_10_goals)

# Goals per match
top_10_goals_per_match = epl_df[["Name", "GoalsPerMatch", "Matches", "Goals"]].nlargest(n=10, columns="GoalsPerMatch")
print("\n")
print(top_10_goals_per_match)

# 10th chart
# Pie chart - Gpals with assist and without assist
plt.figure(figsize=(14, 7))
assists = epl_df["Assists"].sum()
data = [total_goals - assists, assists]
labels = ["Goals without assists", "Goals with assists"]
color = sns.color_palette("Set1")
plt.pie(data, labels=labels, colors=color, autopct="%.0f%%")
plt.show()

# 11th chart
# Top 10 players with most yellow cards
epl_yellow = epl_df.sort_values(by="Yellow_Cards", ascending=False)[:10]
plt.figure(figsize=(20, 6))
plt.title("Players with the most yellow cards")
c = sns.barplot(x=epl_yellow["Name"], y=epl_yellow["Yellow_Cards"], label="Players", color="yellow")
plt.ylabel("Number of Yellow Cards")
c.set_xticklabels(c.get_xticklabels(), fontsize=6, rotation=45)
plt.show()