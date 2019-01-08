import re
import requests
from lxml import html
from bs4 import BeautifulSoup


class Course:
    def __init__(self, cid: str, ctitle: str, cunits: str, cdesc: str, so: list, preq: str =None, restric: str =None,
                 overlap: str =None, concurr: str =None, same: str =None, grading: str =None,
                 repeat: str =None, cat: str =None):
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


def create_course(parsable: html.Element, courseID: str) -> Course:
    cid = ""
    ctitle = ""
    cunits = ""
    cdesc = ""
    preq = None
    restric = None
    overlap = None
    concurr = None
    same = None
    grading = None
    repeat = None
    cat = None
    spillover = list()

    courses = get_class_titles(parsable)
    reID = re.compile(r'^{}'.format(courseID + ' *\.'))
    try:
        for place, course in enumerate(courses, start=1):
            matching = reID.search(course.replace(u'\xa0', u' '))
            if matching is not None:
                cid = matching[0]
                print("MATCH: " + cid)
                cunits = re.search(r'(.+)\. *([^\d]+)\. *(.+)\.', courses[place - 1]).group(3)
                ctitle = courses[place - 1].replace(u'\xa0', u' ').replace(cid, '') \
                    .replace(cunits, '').replace('.', '').strip()
                descs = get_course_desc_list(parsable, place)
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
                return Course(cid=cid, ctitle=ctitle, cunits=cunits, cdesc=cdesc, preq=preq, restric=restric,
                              overlap=overlap,
                              concurr=concurr, same=same, grading=grading, repeat=repeat, cat=cat, so=spillover)
    except Exception as e:
        raise e


def get_course(courseid: str) -> Course:
    split = courseid.split()
    section = " ".join(split[0:len(split) - 1])
    section = re.sub(r'/|&| ', "_", section).lower()
    print(section)
    parsable = parsable_html(request_courses_section(section).content)

    try:
        return create_course(parsable, courseid.upper())
    except Exception as e:
        print("ERROR: " + e)


def is_category(potential: str) -> bool:
    '''NOT IMPLEMENTED YET'''
    return False


def request_courses_section(section: str) -> requests.Response:
    '''This function returns a get request for the specified section
        The section must be lowercase and contain no spaces symbols and spaces must be converted to underscores
        DOESNT HANDLE GET EXCEPTIONS'''
    return requests.get("http://catalogue.uci.edu/allcourses/" + section + "/", timeout=10)


def parsable_html(pagebytes: bytes) -> html.Element:
    '''returns an Element html class from the lxml library'''
    return html.fromstring(pagebytes)


def get_class_titles(parsable: html.Element) -> [str]:
    '''gets a list of the course block titles for a parsable html page
    this should be a section of the UCI catalogue'''
    return parsable.xpath('//div[@class="courseblock"]//p[@class="courseblocktitle"]//strong/text()')


def get_course_desc_list(parsable: html.Element, course: int) -> [html.Element]:
    return parsable.xpath('//div[@class="courseblock"][{c}]//div[@class="courseblockdesc"]/child::p'.\
                          format(c=course))

def get_course_ids(letter: str) -> [str]:
    '''gets a list of all the tags for a beginning letter'''
    page = requests.get("http://catalogue.uci.edu/allcourses/", timeout=10)
    soup = BeautifulSoup(page.content, "lxml")
    ids = re.findall(r"(\(.*\))", soup.find(id=letter).find_next_sibling().text)
    return [id.strip("()") for id in ids]



if __name__ == "__main__":
    # user_input = input("Enter Course name: ")
    # while user_input != "stop":
    #     get_course(user_input).print_course()
    #     user_input = input("Enter Course name: ")

    user_input = input("Enter Course Letter: ")
    while user_input != "stop":
        for id in get_course_ids(user_input):
            print(id)
        user_input = input("Enter Course Letter: ")

    # pat = re.compile("(\(.*\))")
    # page = requests.get("http://catalogue.uci.edu/allcourses/")
    # soup = bs4.BeautifulSoup(page.content, "lxml")
    # ids = re.findall(pat, soup.find(id="A").find_next_sibling().text)
    #
    # for id in ids:
    #     print(id.strip("()"))








