# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GlassdoorCompaniesItem(scrapy.Item):
    # define the fields for your item here like:
    # General informations
    S_CName = scrapy.Field()
    S_Industry = scrapy.Field()
    S_Revenue = scrapy.Field()

    # Review
    R_ROverall = scrapy.Field()
    R_RWork_life = scrapy.Field()
    R_RCulture_values = scrapy.Field()
    R_RCareer_opportunities = scrapy.Field()
    R_RCompens_benef = scrapy.Field()
    R_RSenior_manag = scrapy.Field()
    R_Former_Current = scrapy.Field()
    R_Position = scrapy.Field()
    R_Author_Location = scrapy.Field()

    # Benefits
    B_Health_Insurance = scrapy.Field()
    B_Dental_Insurance = scrapy.Field()
    B_Flexible_Spending_Account = scrapy.Field()
    B_Vision_Insurance = scrapy.Field()
    B_Health_Savings_Account = scrapy.Field()
    B_Life_Insurance = scrapy.Field()
    B_Supplemental_Life_Insurance = scrapy.Field()
    B_Disability_Insurance = scrapy.Field()
    B_Occupational_Accident_Insurance = scrapy.Field()
    B_Health_Care_On_Site = scrapy.Field()
    B_Mental_Health_Care = scrapy.Field()
    B_Retiree_Health_Medical = scrapy.Field()
    B_Accidental_Death_Dismemberment_Insurance = scrapy.Field()
    B_Pension_Plan = scrapy.Field()
    ###############################################################
    B_K401_Plan = scrapy.Field()  # Modified 401K_plan to K401_plan
    ###############################################################
    B_Retirement_Plan = scrapy.Field()
    B_Employee_Stock_Purchase_Plan = scrapy.Field()
    B_Performance_Bonus = scrapy.Field()
    B_Stock_Options = scrapy.Field()
    B_Equity_Incentive_Plan = scrapy.Field()
    B_Supplemental_Workers_Compensation = scrapy.Field()
    B_Charitable_Gift_Matching = scrapy.Field()
    B_Maternity_Paternity_Leave = scrapy.Field()
    B_Work_From_Home = scrapy.Field()
    B_Dependent_Care = scrapy.Field()
    B_Reduced_or_Flexible_Hours = scrapy.Field()
    B_Military_Leave = scrapy.Field()
    B_Family_Medical_Leave = scrapy.Field()
    B_Unpaid_Extended_Leave = scrapy.Field()
    B_Vacation_Paid_Time_Off = scrapy.Field()
    B_Sick_Days = scrapy.Field()
    B_Paid_Holidays = scrapy.Field()
    B_Volunteer_Time_Off = scrapy.Field()
    B_Bereavement_Leave = scrapy.Field()
    B_Employee_Discount = scrapy.Field()
    B_Free_Lunch_or_Snacks = scrapy.Field()
    B_Employee_Assistance_Program = scrapy.Field()
    B_Gym_Membership = scrapy.Field()
    B_Commuter_Checks_Assistance = scrapy.Field()
    B_Pet_Friendly_Workplace = scrapy.Field()
    B_Mobile_Phone_Discount = scrapy.Field()
    B_Company_Social_Events = scrapy.Field()
    B_Travel_Concierge = scrapy.Field()
    B_Legal_Assistance = scrapy.Field()
    B_Diversity_Program = scrapy.Field()
    B_Job_Training = scrapy.Field()
    B_Professional_Development = scrapy.Field()
    B_Tuition_Assistance = scrapy.Field()
