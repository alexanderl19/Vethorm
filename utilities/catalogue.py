# BUILT-IN IMPORTS

import asyncio
import re
import time

# THIRD PARTY IMPORTS

import aiohttp
import requests

from lxml import html
import bs4
from bs4 import BeautifulSoup

# PERSONAL IMPORTS



# CUSTOM EXCEPTIONS

class CourseRequestError(Exception):
    pass

class CourseCreationError(Exception):
    def __init__(self, message: str = "No message passed"):
        Exception.__init__(self, message)

# GLOBAL CONSTANTS

_ALL_COURSES = "http://catalogue.uci.edu/allcourses" 

# CUSTOM CLASSES

class Course:
    '''class used to store the information given in the course catalogue'''
    def __init__(self, course_tags: dict):

        # course_tags = {
        #     'id' : None,
        #     'title' : None,
        #     'units' : None,
        #     'desc' : None,
        #     'preq' : None,
        #     'restrictions' : None,
        #     'overlap' : None,
        #     'concurrent' : None,
        #     'same' : None,
        #     'grading' : None,
        #     'repeat' : None,
        #     'category' : None,
        #     'spillover' : []
        # }
        self.creation_date = time.time()
        self.id = course_tags['id']
        self.course_id = course_tags['id']
        self.course_title = course_tags['title']
        self.course_units = course_tags['units']
        self.course_desc = course_tags['desc']
        self.prereqs = course_tags['preq']
        self.restrictions = course_tags['restrictions']
        self.overlaps = course_tags['overlap']
        self.concurrent = course_tags['concurrent']
        self.same_as = course_tags['same']
        self.grading_option = course_tags['grading']
        self.repeatability = course_tags['repeat']
        self.category = course_tags['category']
        self.spillover = course_tags['spillover']

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
        return 'ID=(%s) Title=(%s) Units=(%s)' % (self.course_id, self.course_title, self.course_units)

    def __str__(self):
        return "%s %s %s" % (self.course_id, self.course_title, self.course_units)

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
    async def get_course(course_id: str) -> Course:
        """
            attempts to get a course by course_id

            In the event an error occurs or a course can't be found a CourseCreationError is raised

            Return value Course
        """
        try:
            return await UCICatalogueScraper._create_course(course_id.upper())
        except CourseCreationError as e:
            raise e

    @staticmethod
    async def get_departments(letter: str) -> [str]:
        """
            Retrieves a list of all the course section identifers for a specific letter grouping

            Return value [str]
        """
        def helper(tag: bs4.Tag):
            return tag.has_attr('id') and letter in tag['id']

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{_ALL_COURSES}') as rsp:
                soup = BeautifulSoup(await rsp.text(), 'lxml')
                return [item for item in re.findall(r'(\(.*\))', soup.find(helper).find_next_sibling().text)]

    # PRIVATE METHODS

    @staticmethod
    async def _create_course(course_id: str) -> Course:
        """
            Retrieves a course from the UCI catalogue and converts it to a Course class object

            Return value Course
        """

        #variable storage
        course_tags = {
            'id' : None,
            'title' : None,
            'units' : None,
            'desc' : None,
            'preq' : None,
            'restrictions' : None,
            'overlap' : None,
            'concurrent' : None,
            'same' : None,
            'grading' : None,
            'repeat' : None,
            'category' : None,
            'spillover' : []
        }
        course_block = await UCICatalogueScraper._get_title_and_desc(course_id.upper())
        
        course_tags['id'], course_tags['title'], course_tags['units'] = UCICatalogueScraper._parse_title_block(course_block[0])
        for count, piece in enumerate(UCICatalogueScraper._extract_description_values(course_block[1])):
            piece = UCICatalogueScraper._parse_desc_block(count, piece)
            if piece[0] == 'spillover':
                course_tags[piece[0]] = piece[1]
            else:
                course_tags[piece[0]] = piece[1]
        return Course(course_tags)

    @staticmethod
    async def _get_title_and_desc(course_id: str) -> (bs4.Tag, bs4.Tag):
        """ 
            Asynchronous function for retrieving the title and description block for a course in a specific section

            Return Value: (bs4.Tag, bs4.Tag)
        """
        # print(course_id)
        split = course_id.split()
        section = " ".join(split[0:len(split) - 1])
        section = re.sub(r'/|&| ', "_", section).lower()
        def helper(tag: bs4.Tag):
            return tag.has_attr('class') and 'courseblock' in tag['class'] and course_id in str(tag.p.string).replace(u'\xa0', u' ')
        
        async with aiohttp.ClientSession() as session:
            async with session.get("%s/%s/" % (_ALL_COURSES, section)) as rsp:
                # print(f'{_ALL_COURSES}/{section}')
                soup = BeautifulSoup(await rsp.text(), 'lxml')
                cblock = soup.find(helper)
                return (cblock.find(attrs={'class':'courseblocktitle'}), cblock.find(attrs={'class':'courseblockdesc'}))

    @staticmethod
    def __clean_string(line: str) -> str:
        """ cleans a string of '\xa0' that occurs in strings from UCI catalogue """
        return line.replace(u'\xa0', u' ')

    @staticmethod
    def _parse_title_block(block: bs4.Tag) -> (str, str, str):
        """
            Parses the title block into the course id, title, units

            Return ('course id', 'title', 'units')
        """
        block = block.strong.text
        units = re.search(r'\. +([\d.].{0,15}Unit.+)', block)
        if units is None:
            units = 'No Units'
        else:
            units = units.groups()[0]
            block = block[:len(block)-len(units)]
        block = block.strip('. ')
        id_and_title = re.search(r'([^.]{1,15})\. +([A-Z0-9].+)', block)
        if id_and_title is None:
            # print(block)
            return ('', '', '')
        course_id = UCICatalogueScraper.__clean_string(id_and_title.groups()[0]).strip()
        course_title = UCICatalogueScraper.__clean_string(id_and_title.groups()[1]).strip()
        units = UCICatalogueScraper.__clean_string(units).strip()

        return (course_id, course_title, units)

    @staticmethod
    def _parse_desc_block(count: int, desc_block: str) -> (str, str):
        """

        """
        if count == 0:
            return ('desc', desc_block)
        elif desc_block.startswith('Prerequisite') or desc_block.startswith('Corequisite'):
            return ('preq', desc_block)
        elif desc_block.startswith('Restriction'):
            return ('restrictions', desc_block)
        elif desc_block.startswith('Overlaps'):
            return ('overlap', desc_block)
        elif desc_block.startswith('Concurrent with'):
            return ('concurrent', desc_block)
        elif desc_block.startswith('Same as:'):
            return ('same', desc_block)
        elif desc_block.startswith('Grading Option:'):
            return ('grading', desc_block)
        elif desc_block.startswith('Repeatability:'):
            return ('repeat', desc_block)
        # elif is_category(desc_block):
        #     return ('category', desc_block)
        else:
            return ('spillover', desc_block)

    @staticmethod
    def _extract_description_values(desc_block: bs4.Tag):
        """
            Generator to yield the pieces of a description block

            Values may be prereqs, descriptions, restrictions, etc
        """
        for item in desc_block.find_all('p'):
            yield UCICatalogueScraper.__clean_string(item.text)



