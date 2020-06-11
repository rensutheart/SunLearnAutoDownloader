from html.parser import HTMLParser
import webbrowser
import shutil
import pandas as pd
from time import time
import os

question_name = '1B'
html_file_path = 'C:\\Users\\name\\Downloads\\Submission.html'
browser_download_location = 'C:\\Users\\name\\Downloads\\'
DOWNLOAD_TIMEOUT_SECONDS = 30

class MyHTMLParser(HTMLParser):
    read_data_name = False
    look_for_next_link = False
    read_data_link_a = False

    link_count = 0 # this is used if more than 1 attachment is allowed for the submission

    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            self.read_data_name = True

        if self.look_for_next_link and tag == 'a':
            self.read_data_link_a = True
            #self.look_for_next_link = False  # this line is commented out since it allowed for only a single submission
            dataList[-1]['Link_' + str(self.link_count)] = attrs[0][1]
            #print('link: ', dataList[-1]['Link_' + str(self.link_count)])


    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        global dataList
        if self.read_data_name:
            if data.startswith('Attempt'):
                #print("Links: ", self.link_count)
                #print('Name:', data[data.find('for') + 4:])
                dataList.append({'Name': data[data.find('for') + 4:data.find('(')-1], 'StudentNum': data[data.find('(') + 1:data.find(')')]})
                self.look_for_next_link = True  # expect a link to follow soon
                self.link_count = 0
            self.read_data_name = False

        if self.read_data_link_a:
            #print('filename: ', data)
            trimmed_data = data.strip()
            dataList[-1]['FileName_' + str(self.link_count)] = trimmed_data
            dataList[-1]['Extention_' + str(self.link_count)] = trimmed_data[trimmed_data.rfind('.'):].lower()
            self.read_data_link_a = False
            self.link_count += 1


parser = MyHTMLParser()

dataList = []

f = open(html_file_path, 'r')
contents = f.read()
parser.feed(contents)
df = pd.DataFrame(dataList)
f.close()

pd.set_option('display.max_columns', None)
#print(df)


stopped_at_student = "" #str(12345678) # if the download stopped half way, by supplying the last successful student number, you can continue from there
if stopped_at_student != "":
    start_index = df.loc[df['StudentNum'] == stopped_at_student].index[0]
else:
    start_index = 0

print('Starting from index', start_index )

for i in range(start_index, len(df.get('StudentNum'))):
    print('{}: Processing student: {}'.format(i,df.get('StudentNum')[i]))
    start_time = time()

    link_count = 0
    # iterating the columns
    for col in df.columns:
        if 'Link' in col:
            #print(df.get('Link_' + str(link_count))[i])
            if not (pd.isna(df.get('Link_' + str(link_count))[i])): # check for NaN
                try:
                    webbrowser.open(df.get('Link_' + str(link_count))[i], new=2)
                except:
                    print('\nFailed to download. Link of "{}" might be empty or invalid'.format(df.get('Link_' + str(link_count))[i]))
                    continue

                while not os.path.exists(browser_download_location + df.get('FileName_' + str(link_count))[i]):
                    if int(time() - start_time) == DOWNLOAD_TIMEOUT_SECONDS:
                        start_time = time()
                        print('\tTIMED OUT: {}'.format(df.get('FileName_' + str(link_count))[i]))
                        break

                if not os.path.exists(browser_download_location + question_name):
                    os.makedirs(browser_download_location + question_name)
                sleep(0.5) # some times chrome conflicts and the file is not moved correctly
                shutil.move(browser_download_location + df.get('FileName_' + str(link_count))[i], '{}{}/{}_{}{}'.format(browser_download_location, question_name, df.get('StudentNum')[i], link_count, df.get('Extention_' + str(link_count))[i]))

                print('\tDone with ', df.get('FileName_' + str(link_count))[i])

            #sleep(0.1)

            link_count += 1
