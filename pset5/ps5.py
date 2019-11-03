# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    """
    Encapsulates the guid, title, description, link, and pubdate
    of a parsed story
    """
    def __init__(self, guid, title, description, link, pubdate):
        self.__guid = guid
        self.__title = title
        self.__description = description
        self.__link = link
        self.__pubdate = pubdate
    
    def get_guid(self):
        return self.__guid
    
    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description
    
    def get_link(self):
        return self.__link
    
    def get_pubdate(self):
        return self.__pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    """
    Returns True if an alert should be generated
    based on a parsed phrase
    """
    def __init__(self, phrase):
        self.__phrase = phrase
    
    def is_phrase_in(self, text):
        """ 
        Returns True if phrase is found in input text.
        Otherwise, returns False
        """
        import re

        phrase_cpy = self.__phrase[:]
        text_cpy = text[:]

        # Use regex to disregard special characters 
        spec_chars = re.escape(string.punctuation)
        matches = re.findall(r"[" + spec_chars + r"]", text_cpy)
        for match in matches:
            text_cpy = text_cpy.replace(match, " ")

        # Disregard case and split into a list of words
        p_words = phrase_cpy.lower().split()
        t_words = text_cpy.lower().split()

        count = 0

        # Searches text for start of phrase;
        # if not start not found, phrase is not found intact 
        # and trigger does not fire
        if p_words[0] in t_words:
            # Stores index to match words of phrase in the order they appear in the text
            start = t_words.index(p_words[0]) 
            for i in range(len(p_words)):
                # Words in phrase must be in the same order as words in text 
                # AND must be equal in length
                try:
                    if not p_words[i] == t_words[start+i]\
                        or not len(p_words[i]) == len(t_words[start+i]): 
                        break
                except IndexError:
                    break
                count += 1

        # Evaluates whether ALL words in phrase were found
        # according to specifications
        return count == len(p_words) 

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    """
    Returns True if article title contains target phrase.
    """
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        """Parses title of NewsStory instance for target phrase"""
        title = story.get_title()[:]
        return super().is_phrase_in(title)
        

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    """
    Returns True if article description contains target phrase.
    """
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def evaluate(self, story):
        """Parses description of NewsStory instance for target phrase"""
        desc = story.get_description()[:]
        return super().is_phrase_in(desc)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, timestamp):
        self.__timestamp = datetime.strptime(timestamp, "%d %b %Y %H:%M:%S")

    def get_timestamp(self):
        return self.__timestamp


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    """Returns True if story before time used for instantiation"""
    def __init__(self, timestamp):
        super().__init__(timestamp)
    
    def evaluate(self, story):
        # Set pubdate timezone to None for comparison between naive datetimes 
        if story.get_pubdate().replace(tzinfo=None) < super().get_timestamp():
            return True
        return False


class AfterTrigger(TimeTrigger):
    """Returns True if story published after time used for instantiation"""
    def __init__(self, timestamp):
        super().__init__(timestamp)
    
    def evaluate(self, story):
        # Set pubdate timezone to None for comparison between naive datetimes 
        if story.get_pubdate().replace(tzinfo=None) > super().get_timestamp():
            return True
        return False


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    """Returns the inverse of a particular trigger"""
    def __init__(self, trig):
        self.__T = trig
    
    def evaluate(self, x):
        return not self.__T.evaluate(x)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    """Returns True if BOTH triggers are return True"""
    def __init__(self, trig1, trig2):
        self.__T1 = trig1
        self.__T2 = trig2
    
    def evaluate(self, x):
        if self.__T1.evaluate(x) and self.__T2.evaluate(x):
            return True
        return False


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    """Returns True if EITHER trigger returns True"""
    def __init__(self, trig1, trig2):
        self.__T1 = trig1
        self.__T2 = trig2
    
    def evaluate(self, x):
        if self.__T1.evaluate(x) or self.__T2.evaluate(x):
            return True
        return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filt_stories = []
    # Filter for story that can fire off at least one trigger
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filt_stories.append(story)
                break
    return filt_stories





#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggerlist = [] # For storing triggers specified by config file 
    config = {} # For access to Trigger subclass instance using trigger name in config file

    for line in lines:
        args = line.split(",")
        if args[0] != "ADD":
            trig_type = args[1]
            phrase = args[2]
            # Switch on trig_type, instantiating appropriate Trigger subclass
            if trig_type == "DESCRIPTION":
                trig = DescriptionTrigger(phrase)
            elif trig_type == "TITLE":
                trig = TitleTrigger(phrase)
            elif trig_type == "AND":
                trigs = [args[2], args[3]]
                trig = AndTrigger(config[trigs[0]], config[trigs[1]])
            config[args[0]] = config.get(args[0], trig)
        # If line begins with "ADD", save specified triggers to list
        else:
            trigs = args[1:]
            for trig in trigs:
                triggerlist.append(config[trig])
    return triggerlist


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

