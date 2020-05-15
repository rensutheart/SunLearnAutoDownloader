from html.parser import HTMLParser
import webbrowser
import shutil
import pandas as pd
from time import time
import os

question_name = '1B'
html_file_path = 'C:\\Users\\name\\Downloads\\Submission.html'
browser_download_location = 'C:\\Users\\name\\Downloads\\'
DOWNLOAD_TIMEOUT_SECONDS = 10

class MyHTMLParser(HTMLParser):
    read_data_name = False
    look_for_next_link = False
    read_data_link_a = False
    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            self.read_data_name = True

        if self.look_for_next_link and tag == 'a':
            self.read_data_link_a = True
            self.look_for_next_link = False
            dataList[-1]['Link'] = attrs[0][1]

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        global dataList
        if self.read_data_name:
            if data.startswith('Attempt'):
                # print('Name:', data[data.find('for') + 4:])
                dataList.append({'Name': data[data.find('for') + 4:data.find('(')-1], 'StudentNum': data[data.find('(') + 1:data.find(')')-1]})
                self.look_for_next_link = True  # expect a link to follow soon
            self.read_data_name = False

        if self.read_data_link_a:
            # print('filename: ', data)
            trimmed_data = data.strip()
            dataList[-1]['FileName'] = trimmed_data
            dataList[-1]['Extention'] = trimmed_data[trimmed_data.find('.'):].lower()
            self.read_data_link_a = False


parser = MyHTMLParser()

dataList = []

f = open(html_file_path, 'r')
contents = f.read()
parser.feed(contents)
df = pd.DataFrame(dataList)
f.close()

pd.set_option('display.max_columns', None)
#print(df)

for i in range(0, len(df.get('Link'))):
    start_time = time()
    print('Processing ', df.get('StudentNum')[i])
    try:
        webbrowser.open(df.get('Link')[i], new=2)
    except:
        print('\nFailed to download. Link of "{}" might be empty or invalid'.format(df.get('Link')[i]))
        continue

    while not os.path.exists(browser_download_location + df.get('FileName')[i]):
        if int(time() - start_time) == DOWNLOAD_TIMEOUT_SECONDS:
            start_time = time()
            print('\tTIMED OUT: {}'.format(df.get('FileName')[i]))
            break

    if not os.path.exists(browser_download_location + question_name):
        os.makedirs(browser_download_location + question_name)

    shutil.move(browser_download_location + df.get('FileName')[i], '{}{}/{}{}'.format(browser_download_location, question_name, df.get('StudentNum')[i], df.get('Extention')[i]))

    print('\tDone with ', df.get('FileName')[i])