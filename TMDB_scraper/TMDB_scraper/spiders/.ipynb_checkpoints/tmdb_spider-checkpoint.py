# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.http import Request


class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/67915']
    
    # parse() is implemented in no more than 5 lines
    def parse(self, response):
        '''
        Parse the movie page to obtain the link to the Cast & Crew page
        Then navigate to Cast & Crew page
        '''
        #obtain the link to the Cast & Crew page
        cast_link = response.css('p.new_button a::attr(href)').get()
        
        #if the Cast & Crew link exist and is reached
        #call parse_full_credits(self, response) method
        if cast_link:
            cast_link = response.urljoin(cast_link)
            yield scrapy.Request(cast_link, callback = self.parse_full_credits)
    
    # parse_full_credits() is implemented in no more than 5 lines
    def parse_full_credits(self, response):
        '''
        Parse the Cast & Crew page to obtain the links of all actors & actresses
        Then navigate to each page of actors & actresses 
        '''
        #avoid scrapy links of crew members
        selected_class=response.css("ol:not([class='people credits crew'])")
        actor_links = selected_class.css("ol.people.credits div.info a::attr(href)").getall()
        
        #call parse_actor_page(self, response) method when each actor’s page reached
        for link in actor_links:  
            yield scrapy.Request(url = "https://www.themoviedb.org" + link,
                                 callback=self.parse_actor_page)
        
            
    # parse_actor_page() is implemented in no more than 15 lines
    def parse_actor_page(self, response):
        '''
        Parse the Actor page to obatin the actor name and previous works
        Then compute a dictionary with the actor name and the movie name
        '''
        #get the name of the actor or actress 
        actor_name = response.css("h2.title a::text").get()
        
        #get the name of his/her movies
        movie_or_TV_names = response.css("div.credits_list table.card.credits table.credit_group td.role.false.account_adult_false.item_adult_false a.tooltip bdi::text").getall()
        
        #for each movie or show scrapyed, store them into the dictionary
        for movie_or_TV_name in movie_or_TV_names:
            yield{"actor":actor_name,
                  "movie_or_TV_name":movie_or_TV_name}
    