class UCICatalogueCachedScraper(UCICatalogueScraper):

    def __init__(self, threshhold: int):
        """
            This course will cache a class for a specified amount of time
            If the course hasn't been scrapped since the specified amount then the course will be rescraped

            threshhold: this should be given in seconds, others can be given by multiplying the correct value

            for minutes (threshhold * 60)

            for hours   (threshhold * 3600)

            for days    (threshhold * 86400)

            recommend values for the threshhold are positive integers above 120, anything lower will most likely do nothing
        """
        self._threshhold = threshhold
        self._cache = {}
    
    def updateThreshhold(self, threshhold: int) -> None:
        """
            Lets a user update the threshhold of the scraper
        """
        self._threshhold = threshhold

    def reset_cache(self) -> None:
        self._cache.clear()

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

    async def get_course(self, courseid: str) -> Course:
        if self._rescrape_check(courseid):
            item = await super().get_course(courseid)
            self._cache[courseid] = item
            return item
        else:
            return self._cache[courseid]


# if __name__ == '__main__':
#     s = UCICatalogueScraper()
#     asyncio.run(s.get_course_section('A'))

# if __name__ == '__main__':
#     s = UCICatalogueCachedScraper(360)
#     start = time.time()
#     course = asyncio.run(s.get_course('COMPSCI 171'))
#     print(time.time() - start)
#     start = time.time()
#     course = asyncio.run(s.get_course('COMPSCI 171'))
#     print(time.time() - start)
#     start = time.time()
#     course = asyncio.run(s.get_course('COMPSCI 171'))
#     print(time.time() - start)
#     s.reset_cache()
#     start = time.time()
#     course = asyncio.run(s.get_course('COMPSCI 171'))
#     print(time.time() - start)
#     start = time.time()
#     course = asyncio.run(s.get_course('COMPSCI 171'))
#     print(time.time() - start)
#     print(course)
    



# if __name__ == "__main__":
#     uci_scraper = UCICatalogueCachedScraper(4*60)
#     user_input = input("Enter Course name: ")
#     while user_input != "stop":
#         c = uci_scraper.get_course(user_input)
#         print(c)
#         user_input = input("Enter Course name: ")

#     # user_input = input("Enter Course Letter: ")
#     # while user_input != "stop":
#     #     for id in get_course_ids(user_input):
#     #         print(id)
#     #     user_input = input("Enter Course Letter: ")

#     # pat = re.compile("(\(.*\))")
#     # page = requests.get("http://catalogue.uci.edu/allcourses/")
#     # soup = bs4.BeautifulSoup(page.content, "lxml")
#     # ids = re.findall(pat, soup.find(id="A").find_next_sibling().text)
#     #
#     # for id in ids:
#     #     print(id.strip("()"))








