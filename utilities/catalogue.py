# BUILT-IN IMPORTS

import re
import time

# THIRD PARTY IMPORTS

import requests

from lxml import html
from bs4 import BeautifulSoup

# PERSONAL IMPORTS



# CUSTOM EXCEPTIONS

class CourseRequestError(Exception):
    pass

class CourseCreationError(Exception):
    def __init__(self, message: str = "No message passed"):
        Exception.__init__(self, message)

# GLOBAL CONSTANTS



# CUSTOM CLASSES

class Course:
    '''class used to store the information given in the course catalogue'''
    def __init__(self, id: str, cid: str, ctitle: str, cunits: str, cdesc: str, so: list, preq: str = None, restric: str = None,
                 overlap: str = None, concurr: str = None, same: str = None, grading: str = None,
                 repeat: str = None, cat: str = None):
        self.id = id
        self.creation_date = time.time()
        self.courseID = cid
        self.course_title = ctitle
        self.course_units = cunits
        self.course_desc = cdesc
        self.prereqs = preq
        self.restrictions = restric
        self.overlaps = overlap
        self.concurrent = concurr
        self.same_as = same
        self.grading_option = grading
        self.repeatability = repeat
        self.category = cat
        self.spillover = so

    def print_course(self):
        print("COURSE ID: ", self.courseID)
        print("COURSE TITLE: ", self.course_title)
        print("COURSE UNITS: ", self.course_units)
        print("COURSE DESC: ", self.course_desc)
        print("COURSE PREQS: ", self.prereqs)
        print("COURSE RESTRICS: ", self.restrictions)
        print("COURSE OVERLAPS: ", self.overlaps)
        print("COURSE CONCURRENT: ", self.concurrent)
        print("COURSE SAME AS: ", self.same_as)
        print("COURSE GRADING: ", self.grading_option)
        print("COURSE REPEATABILITY: ", self.repeatability)
        print("COURSE CATEGORY: ", self.category)
        print(self.spillover)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s %s (%s)" % (self.courseID, self.course_title, self.course_units)

    def __eq__(self, right):
        return (self.courseID, self.course_title) == (right.courseID, right.course_title)
    
    def __hash__(self):
        return self.id

