import scrapy  
from parsel import Selector
from remax_scrapy.items import *
import json
import re

headers = {
		 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
		} 

class RemaxSpider(scrapy.Spider): 
   name = "remax"
   
   
  
  
   def start_requests(self):
      urls = [ 
      'https://www.remax.com/agents-1.xml',
      'https://www.remax.com/agents-2.xml'
      ]
      for url in urls:
         yield scrapy.Request(url=url,
                              headers=headers,
                              callback = self.parse)
   def parse(self, response):
      # print(response.text)
      response=Selector(text=response.text)
      
      links=response.xpath("//loc/text()").extract()
      for link in links:
         yield scrapy.Request(url=link,
                              headers=headers,
                              callback = self.parse_profile)
         
   def parse_profile(self, response):
        languages = []
        office_phone_numbers = []
        agent_phone_numbers = []
        websites = ''
        social = {}
        zipcode = ''
        city = ''    
        state = ''
        country = 'United States'
        title = ''
        address = ''
        
        #XPATH
        SCRIPT_XPATH= "//script[contains(@type,'application/ld+json')]/text()"
        TITLE_XPATH= '//span[@class="capitalize"]/text()'
        DESCRIPTION_XPATH = "//div[@class='col']//p/text()"
        DESCRIPTION_XPATH_2 = "//span[contains(@class,'whitespace')]/text()"
        AGENT_PHONE_XPATH='//a[@class="phone-link"]/text()'
        OFFICE_PHONE_XPATH="//div[@id='__nuxt']/following-sibling::script/text()"
        
        
        #EXTRACT
        script= json.loads(response.xpath(SCRIPT_XPATH).extract_first())
        name = script.get("name",'')
        title = response.xpath(TITLE_XPATH).extract_first()
        image = script.get("image",'')
        office_name = script.get("subOrganization",'')
        agent_phone_numbers = response.xpath(AGENT_PHONE_XPATH).extract()
        office_phone_numbers = response.xpath(OFFICE_PHONE_XPATH).extract_first()
        address = script.get('address', {}).get('streetAddress','N/A')
        city= script.get('address', {}).get('addressLocality','N/A')
        state = script.get('address', {}).get('addressRegion','N/A')
        zipcode = script.get('address', {}).get('postalCode','N/A')
        description = response.xpath(DESCRIPTION_XPATH).extract()
        description_2 = response.xpath(DESCRIPTION_XPATH_2).extract_first()
        language=script.get("knowsLanguage",'')
        email = script.get("email",'')
        websites = script.get('url', '')
        
        #Cleaning
        #office phone number
        office_phone_numbers=[*set(re.findall('phoneNumber.*?\",',office_phone_numbers))]
        office_phone=[]
        for ele in office_phone_numbers:
            ele=ele.split('"')
            for ch in ele:
                if 10<=len(ch)<=16 and bool(re.match('^(?=.*[0-9]$)', ch)):
                    office_phone.append(ch)
        office_phone=[*set(office_phone)]
        
        #agent_phone number
        agent_phone_numbers=[*set(agent_phone_numbers)]
        
        #discription
        desc=[]
        for line in description:
            line=line.replace("\n"," ").replace("''"," ")
            try:
                line=line.split("        ")
                for i in line:
                    desc.append(i.strip(" "))
            except: 
                desc.append(line.strip(" ")) 
        desc=''.join(desc)   
            
        if desc is '':
            desc=description_2.replace("\n","")
            
        #name
        if " " in name:
             name=name.split(" ")
             if len(name)==2:
                first_name = name[0]
                middle_name = ''
                last_name = name[1]
             elif len(name)==3:
                  first_name = name[0]
                  middle_name = name[1]
                  last_name = name[2]
             else:
                 name=''.join(name)
                 first_name = name
                 middle_name = ''
                 last_name = ''
        else:
            first_name = name
            middle_name = ''
        
            last_name = ''
        #languages
        if type(language)==str:
            languages.append(language)
        else:
            languages=language
        
        item = RemaxScrapyItem(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            office_name=office_name,
            title=title,
            description=desc,
            languages=languages,
            image_url=image,
            address=address,
            city=city,
            state=state,
            country=country,
            zipcode=zipcode,
            office_phone_numbers=office_phone,
            agent_phone_numbers=agent_phone_numbers,
            email=email,
            website=websites,
            social=social,
            profile_url=response.url,
        )
        
        
        try:
            yield item
        except:
            pass
        
      
