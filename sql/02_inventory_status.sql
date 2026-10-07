WITH demand AS (
    SELECT sku, AVG(units_sold) AS avg_monthly_demand
    FROM monthly_sales
    WHERE month >= '2025-10'
    GROUP BY sku
)
SELECT p.product_name,
       ROUND(p.on_hand * 1.0 / d.avg_monthly_demand, 1) AS months_of_supply,
       CASE
           WHEN p.on_hand * 1.0 / d.avg_monthly_demand > 4 THEN 'Overstocked'
           WHEN p.on_hand * 1.0 / d.avg_monthly_demand < 1.5 THEN 'At Risk'
           ELSE 'Healthy'
       END AS status,
       MAX(0, ROUND(p.on_hand - 4 * d.avg_monthly_demand, 0)) AS excess_units,
       MAX(0, ROUND((p.on_hand - 4 * d.avg_monthly_demand) * p.unit_cost, 0)) AS excess_value_usd
FROM products p
JOIN demand d ON p.sku = d.sku
ORDER BY excess_value_usd DESC;