#!/usr/bin/env python
# coding: utf-8

# Name:  Anzar Naseer
# ID: 21087748

# The issue of global warming is currently one of the most significant challenges facing humanity. While it is widely known that the increase in atmospheric carbon dioxide due to human activities is likely a contributing factor to global warming, it is important to investigate and analyze the data to gain a better understanding of this phenomenon. To achieve this goal, I will be using the "World Development Indicators" dataset available on the WorldBank website. Specifically, I will be focusing on the "WDIData_T.csv" and "WDICountry.csv" files to analyze CO2 emissions data. Through this analysis, I aim to answer important questions, such as identifying the top 10 countries with the highest CO2 emissions (in kt and metric tons per capita) and examining their emissions trends. Additionally, I will explore the overall emissions trend of all countries and determine which sectors contribute most heavily to emissions. The dataset contains extensive information, comprising 7,678,806 rows of data on 263 countries, with 1,437 different types of development indicators.



"""
Libraries for fundamental scientific computing (NumPy) and data manipulation and analysis (Pandas) Plotting and visualization (Matplotlib)

"""

# Importing necessary libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter, FuncFormatter
from textwrap import wrap
       

# Read in required data
world_data = pd.read_csv('WDIData_T.csv')
supplemental_data = pd.read_csv('WDICountry.csv')

# Remove aggregated data
countries_to_exclude = '|'.join(supplemental_data[supplemental_data['Currency Unit'].isna()]['Country Code'].unique().tolist())
cleaned_data = world_data[~world_data['CountryCode'].str.contains(countries_to_exclude)]


def filter_data(data):
    # Define indicators of interest
    co2_indicator = 'CO2 emissions \(metric'
    co2kt_indicator = 'CO2 emissions \(kt'
    totGHG_indicator = 'Total greenhouse gas emissions \(kt of CO2'
    tot_fuel_indicator = 'CO2 emissions from gaseous fuel consumption|CO2 emissions from liquid fuel consumption|CO2 emissions from solid fuel consumption'
    country_codes = ['USA', 'GBR', 'FRA', 'CHN', 'JPN', 'DEU', 'IND', 'ITA', 'BRA', 'CAN']

    # Filter data based on indicators and country codes
    mask_co2 = data['IndicatorName'].str.contains(co2_indicator) | data['IndicatorName'].str.contains(co2kt_indicator)
    mask_ghg = data['IndicatorName'].str.contains(totGHG_indicator)
    mask_fuel = data['IndicatorName'].str.contains(tot_fuel_indicator)
    mask_country = data['CountryCode'].isin(country_codes)
    mask_year = data['Year'].isin([1960, 1970, 2006, 2011, 2016])
    filtered_data = data[(mask_co2 | mask_ghg | mask_fuel) & mask_country & mask_year]

    return filtered_data

filter_data(cleaned_data)

# Create masks for top ten countries (GDP)
hist_indicator = 'CO2 emissions \(metric'
mask1 = cleaned_data['IndicatorName'].str.contains(hist_indicator) 
co2_stage = cleaned_data[mask1]
co2_stage.head()


