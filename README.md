## データ出典

[内閣府](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)が公開している「国民の祝日」データと、
DuckDB の generate_series で生成した日付スパイン（1955年〜2027年）を組み合わせた日本の暦データです。

## テーブル: mart_calendar

日付を主キーとする暦データです。1955-01-01 から 2027-12-31 まで、全26,663日分のレコードを含みます。

- date: 日付 (主キー)
- year / month / day: 年月日
- weekday_code / weekday: 曜日コード (ISO 8601) / 曜日名
- is_holiday / holiday_name: 祝日フラグ / 祝日名
- is_substitute_holiday: 振替休日フラグ
- is_sat / is_sun / is_sat_sun: 土曜 / 日曜 / 土日フラグ
- is_sat_sun_holiday / is_weekday: 土日祝フラグ / 平日フラグ
- fiscal_year / fiscal_quarter: 会計年度 / 会計四半期
- wareki_era / wareki_year / wareki_label: 和暦元号 / 和暦年 / 和暦ラベル

## ライセンス

祝日データ: [内閣府「国民の祝日」](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) (CC-BY、出典: 内閣府)
