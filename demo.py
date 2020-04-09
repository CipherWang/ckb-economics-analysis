#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np 
from matplotlib import pyplot as plt

# data in billion
INITIAL_SUPPLY = 33.6
PRIMARY_SUPPLY_1STYEAR = 33.6 / 4
SECONDARY_SUPPLY_YEARLY = 1.344
HALFING_PERIOD = 4

cut_off_year = 50

x = np.arange(0, cut_off_year)
primary_issuance = PRIMARY_SUPPLY_1STYEAR * np.power(2, -np.floor(x/4))

def _getMonthSupply(t_monthly):
    primary_issuance_monthly = PRIMARY_SUPPLY_1STYEAR * np.power(2, -np.floor(t_monthly/4)) / 12.
    secondary_issuance_monthly = SECONDARY_SUPPLY_YEARLY / 12
    total_supply_monthly = []
    for m in np.arange(0, len(t_monthly)):
        total_supply_monthly.append(INITIAL_SUPPLY + np.sum(primary_issuance_monthly[:m]) + m*secondary_issuance_monthly)
    return (primary_issuance_monthly, secondary_issuance_monthly, np.array(total_supply_monthly))

def Primary_Issuance():
    # 1st issuance
    plt.bar(x, primary_issuance)
    plt.ylim((0, 10))
    plt.xlim(( - 0.5, cut_off_year - 0.5))
    plt.xticks(np.arange(0, cut_off_year, 4))
    plt.xlabel('Time / year')
    plt.ylabel("Supply / GB")
    plt.show()

def Inflation_Rate_Comparison():
    t_monthly = np.arange(0, cut_off_year, 1./12)
    (primary_issuance_monthly, secondary_issuance_monthly, total_supply_monthly) = _getMonthSupply(t_monthly)
    # Baseline of Annual Percentage of Compesation
    APC = SECONDARY_SUPPLY_YEARLY / total_supply_monthly * 100
    #inflation_rate = np.power(1 + (primary_issuance_monthly + secondary_issuance_monthly) / total_supply_monthly, 12) - 1.0
    inflation_rate = (primary_issuance_monthly + secondary_issuance_monthly) / total_supply_monthly * 12
    inflation_rate = inflation_rate * 100
    real_inflation = inflation_rate - APC
    # Nominal Inflation Rate 名义通胀率：当年总增发除以总发行
    plt.plot(t_monthly, inflation_rate, "r-.", linewidth=0.8, label = 'Nominal Inflation Rate')
    # Baseline of APC 基准补偿率：二级增发除以总发行
    plt.plot(t_monthly, APC, "g-.", linewidth=0.8, label = 'Baseline of APC (Compensation in NervosDAO)')
    # Real Inflation Rate 实际通胀率：一级增发除以总发行
    plt.plot(t_monthly, real_inflation, "b", label = 'Real Inflation Rate')
    plt.ylim((0, 35))
    plt.xlim((0, cut_off_year))
    plt.xticks(np.arange(0, cut_off_year, 4))
    plt.legend(loc='upper right')
    plt.xlabel('Time / year')
    plt.ylabel("Interest / %")
    plt.show()

# De Facto Hard Cap 
'''
    等效硬顶曲线:理论总发行量折算到0年的等效值
'''
def deFacto_Hard_Cap():
    t_monthly = np.arange(0, cut_off_year, 1./12)
    (primary_issuance_monthly, secondary_issuance_monthly, total_supply_monthly) = _getMonthSupply(t_monthly)
    monthly_apc = (SECONDARY_SUPPLY_YEARLY/12.0) / total_supply_monthly
    deFactoSupply = []
    accumulated_interest = 1.0
    index = 0
    for supply in total_supply_monthly:
        deFactoSupply.append(supply / accumulated_interest)
        accumulated_interest *= (1 + monthly_apc[index])
        index += 1
    plt.plot(t_monthly, deFactoSupply)
    plt.ylim((32, 100))
    plt.xlim((0, cut_off_year))
    plt.xticks(np.arange(0, cut_off_year, 4))
    plt.xlabel('Time / year')
    plt.ylabel("de Facto Supply / GB")
    plt.show()

if __name__ == "__main__":
    Primary_Issuance()
    Inflation_Rate_Comparison()
    deFacto_Hard_Cap()
