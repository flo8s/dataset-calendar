{{ config(materialized='view') }}

with date_spine as (
    select unnest(generate_series(DATE '1955-01-01', DATE '2027-12-31', INTERVAL 1 DAY))::DATE as date
),

holidays as (
    select
        date,
        holiday_name
    from {{ ref('raw_holidays') }}
),

joined as (
    select
        d.date,
        h.holiday_name as raw_holiday_name
    from date_spine d
    left join holidays h on d.date = h.date
)

select
    date,

    -- 年月日
    year(date)::INTEGER as year,
    month(date)::INTEGER as month,
    day(date)::INTEGER as day,

    -- 曜日
    isodow(date)::INTEGER as weekday_code,
    case isodow(date)::INTEGER
        when 1 then '月曜日'
        when 2 then '火曜日'
        when 3 then '水曜日'
        when 4 then '木曜日'
        when 5 then '金曜日'
        when 6 then '土曜日'
        when 7 then '日曜日'
    end as weekday,

    -- 祝日・振替休日
    raw_holiday_name is not null and raw_holiday_name != '休日' as is_holiday,
    case when raw_holiday_name is not null and raw_holiday_name != '休日'
        then raw_holiday_name
    end as holiday_name,
    raw_holiday_name = '休日' as is_substitute_holiday,

    -- 曜日フラグ
    isodow(date) = 6 as is_sat,
    isodow(date) = 7 as is_sun,
    isodow(date) >= 6 as is_sat_sun,
    isodow(date) >= 6 or raw_holiday_name is not null as is_sat_sun_holiday,
    isodow(date) < 6 and raw_holiday_name is null as is_weekday,

    -- 会計年度
    (case when month(date) >= 4 then year(date) else year(date) - 1 end)::INTEGER as fiscal_year,
    (case
        when month(date) in (4, 5, 6) then 1
        when month(date) in (7, 8, 9) then 2
        when month(date) in (10, 11, 12) then 3
        else 4
    end)::INTEGER as fiscal_quarter,

    -- 和暦
    case
        when date < DATE '1912-07-30' then '明治'
        when date < DATE '1926-12-25' then '大正'
        when date < DATE '1989-01-08' then '昭和'
        when date < DATE '2019-05-01' then '平成'
        else '令和'
    end as wareki_era,
    (case
        when date < DATE '1912-07-30' then year(date) - 1867
        when date < DATE '1926-12-25' then year(date) - 1911
        when date < DATE '1989-01-08' then year(date) - 1925
        when date < DATE '2019-05-01' then year(date) - 1988
        else year(date) - 2018
    end)::INTEGER as wareki_year,
    case
        when date < DATE '1912-07-30' then '明治' || (year(date) - 1867) || '年'
        when date < DATE '1926-12-25' then '大正' || (year(date) - 1911) || '年'
        when date < DATE '1989-01-08' then '昭和' || (year(date) - 1925) || '年'
        when date < DATE '2019-05-01' then '平成' || (year(date) - 1988) || '年'
        else '令和' || (year(date) - 2018) || '年'
    end as wareki_label

from joined
