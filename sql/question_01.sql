-- ○ From the two most commonly appearing regions, which is the latest datasource?
SELECT 
    datasource
    ,region
    ,datetime
FROM trips t2
WHERE region in
    (
        SELECT region
     FROM
       (
        SELECT
            region
            ,count(1) AS COUNT
        FROM trips t
        GROUP BY region
        ORDER BY COUNT DESC
        LIMIT 2
        ) t1
    )
ORDER BY datetime DESC
LIMIT 1