import requests
import pprint
from bs4 import BeautifulSoup
import re

class Download:

    """Download a web page using different methods."""

    def __init__(self, url=None):

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
        with open(filename + '.html', 'w') as fp:
            print(self.content.prettify(), file=fp)
    
class ProgramsDownload():

    def __init__(self, search, year='2022-2023'):
        self.template = f"https://www.mcgill.ca/study/{year}/programs/search?search_api_views_fulltext={search.strip().replace(' ', '+')}&sort_by=search_api_relevance&page="
    
        self.programs = {}
        self.course_search()

    def course_search(self):
        """
        Search courses using McGill api
        """

        page = 0
        while self.get_programs_from_page(self.template + str(page)):
            page += 1
    
    def get_programs_from_page(self, url):
        """
        retrieve every program from a search page
        return true if there is at least 1 program in the page
        false otherwise
        """

        has_result = False
        dl = Download(url)
        dl.request()

        programs = dl.content.find_all('a', href=True)
        p = re.compile(r'([0-9]{2,3} credits)') # match programs
        for program in programs:
            m = p.search(program.text)
            if m:
                self.programs[program.text] = 'https://www.mcgill.ca' + program['href']
                has_result = True
        
        return has_result

    def __str__(self):
        return pprint.pformat(self.programs, width=200)

    def __len__(self):
        return len(self.programs)


class CoursesDownload():

    def __init__(self, url):
        #convert course code to url
        self.url = url
        self.courses = self.get_courses_from_program_page()

    def get_courses_from_program_page(self):
        """
        Get all courses code from soup. Course code should look like this:
        MATH 222
        COMP 551
        ECSE 539
        """
        dl = Download(self.url)
        dl.request()
        course_numbers = dl.content.find_all('a',
                                                {'class': 'program-course-title'})
        
        codes = {}
        p = re.compile(r'[A-Z]{4} [0-9]{3}')
        for course_number in course_numbers:
            m = p.search(course_number.text)
            if m.group():
                codes[(m.group().replace(' ', '-'))] = course_number.text.strip().strip('*').strip()
        return codes

    def __str__(self):
        return pprint.pformat(self.courses, width=200)

    def __len__(self):
        return len(self.courses)


class CourseDownload():

    def __init__(self, code, year='2022-2023'):

        #convert course code to url
        code = code.replace(' ', '-')
        p = re.compile(r'[A-Z]{4}-[0-9]{3}')
        m = p.search(code)
        if m and len(code) == 8:
            self.url = f'https://www.mcgill.ca/study/{year}/courses/' + code
        else:
            raise(Exception("Not a valid course code"))

    def overview(self):

        dl = Download(self.url)
        dl.request()
        print(dl.content)

if __name__ == '__main__':
    
    # url_math = 'https://www.mcgill.ca/mathstat/undergraduate/programs/b-sc/minor-statistics-b-sc'
    # url = 'https://www.mcgill.ca/study/2022-2023/faculties/engineering/undergraduate/programs/bachelor-engineering-beng-bioengineering'

    # dl = Download(url)
    # dl.request()
    # print(dl.get_courses_from_program_page())

    """
    Programs search page
    """
    # dl = ProgramsDownload('software engineering')
    # print(dl)
    # print(len(dl))

    """
    Courses listing page
    """
    # url = 'https://www.mcgill.ca/study/2022-2023/faculties/engineering/undergraduate/programs/bachelor-engineering-beng-co-op-software-engineering'
    # dl = CoursesDownload(url)
    # print(dl)
    # print(len(dl))

    """
    Course page
    """
    dl = CourseDownload('COMP 409')
    dl.overview()


