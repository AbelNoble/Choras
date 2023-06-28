import os
import scrapy
from scrapy.shell import inspect_response

class CourseListSpiderSpider(scrapy.Spider):
    name = "course_list_spider"
    allowed_domains = ["ro.umich.edu"]
    start_urls = ["https://ro.umich.edu/calendars/schedule-of-classes"]

    # Maybe later on have a list of schools and then call this scraper for each school
    # prior to the start of each semester
    school = 'university_of_michigan'

    def parse(self, response):
        # Extract the parent tag name (e.g., Fall 2023)
        semester = response.xpath('//*[@id="block-ro-content"]/article/div/div/ul[1]/li/text()[1]').get()

        # Extract the link to the CSV file
        csv_data = response.xpath('//*[@id="block-ro-content"]/article/div/div/ul[1]/li/a[4]/@href').get()

        if semester and csv_data:
            # Create a filename based on the parent tag
            filename = f'{semester.lower().replace(" ", "").replace(":", "")}.csv'
            
            # Specify the custom directory path
            custom_directory = '../../../../database/' + self.school + '/'

            # Save the CSV file in the custom directory
            file_path = os.path.join(custom_directory, filename)
            yield response.follow(csv_data, self.save_csv, meta={'file_path': file_path})

    def save_csv(self, response):
        # Get the file path from the meta information
        file_path = response.meta['file_path']

        # Save the CSV file in the custom directory
        with open(file_path, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {file_path}')
