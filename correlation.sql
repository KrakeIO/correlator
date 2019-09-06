CREATE TABLE daily_trades(
  "id" TEXT,
  "company_id" TEXT,
  "low" TEXT,
  "high" TEXT,
  "volume" TEXT,
  "date_published" TEXT,
  "created_at" TEXT,
  "updated_at" TEXT,
  "close" TEXT,
  "large_dip" TEXT
);
CREATE TABLE correlation(
  "company1" TEXT,
  "company2" TEXT,
  "month" TEXT,
  "distance" TEXT
);
CREATE TABLE correlation_weekly(
  "company1" INT,
  "company2" INT,
  "week" TEXT,
  "distance" REAL
);
CREATE TABLE correlation_monthly(
"company1" INT,
  "company2" INT,
  "month" TEXT,
  "distance" REAL
);
CREATE TABLE correlation_quarterly(
"company1" INT,
"company2" INT,
"quarter" TEXT,
"distance" REAL
);

.mode csv

.import /Users/ryanfeatherman/correlator/correlation_weekly.csv correlation_weekly
.import /Users/ryanfeatherman/correlator/correlation_monthly.csv correlation_monthly
.import /Users/ryanfeatherman/correlator/correlation_quarterly.csv correlation_quarterly

SELECT count(*) from correlation_weekly;
SELECT count(*) from correlation_monthly;
SELECT count(*) from correlation_quarterly;

SELECT company1, company2, AVG(distance), MAX(distance) FROM correlation_monthly GROUP BY company1, company2 HAVING AVG(distance) < 0.5 AND MAX(distance) > 1.5;

SELECT * FROM correlation_weekly WHERE company1 = 420 AND company2 = 880;
SELECT * FROM correlation_monthly WHERE company1 = 420 AND company2 = 880;
SELECT * FROM correlation_quarterly WHERE company1 = 420 AND company2 = 880;


