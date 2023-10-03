-- Query 1
select date, sum(impressions) 
from marketing_data
group by date;

-- Query 2
select state, sum(revenue) 
from website_revenue
group by state
order by sum(revenue) desc
limit 3;

-- Query 3
select ci.name, sum(md.cost) as total_cost, sum(md.impressions) as total_impressions, sum(md.clicks) as total_clicks, sum(wr.revenue) as total_revenue
from campaign_info ci
left join marketing_data md on ci.id = md.campaign_id
left join website_revenue wr on ci.id = wr.campaign_id
group by ci.name;

-- Query 4
select wr.state, SUM(mp.conversions) as total_conversions
from marketing_data mp
join website_revenue wr on mp.date = wr.date and mp.campaign_id = wr.campaign_id
join campaign_info ci on mp.campaign_id = ci.id
where ci.name = 'Campaign5'
group by wr.state
order by total_conversions DESC;

-- Query 5
select ci.name, sum(wr.revenue) / sum(md.cost) as roas
from campaign_info ci
left join marketing_data md on ci.id = md.campaign_id
left join website_revenue wr on ci.id = wr.campaign_id
group by ci.name
order by roas desc
limit 1;




-- Query 6
select strftime('%w', datetime(date)) as day_of_week, sum(revenue) as total_revenue
from website_revenue
group by day_of_week
order by total_revenue desc
limit 1;
