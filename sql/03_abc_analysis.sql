WITH revenue AS (
    SELECT p.product_name,
           p.category,
           SUM(s.units_sold * p.avg_selling_price * 1.0) AS annual_revenue
    FROM products p
    JOIN monthly_sales s ON p.sku = s.sku
    WHERE s.month >= '2025-10'
    GROUP BY p.sku
),
ranked AS (
    SELECT *,
           SUM(annual_revenue) OVER (ORDER BY annual_revenue DESC)
               / SUM(annual_revenue) OVER () AS cumulative_share
    FROM revenue
)
SELECT product_name,
       category,
       ROUND(annual_revenue / 1000000, 1) AS revenue_millions,
       ROUND(cumulative_share * 100, 1) AS cumulative_pct,
       CASE
           WHEN cumulative_share <= 0.80 THEN 'A'
           WHEN cumulative_share <= 0.95 THEN 'B'
           ELSE 'C'
       END AS abc_class
FROM ranked
ORDER BY annual_revenue DESC;