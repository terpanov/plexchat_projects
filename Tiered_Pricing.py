#TIER PRICING CALCULATOR
import pandas as pd
from gspread_pandas import Spread

pricing = Spread('price', 'Plexchat Pricing')
pricing.open_sheet(0)
price_input = pricing.sheet_to_df(header_rows=1, index=True).apply(pd.to_numeric, errors='ignore')

tier_1_MAU = int(price_input.loc["Tier 1", "MAU"])
tier_2_MAU = int(price_input.loc["Tier 2", "MAU"])
tier_3_MAU = int(price_input.loc["Tier 3", "MAU"])
tier_4_MAU = int(price_input.loc["Tier 4", "MAU"])

tier1_cloud_cost = price_input.loc["Tier 1", "COST_USER"]
tier2_cloud_cost = price_input.loc["Tier 2", "COST_USER"]
tier3_cloud_cost = price_input.loc["Tier 3", "COST_USER"]
tier4_cloud_cost = price_input.loc["Tier 4", "COST_USER"]

estimated_MAU = int(price_input.loc["ESTIMATED MAU", "MAU"])

tiers_MAU = {
    "Tier 1": tier_1_MAU,
    "Tier 2": tier_2_MAU,
    "Tier 3": tier_3_MAU,
    "Tier 4": tier_4_MAU
}

tiers_price_per_user = {
    "Tier 1": price_input.loc["Tier 1", "PRICE_USER"],
    "Tier 2": price_input.loc["Tier 2", "PRICE_USER"],
    "Tier 3": price_input.loc["Tier 3", "PRICE_USER"],
    "Tier 4": price_input.loc["Tier 4", "PRICE_USER"]
}

tiers_cost_total = {
    "Tier 1": tier_1_MAU * tier1_cloud_cost,
    "Tier 2": tier_2_MAU * tier2_cloud_cost,
    "Tier 3": tier_3_MAU * tier3_cloud_cost,
    "Tier 4": tier_4_MAU * tier4_cloud_cost
}

tiers_cost_per_user = {
    "Tier 1": tiers_cost_total["Tier 1"] / tier_1_MAU,
    "Tier 2": tiers_cost_total["Tier 2"] / tier_2_MAU,
    "Tier 3": tiers_cost_total["Tier 3"] / tier_3_MAU,
    "Tier 4": tiers_cost_total["Tier 4"] / tier_4_MAU
}

def variable_price(x):
    price = 0
    for MAU in tiers_MAU.values():
        if 0 < x <= tier_1_MAU:
            price = tiers_price_per_user["Tier 1"]
        elif tier_1_MAU < x <= tier_2_MAU:
            price = tiers_price_per_user["Tier 2"]
        elif tier_2_MAU < x <= tier_3_MAU:
            price = tiers_price_per_user["Tier 3"]
        elif tier_3_MAU < x <= tier_4_MAU:
            price = tiers_price_per_user["Tier 4"]
        elif x <= 0:
            price = "Invalid input"
        else:
            price = "Custom Pricing"
    return price

def variable_cost(x):
    cost = 0
    for MAU in tiers_MAU.values():
        if 0 < x <= tier_1_MAU:
            cost = tier1_cloud_cost * x
        elif tier_1_MAU < x <= tier_2_MAU:
            cost = tier2_cloud_cost * x
        elif tier_2_MAU < x <= tier_3_MAU:
            cost = tier3_cloud_cost * x
        elif tier_3_MAU < x <= tier_4_MAU:
            cost = tier4_cloud_cost * x
        elif x <= 0:
            cost = "Invalid input"
        else:
            cost = "Custom Pricing"
    return cost

def prorated_cost(x):
    cost = 0
    for MAU in tiers_MAU.values():
        if 0 < x <= tier_1_MAU:
            cost = tier1_cloud_cost * x
        elif tier_1_MAU < x <= tier_2_MAU:
            cost = tier1_cloud_cost * tier_1_MAU + (x - tier_1_MAU) * \
                   tier2_cloud_cost
        elif tier_2_MAU < x <= tier_3_MAU:
            cost = tier2_cloud_cost * tier_2_MAU + (x - tier_2_MAU) * \
                   tier3_cloud_cost
        elif tier_3_MAU < x <= tier_4_MAU:
            cost = tier3_cloud_cost * tier_3_MAU + (x - tier_3_MAU) * \
                   tier4_cloud_cost
        elif x <= 0:
            cost = "Invalid input"
        else:
            cost = "Custom Pricing"
    return cost

revenue = {MAU: tiers_MAU[MAU] * tiers_price_per_user[MAU] for MAU in tiers_MAU}
cost = {MAU: tiers_MAU[MAU] * tiers_cost_per_user[MAU] for MAU in tiers_MAU}
profit = {MAU: tiers_MAU[MAU] * tiers_price_per_user[MAU] - tiers_MAU[MAU] * tiers_cost_per_user[MAU]
          for MAU in tiers_MAU}
profit_margin = {MAU: (tiers_MAU[MAU] * tiers_price_per_user[MAU] - tiers_MAU[MAU] * tiers_cost_per_user[MAU]) /
                      (tiers_MAU[MAU] * tiers_price_per_user[MAU]) for MAU in tiers_MAU}

pd.options.display.float_format = '{:,.4f}'.format
results = [tiers_MAU, tiers_price_per_user, tiers_cost_per_user, revenue, cost, profit, profit_margin]

report = pd.DataFrame.from_dict(results)
report.index = ['MAU', 'price per user', 'cost_per_user', 'revenue', 'cost', 'profit', 'profit_margin']

print(report)

MAU_actual = estimated_MAU
revenue_actual = MAU_actual * variable_price(MAU_actual)
variable_cost_actual = variable_cost(MAU_actual)
prorated_cost_actual = prorated_cost(MAU_actual)
variable_profit = revenue_actual - variable_cost_actual
variable_profit_margin = variable_profit / revenue_actual
prorated_profit = revenue_actual - prorated_cost_actual
prorated_profit_margin = prorated_profit / revenue_actual

results_actual = [MAU_actual, revenue_actual, variable_cost_actual, prorated_cost_actual, variable_profit,
                  variable_profit_margin, prorated_profit, prorated_profit_margin]

pd.options.display.float_format = '{:,.4f}'.format
report_actual = pd.DataFrame(results_actual)
report_actual.index = ['MAU_actual', 'revenue_actual', 'variable_cost_actual', 'prorated_cost_actual',
                       'variable_profit', 'variable_profit_margin', 'prorated_profit', 'prorated_profit_margin']

print(report_actual)


