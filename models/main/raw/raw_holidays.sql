{{
    config(
        materialized='table'
    )
}}

{{ read_holidays_csv() }}