def lineplot(data, countrylist, HorizPlots, PlotNo, Xmin, Xmax, Ymin, Ymax, Type):
    
    """
     This function plots CO2 emission data for 10 selected countries using a line plot to display the time series data.
     The function first saves the minimum and maximum values of CO2 emission for each country in order to create a clear
     and easily comparable chart. The resulting plot consists of horizontal subplots, each displaying the CO2 emissions
     for a specific country. The data spans from 1960 to 2020 and was obtained from the World Bank website.
    """
      
    
    plt_vals = []
    ax = plt.subplot(1, HorizPlots, PlotNo)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_yaxis().tick_left()
    
    
    if Type == 0:
        ax.spines["left"].set_visible(False)
        for y in range(5, 30, 5):
            plt.plot(range(1959, 2021), [y] * len(range(1959, 2021)), "--", lw = 1.0, color = "black", alpha = 0.3)
        for i, col in enumerate(countrylist):
            plt_vals = data.loc[data['CountryCode'] == col]
            ax.plot(plt_vals['Year'].values, plt_vals['Value'].values, linewidth = 1.5)
            y_pos = plt_vals['Value'].values[-1] -0.3
            if plt_vals['CountryCode'].iloc[0] == 'USA':
                y_pos += 0.3
            elif plt_vals['CountryCode'].iloc[0] == 'JPN':
                y_pos += 0.3
            elif plt_vals['CountryCode'].iloc[0] == 'DEU':
                y_pos -= 0.3
            elif plt_vals['CountryCode'].iloc[0] == 'BRA':
                y_pos += 0.3
            elif plt_vals['CountryCode'].iloc[0] == 'GBR':
                y_pos += 0.3
            plt.text(2016.5, y_pos, plt_vals['CountryName'].iloc[0], fontsize = 12)
        plt.title('CO2 Emissions (metric tons per capita)')
    
    if Type == 1:
        ax.set_xticks(ticks=[2006, 2011, 2016])
        ax.set_ylabel(data['IndicatorName'].iloc[0],fontsize = 12)
        
        for i, col in enumerate(countrylist):
            plt_vals = data.loc[data['CountryCode'] == col]
            ax.plot(plt_vals['Year'].values, plt_vals['Value'].values, linewidth=1.5, marker ='o')
            y_pos = plt_vals['Value'].values[-1] -0.3
            x_pos = 2016.5
            if plt_vals['CountryCode'].iloc[0] == 'SAU':
                y_pos -=2.0
            elif plt_vals['CountryCode'].iloc[0] == 'TTO':
                y_pos -=1.0
            elif plt_vals['CountryCode'].iloc[0] == 'BHR':
                y_pos -=1.0
            elif plt_vals['CountryCode'].iloc[0] == 'ARE':
                y_pos +=1.0
            elif plt_vals['CountryCode'].iloc[0] == 'BRN':
                y_pos -=1.0
            elif plt_vals['CountryCode'].iloc[0] == 'GIB':
                x_pos +=4.5
                y_pos +=0.3
            plt.text(x_pos, y_pos, plt_vals['CountryName'].iloc[0], fontsize = 12)
    
    if Type == 2:
        ax.set_yscale('log')
        ax.set_yticks(ticks=[1e3,1e5,1e7])
        ax.set_xticks(ticks=[2006,2011,2016])
        ax.set_ylabel(data['IndicatorName'].iloc[0],fontsize = 12)
        ax.yaxis.set_major_formatter(formatterK)
        
        for i, col in enumerate(countrylist):
            plt_vals = data.loc[data['CountryCode'] == col]
            ax.plot(plt_vals['Year'].values, plt_vals['Value'].values, lw = 1.5, marker = 'o')
            y_pos = plt_vals['Value'].values[-1]
            if plt_vals['CountryCode'].iloc[0] == 'IDN':
                y_pos *=0.78
            elif plt_vals['CountryCode'].iloc[0] == 'SAU':
                y_pos *=0.90
            elif plt_vals['CountryCode'].iloc[0] == 'KOR':
                y_pos *=0.93
            elif plt_vals['CountryCode'].iloc[0] == 'DEU':
                y_pos *=1.05
            plt.text(2016.5, y_pos, plt_vals['CountryName'].iloc[0], fontsize = 12)
    
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.axis([Xmin, Xmax, Ymin, Ymax])


#Plot 1: CO2 Emissions by Country
stage1co = data[mask1 & mask2]

countrylist = hist_country.split('|')
plt.figure(figsize = (10,7))
lineplot(stage1co, countrylist, 1, 1, 1960, 2020, 0, 25, 0)
plt.show()


# ## Analysis: 
# - A line plot of World CO2 Emissions (metric tons per capita) from 1960 to 2020 was plotted, with values on the y-axis.
# - The USA had the highest values, followed by Canada, while Japan only had data from 1990 onwards.
# - The plot provides insights into the trends of CO2 emissions over time and the disparities among countries.
# 


countrylist = T10_country.split('|')
plt.figure(figsize = (5,7))
lineplot(stage2co, countrylist, 1, 1, 2005.5, 2017, 0, 70, 1)
plt.show()


plt.figure(figsize = (5,7))
countrylist = T10kt_country.split('|')
lineplot(stage2cokt,countrylist, 1, 1, 2005.5, 2017, 1e5, 1.3e7, 2)
plt.show()



