SELECT p.product_name,
       p.category,
       p.on_hand,
       ROUND(AVG(s.units_sold), 0) AS avg_monthly_demand,
       ROUND(p.on_hand * 1.0 / AVG(s.units_sold), 1) AS months_of_supply
FROM products p
JOIN monthly_sales s ON p.sku = s.sku
WHERE s.month >= '2025-10'
GROUP BY p.sku
ORDER BY months_of_supply DESC;