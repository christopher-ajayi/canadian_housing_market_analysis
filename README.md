# Canadian Housing Market Analysis

## Project Overview

This project examines the evolution of the Canadian housing market by analyzing the relationship between housing prices, household income, population growth, housing supply, and monetary policy.

The analysis combines national and provincial data to identify major housing-market trends, affordability pressures, changes in housing supply, and the relationship between the Bank of Canada's policy rate and housing-market outcomes.

The main comparative analysis covers **2010–2024**, the common period for which the required housing, income, population, housing-supply, and policy-rate indicators are consistently available. The underlying dataset has broader historical coverage, extending from **1946 to 2026**.

## Dataset

### ETL and Data Preparation

The project follows an **ETL (Extract, Transform, Load)** workflow.

### Data Sources
- **Statistics Canada** — NHPI, population, and income data.
- **Bank of Canada** — Policy interest rate data.

* Data was collected from Canadian housing, income, population, and monetary-policy datasets. 
* Data was cleaned, standardized, validated, merged, and transformed into growth and supply-demand indicators using Python and Pandas.
* The transformed datasets were prepared for analysis, visualization, and the final Power BI dashboard.

The analytical dataset contains **841 observations across 11 regions**:

- Canada
- Newfoundland and Labrador
- Prince Edward Island
- Nova Scotia
- New Brunswick
- Quebec
- Ontario
- Manitoba
- Saskatchewan
- Alberta
- British Columbia

The main variables include:

| Variable | Description |
|---|---|
| `year` | Observation year |
| `region` | Canada or province |
| `nhpi` | National House Price Index |
| `median_after_tax_income` | Median after-tax household income |
| `population` | Population |
| `housing_starts_saar` | Housing starts, seasonally adjusted annual rate |
| `policy_rate` | Annual average policy rate |

Derived measures used in the analysis include:

- `nhpi_growth_pct`
- `income_growth_pct`
- `population_growth_pct`
- `housing_supply_growth_pct`
- `supply_demand_growth_gap_pct`

The original dataset contains historical observations beyond the main study period, but differences in source coverage mean that the **2010–2024 period** is used for the primary cross-indicator analysis.

## Analytical Approach

The project follows a structured analytical process:

1. Data loading and initial exploration
2. Data coverage and regional comparison
3. Housing-price analysis
4. Housing affordability analysis
5. Population and housing-supply analysis
6. Policy-rate analysis
7. Integrated Canadian housing-market analysis
8. Key indicator calculations
9. Regional supply-demand analysis
10. Correlation analysis
11. Final findings and recent-period comparison

## Key Analysis

### Housing Prices

The National House Price Index was analyzed to examine long-term housing-price movements and annual changes.

The main 2010–2024 finding is:

- **NHPI increased by 33.68%**

Annual housing-price growth was particularly strong during the pandemic-era housing boom. Growth reached approximately **10% in 2021** before slowing sharply, reaching approximately **0.1% in 2024**.

The historical NHPI analysis also provides broader context. Across the longer historical series, the strongest annual increase occurred in **1987 at 13.80%**, while the weakest occurred in **1991 at -6.85%**.

## Housing Affordability

Housing-price growth was compared with median after-tax income growth to assess whether household income kept pace with housing prices.

Between 2010 and 2024:

- **NHPI growth: 33.68%**
- **Median after-tax income growth: 11.85%**

Housing prices therefore increased substantially faster than median after-tax income.

The growth comparison is approximately:

- **NHPI growth relative to income growth: 2.84×**

The annual comparison also shows that housing prices and incomes generally moved more closely together before the pandemic. This relationship broke down during the pandemic period as housing-price growth accelerated while income growth weakened.

## Population and Housing Supply

Population growth and housing-supply growth were analyzed at the provincial level and then combined to measure the supply-demand growth gap.

The supply-demand growth gap is defined as:

**Housing-supply growth − population growth**

A positive value means housing supply grew faster than population, while a negative value means population growth exceeded housing-supply growth.

The analysis found substantial volatility in housing-supply growth.

Notable national observations include:

- Housing-supply growth reached approximately **25.6% in 2021**
- It subsequently declined to approximately **-7.9% in 2023**
- Housing-supply growth recovered to approximately **1.1% in 2024**
- Population growth reached approximately **3.0% toward the end of the study period**

The results show that housing supply did not move consistently with population growth. In particular, the sharp decline in housing-supply growth occurred while population growth was reaching historically high levels during the recent period.

## Regional Supply-Demand Analysis

The analysis calculates the average supply-demand growth gap for each province.

Provinces are classified according to whether their average gap is:

- **Positive:** housing-supply growth exceeded population growth
- **Negative:** population growth exceeded housing-supply growth

