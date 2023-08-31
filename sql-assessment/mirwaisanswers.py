import sqlite3
import csv
from collections import defaultdict
from datetime import datetime

# Function to import csv into SQLite table
def import_csv_to_sqlite(cursor, csv_path, table_name):
    with open(csv_path, 'r') as f:
        column_names = f.readline().strip().split(",")
        cursor.execute(f"CREATE TABLE {table_name} ({', '.join(column_names)});")
        for line in f:
            values = line.strip().split(",")
            cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in values])});", values)
    print(f"Imported data into {table_name}")

# Creating SQLite database and cursor
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Importing csv files to SQLite
import_csv_to_sqlite(cursor, '/Users/mirwaisjansalah/Desktop/ProgrammingChallenges/sql-assessment/campaign_info.csv', 'campaign_info')
import_csv_to_sqlite(cursor, '/Users/mirwaisjansalah/Desktop/ProgrammingChallenges/sql-assessment/marketing_performance.csv', 'marketing_data')
import_csv_to_sqlite(cursor, '/Users/mirwaisjansalah/Desktop/ProgrammingChallenges/sql-assessment/website_revenue.csv', 'website_revenue')


# Query 1: Sum of impressions by day
query1 = "select date, SUM(impressions) from marketing_data group by date;"

# Query 2: Top three revenue-generating states
query2 = "select state, SUM(revenue) from website_revenue group by state order by SUM(revenue) DESC limit 3;"

# Query 3: Total cost, impressions, clicks, and revenue of each campaign
query3 = '''
select ci.name, SUM(md.cost) as total_cost, SUM(md.impressions) as total_impressions, 
SUM(md.clicks) as total_clicks, SUM(wr.revenue) as total_revenue
from campaign_info ci
LEFT join marketing_data md on ci.id = md.campaign_id
LEFT join website_revenue wr on ci.id = wr.campaign_id
group by ci.name;
'''

# Query 4: Number of conversions of Campaign5 by state
query4 = '''
select wr.state, SUM(mp.conversions) as total_conversions
from marketing_data mp
join website_revenue wr on mp.date = wr.date and mp.campaign_id = wr.campaign_id
join campaign_info ci on mp.campaign_id = ci.id
where ci.name = 'Campaign5'
group by wr.state
order by total_conversions DESC;
'''

# Query 5: Most efficient campaign based on roas
query5 = '''
select ci.name, SUM(wr.revenue) / SUM(md.cost) as roas 
from campaign_info ci
LEFT join marketing_data md on ci.id = md.campaign_id
LEFT join website_revenue wr on ci.id = wr.campaign_id
group by ci.name
order by roas DESC
limit 1;
'''


# Executing and fetching results
cursor.execute(query1)
result1 = cursor.fetchall()

cursor.execute(query2)
result2 = cursor.fetchall()

cursor.execute(query3)
result3 = cursor.fetchall()

cursor.execute(query4)
result4 = cursor.fetchall()

cursor.execute(query5)
result5 = cursor.fetchall()


# Fetching all data from website_revenue
cursor.execute("select date, revenue from website_revenue;")
data = cursor.fetchall()

# Initializing a dictionary to hold total revenue for each day of the week
revenue_by_day = defaultdict(float)

# Looping through each row to populate the revenue_by_day dictionary
for date_str, revenue in data:
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    day_of_week = date_obj.weekday()
    if revenue is not None:
        revenue_by_day[day_of_week] += float(revenue)

best_day, best_revenue = max(revenue_by_day.items(), key=lambda x: x[1])

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(f"Answer to Bonus Query: Best day is {weekdays[best_day]} with total revenue of {best_revenue}")


conn.close()


print("Answer to Query 1:", result1)
print("Answer to Query 2:", result2)
print("Answer to Query 3:", result3)
print("Answer to Query 4:", result4)
print("Answer to Query 5:", result5)




