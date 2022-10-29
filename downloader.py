import requests
from bs4 import BeautifulSoup
import re

class Download:

    """Download a web page using different methods."""

    def __init__(self, url=None):
        #convert course code to url
        self.course_code = None

        p = re.compile(r'[A-Z]{4}-[0-9]{3}')
        m = p.search(url)
        if m and len(url) == 8:
            self.course_code = url
            self.url = 'https://www.mcgill.ca/study/2022-2023/courses/' + url
        else:
            self.url = url
        

    def request(self, method='GET'):
        """
        return true if the request was successful, false otherwise.
        save content as BeautifulSoup object if successful.
        method can be either GET, POST, OPTIONS, HEAD, PUT, DELETE or PATCH.
        """

        result = requests.request(method, self.url)
        if result.status_code == 200:
            self.get_soup(result.content)
            return True
        else:
            return False

    def get_soup(self, content=None, filename=None):
        """get a BeautifulSoup object from the given content, or filename if
        the latter is specified.
        """
            
        if filename is not None:
            with open(filename, 'r') as fp:
                file = fp.read()
                self.content = BeautifulSoup(file, 'html.parser')
        elif content is not None:
            self.content = BeautifulSoup(content, 'html.parser')

    def save_soup(self, filename):
        """Save soup as a HTML document
        automatically add html extension if not exist
        Automatically save the document as course_code if given.
        """
        if self.course_code:
            filename = self.course_code
        with open(filename + '.html', 'w') as fp:
            print(self.content.prettify(), file=fp)

    def get_courses_from_program_page(self):
        """
        Get all courses code from soup. Course code should look like this:
        MATH 222
        COMP 551
        ECSE 539
        """
        if '/mathstat/undergraduate/programs' in self.url:
            course_numbers = self.content.find_all('span', {'class': 'course_number'})
            return [course_number.text.strip().replace(' ', '-')
                    for course_number in course_numbers]
        else:
            course_numbers = self.content.find_all('a',
                                                   {'class': 'program-course-title'})
            
            codes = []
            p = re.compile(r'[A-Z]{4} [0-9]{3}')
            for course_number in course_numbers:
                m = p.search(course_number.text)
                if m.group():
                    codes.append(m.group().replace(' ', '-'))
            return codes
    

if __name__ == '__main__':
    
    url_math = 'https://www.mcgill.ca/mathstat/undergraduate/programs/b-sc/minor-statistics-b-sc'
    url = 'https://www.mcgill.ca/study/2022-2023/faculties/engineering/undergraduate/programs/bachelor-engineering-beng-bioengineering'

    dl = Download(url)
    dl.request()
    print(dl.get_courses_from_program_page())