class UCICatalogueScraper:
    """
        This is a base class that is not meant to be created as an object
        All functions are static and do not need a UCICatalogueScraper object call the method
    """
    def __init__(self):
        pass

    # PUBLIC METHODS

    @staticmethod
    def get_course(courseid: str) -> Course:
        split = courseid.split()
        section = " ".join(split[0:len(split) - 1])
        section = re.sub(r'/|&| ', "_", section).lower()
        print(section)
        try:
            parsable = UCICatalogueScraper._parsable_html(UCICatalogueScraper._request_courses_section(section).content)
        except:
            raise CourseRequestError

        try:
            return UCICatalogueScraper._create_course(parsable, courseid.upper())
        except CourseCreationError as e:
            raise e

    @staticmethod
    def get_course_ids(letter: str) -> [str]:
        '''gets a list of all the tags for a beginning letter'''
        page = requests.get("http://catalogue.uci.edu/allcourses/", timeout=10)
        soup = BeautifulSoup(page.content, "lxml")
        ids = re.findall(r"(\(.*\))", soup.find(id=letter).find_next_sibling().text)
        return [id.strip("()") for id in ids]

    # PRIVATE METHODS

    @staticmethod
    def _get_course_descriptions(descs: list) -> tuple:
        cdesc, preq, restrict, overlap, concurr, same, grading, repeat, cat = (None, None, None, None, None, None, None, None, None)
        spillover = []
        for i, d in enumerate(descs):
            temp = d.xpath('string()')
            if i is 0:
                cdesc = temp
            elif temp.startswith('Prerequisite') or temp.startswith("Corequisite"):
                preq = temp.strip()
            elif temp.startswith('Restriction:'):
                restric = temp
            elif temp.startswith('Overlaps'):
                overlap = temp
            elif temp.startswith('Concurrent with'):
                concurr = temp
            elif temp.startswith('Same as'):
                same = temp
            elif temp.startswith('Grading Option:'):
                grading = temp
            elif temp.startswith('Repeatability:'):
                repeat = temp
            elif is_category(temp):
                cat = temp
            else:
                spillover.append(temp)
        return (cdesc, preq, restrict, overlap, concurr, same, grading, repeat, cat)

    @staticmethod
    def _create_course(parsable: html.Element, courseID: str) -> Course:
        '''creates a course object from the html Element containing the various information pulled from the
        UCI course catalogue'''

        #variable storage
        cid, ctitle, cunits, cdesc = "", "", "", ""
        cdesc, preq, restrict, overlap, concurr, same, grading, repeat, cat = (None, None, None, None, None, None, None, None, None)
        spillover = []

        courses = UCICatalogueScraper._get_class_titles(parsable)
        reID = re.compile(r'^{}'.format(courseID + ' *\.'))
        try:
            for place, course in enumerate(courses, start=1):
                matching = reID.search(course.replace(u'\xa0', u' '))
                if matching is not None:
                    cid = matching[0]
                    # print("MATCH: " + cid)
                    cunits = re.search(r'(.+)\. *([^\d]+)\. *(.+)\.', courses[place - 1]).group(3)
                    ctitle = courses[place - 1].replace(u'\xa0', u' ').replace(cid, '') \
                        .replace(cunits, '').replace('.', '').strip()
                    descs = UCICatalogueScraper._get_course_desc_list(parsable, place)
                    cdesc, preq, restrict, overlap, concurr, same, grading, repeat, cat = UCICatalogueScraper._get_course_descriptions(descs)
                    return Course(id=courseID, cid=cid, ctitle=ctitle, cunits=cunits, cdesc=cdesc, preq=preq, restric=restrict,
                                overlap=overlap,
                                concurr=concurr, same=same, grading=grading, repeat=repeat, cat=cat, so=spillover)
        except Exception as e:
            raise CourseCreationError(str(e) + " with course id = %s" % courseID)

    @staticmethod
    def _is_category(potential: str) -> bool:
        '''NOT IMPLEMENTED YET'''
        raise NotImplementedError

    @staticmethod
    def _request_courses_section(section: str) -> requests.Response:
        '''This function returns a get request for the specified section
            The section must be lowercase and contain no spaces symbols and spaces must be converted to underscores
            DOESNT HANDLE GET EXCEPTIONS'''
        return requests.get("http://catalogue.uci.edu/allcourses/" + section + "/", timeout=10)

    @staticmethod
    def _parsable_html(pagebytes: bytes) -> html.Element:
        '''returns an Element html class from the lxml library'''
        return html.fromstring(pagebytes)

    @staticmethod
    def _get_class_titles(parsable: html.Element) -> [str]:
        '''gets a list of the course block titles for a parsable html page
        this should be a section of the UCI catalogue'''
        return parsable.xpath('//div[@class="courseblock"]//p[@class="courseblocktitle"]//strong/text()')

    @staticmethod
    def _get_course_desc_list(parsable: html.Element, course: int) -> [html.Element]:
        return parsable.xpath('//div[@class="courseblock"][{c}]//div[@class="courseblockdesc"]/child::p'.\
                            format(c=course))

    
class UCICatalogueCachedScraper(UCICatalogueScraper):
    """
        This course will cache a class for a specified amount of time
        If the course hasn't been scrapped since the specified amount then the course will be rescraped

        threshhold: this should be given in seconds, others can be given by multiplying the correct value

        for minutes (threshhold * 60)

        for hours   (threshhold * 3600)

        for days    (threshhold * 86400)

        recommend values for the threshhold are positive integers above 120, anything lower will most likely do nothing
    """
    def __init__(self, threshhold: int):
        """
            Finish Scrapper class
        """
        self._threshhold = threshhold
        self._cache = {}
    
    def updateThreshhold(self, threshhold: int) -> None:
        """
            Lets a user update the threshhold of the scraper
        """
        self._threshhold = threshhold

    def _rescrape_check(self, courseid: str) -> bool:
        """
            If the course hasn't been cached or the cache has expired (past threshhold)
            return True
            else
            return False
        """
        try:
            return time.time() - self._cache[courseid].creation_date > self._threshhold
        except KeyError:
            return True

    def get_course(self, courseid: str) -> Course:
        if self._rescrape_check(courseid):
            item = super().get_course(courseid)
            self._cache[courseid] = item
            return item
        else:
            return self._cache[courseid]


    
    

    





if __name__ == "__main__":
    uci_scraper = UCICatalogueCachedScraper(4*60)
    user_input = input("Enter Course name: ")
    while user_input != "stop":
        c = uci_scraper.get_course(user_input)
        print(c)
        user_input = input("Enter Course name: ")

    # user_input = input("Enter Course Letter: ")
    # while user_input != "stop":
    #     for id in get_course_ids(user_input):
    #         print(id)
    #     user_input = input("Enter Course Letter: ")

    # pat = re.compile("(\(.*\))")
    # page = requests.get("http://catalogue.uci.edu/allcourses/")
    # soup = bs4.BeautifulSoup(page.content, "lxml")
    # ids = re.findall(pat, soup.find(id="A").find_next_sibling().text)
    #
    # for id in ids:
    #     print(id.strip("()"))








