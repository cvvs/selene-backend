SELECT
    id,
    device_id,
    metric_type,
    insert_ts,
    metric_value
FROM
    metrics.core
WHERE
    device_id = %(device_id)s
