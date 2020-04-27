#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np 
from matplotlib import pyplot as plt

# data in billion
INITIAL_SUPPLY = 33.6 * (1 - 0.25)  # burn 25%
PRIMARY_SUPPLY_1STYEAR = 33.6 / 8
SECONDARY_SUPPLY_YEARLY = 1.344
HALFING_PERIOD = 4

cut_off_year = 30

x = np.arange(0, cut_off_year)
primary_issuance = PRIMARY_SUPPLY_1STYEAR * np.power(2, -np.floor(x/4))

def _getMonthSupply(t_monthly, ssy = SECONDARY_SUPPLY_YEARLY):
    primary_issuance_monthly = PRIMARY_SUPPLY_1STYEAR * np.power(2, -np.floor(t_monthly/4)) / 12.
    secondary_issuance_monthly = ssy / 12
    total_supply_monthly = []
    for m in np.arange(0, len(t_monthly)):
        total_supply_monthly.append(INITIAL_SUPPLY + np.sum(primary_issuance_monthly[:m]) + m*secondary_issuance_monthly)
    return (primary_issuance_monthly, secondary_issuance_monthly, np.array(total_supply_monthly))

def Primary_Issuance():
    # 1st issuance
    plt.bar(x, primary_issuance)
    plt.ylim((0, 5))
    plt.xlim(( - 0.5, cut_off_year - 0.5))
    plt.xticks(np.arange(0, cut_off_year, 4))
    plt.xlabel('Time / year')
    plt.ylabel("Supply / GB")
    plt.show()

def Inflation_Rate_Comparison(draw = True):
    t_monthly = np.arange(0, cut_off_year, 1./12)
    (primary_issuance_monthly, secondary_issuance_monthly, total_supply_monthly) = _getMonthSupply(t_monthly)
    # Baseline of Annual Percentage of Compesation
    APC = SECONDARY_SUPPLY_YEARLY / total_supply_monthly * 100
    #inflation_rate = np.power(1 + (primary_issuance_monthly + secondary_issuance_monthly) / total_supply_monthly, 12) - 1.0
    inflation_rate = (primary_issuance_monthly + secondary_issuance_monthly) / total_supply_monthly * 12
    inflation_rate = inflation_rate * 100
    real_inflation = inflation_rate - APC
    if draw:
        # Nominal Inflation Rate 名义通胀率：当年总增发除以总发行
        plt.plot(t_monthly, inflation_rate, "r-.", linewidth=0.8, label = 'Nominal Inflation Rate')
        # Baseline of APC 基准补偿率：二级增发除以总发行
        plt.plot(t_monthly, APC, "g-.", linewidth=0.8, label = 'Nominal Compensation Rate')
        # Real Inflation Rate 实际通胀率：一级增发除以总发行
        plt.plot(t_monthly, real_inflation, "b", label = 'Real Inflation Rate')
        plt.ylim((0, 25))
        plt.xlim((0, cut_off_year))
        plt.xticks(np.arange(0, cut_off_year, 4))
        plt.legend(loc='upper right')
        plt.xlabel('Time / year')
        plt.ylabel("Interest / %")
        plt.show()
    return (inflation_rate, APC, real_inflation)

# De Facto Hard Cap 
'''
    等效硬顶曲线:理论总发行量折算到创世块的等效值
'''
def deFacto_Hard_Cap(draw = True):
    primary_hard_cap = INITIAL_SUPPLY + PRIMARY_SUPPLY_1STYEAR*4*2
    t_monthly = np.arange(0, cut_off_year, 1./12)
    if draw:
        plt.plot((t_monthly[0], t_monthly[-1]), (primary_hard_cap, primary_hard_cap), 
            color='gray', ls = "-." , lw=0.8, label = "Primary issuance hard cap")
    deFactoSupply_array = []
    for ssy_rate in (0, 0.25, 0.5, 1):
        ssy = SECONDARY_SUPPLY_YEARLY * ssy_rate
        (primary_issuance_monthly, secondary_issuance_monthly, total_supply_monthly) = _getMonthSupply(t_monthly, ssy)
        monthly_apc = (ssy/12.0) / total_supply_monthly
        pSupply = []
        deFactoSupply = []
        accumulated_interest = 1.0
        index = 0
        for supply in total_supply_monthly:
            deFactoSupply.append(supply / accumulated_interest)
            accumulated_interest *= (1 + monthly_apc[index])
            index += 1
        deFactoSupply_array.append(deFactoSupply)
        if draw:
            plt.plot(t_monthly, deFactoSupply, label = "Secondary issuance burn %d%%" % int(100 * (1.-ssy_rate)))
    if draw:
        plt.legend(loc='lower right')
        plt.ylim(25, 60)
        plt.xlim((0, cut_off_year))
        plt.xticks(np.arange(0, cut_off_year, 4))
        plt.xlabel('Time / year')
        plt.ylabel("de Facto Supply / GB")
        plt.show()
    return deFactoSupply_array

'''
    和比特币的对比
'''
def VS_BTC():
    # bitcoin calculation
    btc_yearly = 0.5 / 4 * 100
    t_monthly = np.arange(0, cut_off_year, 1./12)
    btc_monthly = btc_yearly * np.power(2, -np.floor(t_monthly/4)) / 12.
    btc_accumulation = []
    for index in range(len(btc_monthly)):
        btc_accumulation.append(np.sum(btc_monthly[:index]))
    btc_accumulation = np.array(btc_accumulation)
    inflation = btc_monthly / btc_accumulation * 100 * 12
    inflation[0] = 10000

    # ckb calculation
    deFacto_supply = deFacto_Hard_Cap(False)[3]
    deFacto_supply = deFacto_supply / np.max(deFacto_supply) * 100
    real_inflation = Inflation_Rate_Comparison(False)[2]


    plt.plot(t_monthly, inflation, '-.', label = "Bitcoin inflation rate")
    plt.plot(t_monthly, btc_accumulation, '-.', label = "Bitcoin issuance")
    plt.plot(t_monthly, real_inflation, label = "CKB deFacto inflation rate (no treasury burn)")
    plt.plot(t_monthly, deFacto_supply, label = "CKB deFacto issuance")
    plt.ylim(0, 100)
    plt.xlim(0, cut_off_year)
    plt.xticks(np.arange(0, cut_off_year, 4))
    plt.yticks(np.arange(0, 110, 10), [str(i) + "%" for i in np.arange(0, 110, 10)])
    plt.legend(loc='center right')
    plt.xlabel('Time / year')
    plt.ylabel("Inflaction rate or Issuance percentage")
    plt.show()

if __name__ == "__main__":
    Primary_Issuance()
    Inflation_Rate_Comparison()
    deFacto_Hard_Cap()
    VS_BTC()
