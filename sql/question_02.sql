-- ○ What regions has the "cheap_mobile" datasource appeared in?
SELECT DISTINCT region
FROM trips t
WHERE datasource = 'cheap_mobile'
ORDER BY region
