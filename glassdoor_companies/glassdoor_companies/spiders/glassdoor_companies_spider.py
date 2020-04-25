from scrapy import Spider, Request
from glassdoor_companies.items import GlassdoorCompaniesItem
import math
import numpy as np

class GlassdoorCompanies_Spider(Spider):
    name = 'glassdoor_companies_spider'
    allowed_urls = ['https://www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Reviews/us-reviews-SRCH_IL.0,2_IN1.htm']

    def parse(self, response):
        num_companies = int(response.xpath('//div[@class="pb-lg-xxl pb-std"]//text()').extract()[-2].replace(',',''))
        num_pages = math.ceil(num_companies/10)

        num_pages = 52
        for page in range(51, num_pages+1):
            print('-'*70)
            print(f'Parsing page {page}')
            print('-'*70)
            url = f'https://www.glassdoor.com/Reviews/us-reviews-SRCH_IL.0,2_IN1_IP{page}.htm'

            yield Request(url = url, callback = self.parse_page)

    def parse_page(self, response):
        rows = response.xpath('//div[@class="single-company-result module "]')

        for row in rows:
            url = row.xpath('.//div[@class="col-3 logo-and-ratings-wrap"]//@href').extract_first()
            url = 'https://www.glassdoor.com' + url

            yield Request(url = url, callback = self.parse_summary_page)

    def parse_summary_page(self, response):
        S_CName = response.xpath('//span[@id="DivisionsDropdownComponent"]/text()').extract_first()

        S_Industry = response.xpath('//div[@class="info flexbox row col-hh"]/div[6]//text()').extract()
        if S_Industry and S_Industry[0].lower() == 'industry':
            S_Industry = S_Industry[1]
        else:
            S_Industry = np.nan

        S_Revenue = response.xpath('//div[@class="info flexbox row col-hh"]/div[7]//text()').extract()
        if S_Revenue and S_Revenue[0].lower() == 'revenue':
            S_Revenue = S_Revenue[1]
        else:
            S_Revenue = np.nan

        meta = {
            'S_CName' : S_CName,
            'S_Industry' : S_Industry,
            'S_Revenue' : S_Revenue,
        }

        url = response.xpath('//a[@class="eiCell cell benefits "]/@href').extract_first()
        url = 'https://www.glassdoor.com' + url

        yield Request(url = url, meta = meta, callback = self.parse_benefits_page)

    def parse_benefits_page(self, response):
        path_benefits = response.xpath('//div[@class="module benefitsList"]/div[3]/ul/li')

        meta = response.meta.copy()

        for index in range(len(path_benefits)):
            benef = path_benefits[index].xpath('.//text()').extract()[-1]

            benef = benef.split(' (')[0].replace(' & ', '_').replace(' ','_').replace('-','_').replace('\'', '')
            str_count = path_benefits[index].xpath('.//@title').extract_first().replace(' employees reporting', '')

            if not str_count:
                meta[benef] = np.nan
            elif benef == '401K_Plan':
                meta['B_K401_Plan'] = str_count
            else:
                meta[f'B_{benef}'] = str_count

        url = response.xpath('//a[@class="eiCell cell reviews "]/@href').extract_first()
        url = 'https://www.glassdoor.com' + url

        yield Request(url = url, meta = meta, callback = self.parse_reviews_all_pages)

    def parse_reviews_all_pages(self, response):
        i=10000
        while True:
            i-=1
            try:
                num_pages = math.ceil(int(response.xpath('//div[@class="mt"]//text()')[-2].extract())/10)
            except:
                print(i)
                continue
            break

        num = 50
        index = 0
        while index <= len(range(num_pages)) and index <= num:
            url = response.url[:-4] + f'_P{index+1}.htm'

            meta = response.meta

            print('-'*10 + meta['S_CName'] + '-'*10 + f': page {index+1}')

            index += 1

            yield Request(url = url, meta = meta, callback = self.parse_reviews_page)

    def parse_reviews_page(self, response):
        reviews = response.xpath('//ol[@class=" highlightsActive empReviews emp-reviews-feed pl-0"]/li')

        index = 1
        for review in reviews:
            index+=1
            Date = review.xpath('.//time[@class="date subtle small"]/text()').extract_first()

            i=0
            while True:
                i+=1
                try:
                    all_rating = review.xpath('.//span[@class="gdStars gdRatings sm stars__StarsStyles__gdStars"]//@title').extract()

                    if len(all_rating) == 1:
                        R_ROverall = float(all_rating[0])
                        R_RWork_life = np.nan
                        R_RCulture_values = np.nan
                        R_RCareer_opportunities = np.nan
                        R_RCompens_benef = np.nan
                        R_RSenior_manag = np.nan

                    else:
                        R_ROverall = float(all_rating[0])
                        R_RWork_life = float(all_rating[1])
                        R_RCulture_values = float(all_rating[2])
                        R_RCareer_opportunities = float(all_rating[3])
                        R_RCompens_benef = float(all_rating[4])
                        R_RSenior_manag = float(all_rating[5])

                except:
                    if i == 100:
                        R_ROverall = np.nan
                        R_RWork_life = np.nan
                        R_RCulture_values = np.nan
                        R_RCareer_opportunities = np.nan
                        R_RCompens_benef = np.nan
                        R_RSenior_manag = np.nan
                        break
                    continue
                break

            temp = review.xpath('.//span[@class="authorJobTitle middle reviewer"]/text()').extract_first()

            if not temp:
                R_Former_Current = R_Position = np.nan
            else:
                try:
                    R_Former_Current, R_Position = temp.split(' Employee - ')
                except:
                    R_Former_Current = R_Position = np.nan

            R_Author_Location = review.xpath('.//span[@class="authorLocation"]/text()').extract_first()

            if not R_Author_Location:
                R_Author_Location = np.nan

            item = GlassdoorCompaniesItem()

            item['S_CName'] = response.meta['S_CName']
            item['S_Industry'] = response.meta['S_Industry']
            item['S_Revenue'] = response.meta['S_Revenue']

            item['B_Health_Insurance'] = response.meta['B_Health_Insurance']
            item['B_Dental_Insurance'] = response.meta['B_Dental_Insurance']
            item['B_Flexible_Spending_Account'] = response.meta['B_Flexible_Spending_Account']
            item['B_Vision_Insurance'] = response.meta['B_Vision_Insurance']
            item['B_Health_Savings_Account'] = response.meta['B_Health_Savings_Account']
            item['B_Life_Insurance'] = response.meta['B_Life_Insurance']
            item['B_Supplemental_Life_Insurance'] = response.meta['B_Supplemental_Life_Insurance']
            item['B_Disability_Insurance'] = response.meta['B_Disability_Insurance']
            item['B_Occupational_Accident_Insurance'] = response.meta['B_Occupational_Accident_Insurance']
            item['B_Health_Care_On_Site'] = response.meta['B_Health_Care_On_Site']
            item['B_Mental_Health_Care'] = response.meta['B_Mental_Health_Care']
            item['B_Retiree_Health_Medical'] = response.meta['B_Retiree_Health_Medical']
            item['B_Accidental_Death_Dismemberment_Insurance'] = response.meta['B_Accidental_Death_Dismemberment_Insurance']
            item['B_Pension_Plan'] = response.meta['B_Pension_Plan']
            item['B_K401_Plan'] = response.meta['B_K401_Plan']
            item['B_Retirement_Plan'] = response.meta['B_Retirement_Plan']
            item['B_Employee_Stock_Purchase_Plan'] = response.meta['B_Employee_Stock_Purchase_Plan']
            item['B_Performance_Bonus'] = response.meta['B_Performance_Bonus']
            item['B_Stock_Options'] = response.meta['B_Stock_Options']
            item['B_Equity_Incentive_Plan'] = response.meta['B_Equity_Incentive_Plan']
            item['B_Supplemental_Workers_Compensation'] = response.meta['B_Supplemental_Workers_Compensation']
            item['B_Charitable_Gift_Matching'] = response.meta['B_Charitable_Gift_Matching']
            item['B_Maternity_Paternity_Leave'] = response.meta['B_Maternity_Paternity_Leave']
            item['B_Work_From_Home'] = response.meta['B_Work_From_Home']
            item['B_Dependent_Care'] = response.meta['B_Dependent_Care']
            item['B_Reduced_or_Flexible_Hours'] = response.meta['B_Reduced_or_Flexible_Hours']
            item['B_Military_Leave'] = response.meta['B_Military_Leave']
            item['B_Family_Medical_Leave'] = response.meta['B_Family_Medical_Leave']
            item['B_Unpaid_Extended_Leave'] = response.meta['B_Unpaid_Extended_Leave']
            item['B_Vacation_Paid_Time_Off'] = response.meta['B_Vacation_Paid_Time_Off']
            item['B_Sick_Days'] = response.meta['B_Sick_Days']
            item['B_Paid_Holidays'] = response.meta['B_Paid_Holidays']
            item['B_Volunteer_Time_Off'] = response.meta['B_Volunteer_Time_Off']
            item['B_Bereavement_Leave'] = response.meta['B_Bereavement_Leave']
            item['B_Employee_Discount'] = response.meta['B_Employee_Discount']
            item['B_Free_Lunch_or_Snacks'] = response.meta['B_Free_Lunch_or_Snacks']
            item['B_Employee_Assistance_Program'] = response.meta['B_Employee_Assistance_Program']
            item['B_Gym_Membership'] = response.meta['B_Gym_Membership']
            item['B_Commuter_Checks_Assistance'] = response.meta['B_Commuter_Checks_Assistance']
            item['B_Pet_Friendly_Workplace'] = response.meta['B_Pet_Friendly_Workplace']
            item['B_Mobile_Phone_Discount'] = response.meta['B_Mobile_Phone_Discount']
            item['B_Company_Social_Events'] = response.meta['B_Company_Social_Events']
            item['B_Travel_Concierge'] = response.meta['B_Travel_Concierge']
            item['B_Legal_Assistance'] = response.meta['B_Legal_Assistance']
            item['B_Diversity_Program'] = response.meta['B_Diversity_Program']
            item['B_Job_Training'] = response.meta['B_Job_Training']
            item['B_Professional_Development'] = response.meta['B_Professional_Development']
            item['B_Tuition_Assistance'] = response.meta['B_Tuition_Assistance']

            item['R_ROverall'] = R_ROverall
            item['R_RWork_life'] = R_RWork_life
            item['R_RCulture_values'] = R_RCulture_values
            item['R_RCareer_opportunities'] = R_RCareer_opportunities
            item['R_RCompens_benef'] = R_RCompens_benef
            item['R_RSenior_manag'] = R_RSenior_manag
            item['R_Former_Current'] = R_Former_Current
            item['R_Position'] = R_Position
            item['R_Author_Location'] = R_Author_Location

            yield item