# Setup masks for data
totFuel_ind = data['IndicatorName'].str.contains('of total fuel combustion')
yearMask = data['Year'] == 2014
TotFuelC = data[yearMask & totFuel_ind]

# Manipulate Data For Next Set Of Graphs
mElecHeat = 'CO2 emissions from electricity and heat production'
mManfIndsConst = 'CO2 emissions from manufacturing industries and construction'
mOtherSec = 'CO2 emissions from other sectors, excluding residential buildings and commercial and public services'
mResid = 'CO2 emissions from residential buildings and commercial and public services'
mTrans = 'CO2 emissions from transport'
T10kt_mask = TotFuelC['CountryCode'].str.contains(T10kt_country)
mEHVal = TotFuelC['Value'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mElecHeat)]
mMICVal = TotFuelC['Value'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mManfIndsConst)]
mOtherVal = TotFuelC['Value'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mOtherSec)]
mResidVal = TotFuelC['Value'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mResid)]
mTransVal = TotFuelC['Value'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mTrans)]
mEHCountry = TotFuelC['CountryName'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mElecHeat)]
mMICCountry = TotFuelC['CountryName'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mManfIndsConst)]
mOSCountry = TotFuelC['CountryName'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mOtherSec)]
mRCountry = TotFuelC['CountryName'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mResid)]
mTransCountry = TotFuelC['CountryName'][T10kt_mask & TotFuelC['IndicatorName'].str.contains(mTrans)]

def hBar(Val,Country,PlotNo,Title):
    '''
    Here a HBar function for the purpose of Horizontal Bar Chart.
     horizontal bar chart is a graph in the form of rectangular bars.
     It's a data visualization technique. The length of these bars is proportional to the values they represent.
     The bar chart title indicates which data is represented.
    '''
    
    X = [x for x, _ in enumerate(Val)]
    Y = np.array(Val)
    ax = plt.subplot(1, 5, PlotNo) 
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)
    for i, col in enumerate(Country):
        ax.text(29, i-0.1, str(int(round(Val.values[i])))+'%', fontsize=12)
    ax.barh(X,Y)
    plt.title(("\n".join(wrap(Title, 15))))
    if PlotNo == 1:
        plt.yticks(X, Country, wrap = True, fontsize = 12)
    else:
        plt.yticks([])
    plt.xticks(fontsize = 12)
    plt.xlim(0, 60)


plt.figure(figsize = (10,7))
hBar(mEHVal, mEHCountry, 5,'Electricity and Heat production')
hBar(mTransVal, mEHCountry, 4, 'Transport')
hBar(mMICVal, mEHCountry, 3, 'Manufacturing Industries and Construction')
hBar(mResidVal, mEHCountry, 2, 'Residential Buildings and Commercial and Public Services')
hBar(mOtherVal, mEHCountry, 1, 'Other sectors, excluding Residential Buildings and Commercial and Public Services')
plt.show()

# On average, the top ten CO2 emitters (kt) attribute 70.93% of their emissions to transportation, electricity, and heat production.
#  However, emission patterns can vary significantly across different sectors for each country, depending on their respective economies.

"""
Summary
Upon analyzing the available data, it was discovered that a considerable number of countries, ranging from 70% to 80%, experienced a rise in their CO2 emissions (metric tons per capita or absolute CO2 emissions (kt)) during the periods of 2006-2016 or 1970-2016. While the rate of change observed between 2006 and 2016 was less than that of 1970-2016, the upward trend continues.
When gauging relative improvements among different countries with varied population sizes, CO2 emissions (metric ton per capita) serves as a good metric. However, when determining the countries with the greatest global emissions impact, the most critical metric is absolute CO2 emissions (kt).
Furthermore, the analysis revealed that transportation, electricity, and heat production constitute an average of 70.93% of the emissions among the top ten CO2 emitters. However, variations in emissions per sector are evident across different countries, dependent on their respective economic structures. If renewable energy sources and electric vehicles are adopted more widely, there could be significant reductions in emissions. Overall, the findings suggest that urgent action is needed to address the rising trend of CO2 emissions and mitigate the effects of climate change.

"""