This regional analysis demonstrates that housing-market conditions varied considerably across provinces rather than following a uniform national pattern.

## Monetary Policy and Housing

The Bank of Canada's policy rate is examined in relation to both housing-price growth and housing-supply growth.

Two correlation analyses were performed:

- **Policy rate vs housing-supply growth: -0.43**
- **Policy rate vs NHPI growth: -0.30**

Both relationships are negative, indicating that higher policy rates were associated with weaker housing-supply growth and weaker annual NHPI growth during the study period.

The relationship was stronger for housing supply than for housing-price growth.

These results represent **correlation rather than causation**. Other factors, including economic conditions, construction costs, household demand, credit conditions, and market expectations, may also affect housing-market outcomes.

## Major Visualizations

The notebook includes the following major visual analyses:

- Canadian NHPI trend[![Canadian NHPI Trend](<graphs/Canadian NHPI trend.png>)](<graphs/Canadian NHPI trend.png>)

- Annual NHPI growth
[![alt text](<graphs/Annual Home Price Growth.png>)](<graphs/Annual Home Price Growth.png>)

- Housing-price growth vs income growth 
[![HPGvI](<graphs/Housing-price growth vs income growth.png>)](<graphs/Housing-price growth vs income growth.png>)

- National Population growth vs housing-supply growth
[![PGvHSG](<graphs/Population growth vs housing-supply growth.png>)](<graphs/Population growth vs housing-supply growth.png>)


- Housing supply growth relative to population growth by province
[![alt text](<graphs/Housing Supply Growth to Population Growth by Province.png>)](<graphs/Housing Supply Growth to Population Growth by Province.png>)

- Policy rate vs housing-supply growth
[![alt text](<graphs/Policy rate vs housing-supply growth.png>)](<graphs/Policy rate vs housing-supply growth.png>)

- Policy rate vs NHPI growth
[![alt text](<graphs/Policy rate vs NHPI growtht.png>)](<graphs/Policy rate vs NHPI growtht.png>)

- Canadian housing-market growth indicators for 2020–2024
[![alt text](<graphs/Canadian housing-market growth indicators for 2020–2024.png>)](<graphs/Canadian housing-market growth indicators for 2020–2024.png>)

The 2020–2024 comparison highlights the divergence between housing-price growth, population growth, and housing-supply growth during the most recent period.

## Main Findings

The analysis identifies several important patterns:

1. **Canadian housing prices increased substantially between 2010 and 2024**, with NHPI rising by approximately 33.68%.

2. **Housing prices grew much faster than median after-tax income**, which increased by approximately 11.85% over the same period.

3. **The affordability gap widened substantially during the pandemic-era housing boom**, when housing-price growth accelerated while income growth weakened.

4. **Housing-supply growth was considerably more volatile than population growth**, with a major expansion in 2021 followed by a contraction in 2023.

5. **Population growth accelerated toward the end of the study period**, increasing the importance of housing-supply capacity.

6. **Housing supply and population growth did not move consistently together across provinces and years**, producing substantial regional differences in the supply-demand growth gap.

7. **Policy rates were negatively correlated with housing-supply growth (-0.43)**.

8. **Policy rates were also negatively correlated with NHPI growth (-0.30)**, although the relationship was weaker than the association with housing supply.

## Interpretation and Limitations

The findings in this project describe **relationships and patterns in the data; they do not establish causation**.

In particular, the negative correlations between the policy rate and housing-market indicators should not be interpreted as evidence that changes in the policy rate alone caused changes in housing prices or housing supply.

Housing-market outcomes are influenced by multiple factors, including economic conditions, household demand, income, construction costs, credit conditions, population changes, housing availability, and market expectations. The observed relationships may therefore reflect the combined influence of several factors.

The correlation analysis measures the **strength and direction of association** between variables during the study period. It does not identify the underlying causal mechanism.

The analysis also has the following limitations:

* The underlying datasets have different historical coverage periods.
* The main integrated analysis therefore focuses on the common **2010–2024** period.
* National averages can mask substantial differences between provinces.
* Some housing-market indicators are measured differently across datasets and therefore require careful interpretation when combined.
* Correlation results should not be interpreted as causal estimates.


## Tools and Technologies

- Python
- Pandas
- Matplotlib
- SQL
- Jupyter Notebook
- VS Code
- Power BI

## Project Outputs

The project consists of:

- **Python analysis notebook** — data preparation, exploratory analysis, calculations, visualizations, correlations, and findings


## Future Improvements
- Indept provincial level analysis
- Power BI: The Power BI dashboard will be developed from the finalized analytical results in the notebook rather than introducing a separate analytical framework.

## Author
Christoher Ajayi
