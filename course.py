from downloader import Download, courses
from pathlib import Path

root = Path(__file__).parent
courses = root / "courses"
courses.mkdir(parents=True, exist_ok=True)

class Course:

    """
    Course is a structure that represents a McGill Course.
    course_code(str) MUST follow this structure: [A-Z]{4}-[0-9]{3}

    numbers of credits
    course code
    course name
    course description
    prerequisites and restrictions
    """
    
    def __init__(self, course_code, overwrite=False) -> None:
        root = Path(__file__).parent
        courses = root / "courses"
        courses.mkdir(parents=True, exist_ok=True)

        self.course_code = course_code
        self.file = courses / (course_code) + '.html'
        dl = Download(self.course_code)

        if self.file.is_file() and not overwrite:
            dl.get_soup(filename = self.file)
        else:
            dl.request()
        

if __name__ == '__main__':
    # dl = Download('https://www.mcgill.ca/study/2022-2023/faculties/science/undergraduate/programs/bachelor-science-bsc-major-software-engineering')
    # dl.request()
    # course_offering = dl.get_courses_from_program_page()
    # course_code = course_offering(course_offering.find('COMP-409'))
    dl = Course('COMP-409')
     