# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
from scrapy.utils.response import open_in_browser
#from DPDeleted.items import DpdeletedItem


#Creates the spider for crawling
class RrcSpider(scrapy.Spider):
    name = 'DP2'


    login_page = 'https://webapps.rrc.state.tx.us/DP/initializePublicQueryAction.do'
    start_urls = ['https://webapps.rrc.state.tx.us/DP/initializePublicQueryAction.do',]

    #Tells the spider to first go to the Query page where we can input search data
    def parse(self, response):
        return Request(url=self.login_page, callback=self.login)

    #At the Query page, we input 02/01/2018 into the Submitted Date Form: Field and click submit
    def login(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formname="PublicQueryForm",  # xpath of form to input data into

            #Below we select the Submitted Date From: text box and entering of date
            #CHANGE THIS DATE TO FIND ALL PERMITS SUBMITTED FROM A DIFFERENT DATE OF YOUR CHOOSING
            formdata={'submitStart': '4/1/2017', 'submitEnd': '5/01/2018', 'dpFilingStatus': 'Z'}, #'submit':'Submit'},
              # the button we "click" to submit the form with the input
            clickdata={'value':'Submit'},
            callback=self.parse2  # the method we execute on the sorted page
        )

    #We now will parse the page and scrape all the information we need before crawling on to the next page
    # We will continue moving through the pages until all pages have been scraped
    def parse2(self, response):

        #open_in_browser(response)                     #Opens browser after date submission to verify
        #print("CHECK")                                 #Just a print check

        #item = DrillingpermitsItem()                    #Calls the items from the items.py to be loaded with data

        #Finds the next button and creates the URL to crawl to the next page
        Next_page = ("https://webapps.rrc.state.tx.us" + str(
            response.xpath('//a[contains(string(), "Next")]/@href').extract())[3:-2])
        print(response.xpath('//a[contains(string(), "Next")]/@href').extract())


        # Determine number of wells on page
        print(response.xpath('//strong/text()')[1].extract())
        wells_on_page_range = response.xpath('//strong/text()')[1].extract()
        wells_on_page_low = int(wells_on_page_range.split("-")[0])
        wells_on_page_high = int(wells_on_page_range.split("-")[1])
        wells_on_page_range = wells_on_page_high - wells_on_page_low
        print(wells_on_page_range + 1)


        #Loops across the up to 10 rows of permits per page
        for i in range(7, 7 + wells_on_page_range + 1):

            print(response.xpath('//td[2]/text()')[i].extract())
            #intro_x = "//tr[" + str(i) + "]"   #First calls the xpath identifier of each row with a permit


            #Extracts each parameter as we loop through the permit rows, storing it in the respective item
            # item['API'] = response.xpath(str(intro_x) + '//a[contains(@title, "Lease detail")]/text()').extract()  # Scrapes the API
            # item['Lease'] = response.xpath(str(intro_x) + '//td[3]/a/text()').extract()  # Scrapes the Lease
            # item['District'] = response.xpath(str(intro_x) + '/td[2]/text()').extract()  # Scrapes the District
            # item['Well_Number'] = response.xpath(str(intro_x) + '/td[4]/text()').extract() #Scrapes the Well Number
            # item['Permitted_Operator'] = response.xpath(str(intro_x) + '/td[5]/text()').extract() #Scrapes the Permitted Operator
            # item['County'] = response.xpath(str(intro_x) + '/td[6]/text()').extract() # Scrapes the County
            # item['Status_Date'] = response.xpath(str(intro_x) + '/td[7]/text()').extract()# Scrapes the Status Date
            # item['Status_Number'] = response.xpath(str(intro_x) + '/td[8]/text()').extract() # Scrapes the Status Number
            # item['Wellbore_Profiles'] = response.xpath(str(intro_x) + '/td[9]/text()').extract() # Scrapes the Wellbore Profiles
            # item['Filing_Purpose'] = response.xpath(str(intro_x) + '/td[10]/text()').extract() # Scrapes the Filing Purpose
            # item['Amend'] = response.xpath(str(intro_x) + '/td[11]/text()').extract() # Scrapes the Amend
            # item['Total_Depth'] = response.xpath(str(intro_x) + '/td[12]/text()').extract() # Scrapes the Total Depth
            # item['Stacked_Lateral_Parent_Well_DP'] = response.xpath(str(intro_x) + '/td[13]/text()').extract() # Scrapes the Stacked Lateral Parent
            # item['Status'] = response.xpath(str(intro_x) + '/td[14]/text()').extract() # Scrapes the Status

            #yield item #updates the items with the new data after each row

        #Uses the next page hyperlink to crawl to and recursively scrape
        if response.xpath('//a[contains(string(), "Next")]/@href').extract() == []:
            print("scraped all pages of wells in set time period")
            yield
            return
        else:
            yield Request(url=Next_page, callback=self.parse2, dont_filter=False)
