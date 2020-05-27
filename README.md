# SunLearn Auto Downloader
This Python script can automatically download the documents that were submitted for essay questions in the Moodle system.

A plugin already exists for Moodle that can achieve this:
https://moodle.org/plugins/quiz_downloadsubmissions

However, since I don't have administrative rights to add it, I wrote a quick script that does it automatically from the HTML. <strong> One major advantage of this tool is that it also renames the files to the student number instead the random filenames that students assign.</strong>

<h2>Step 1: Download HTML file</h2>
<ol>
  <li>Log in to the moodle system (SunLearn) and open the quiz</li>
  <li>Under the gear icon click 'Manual grading'</li>
  <li>Click on 'grade all' next to the question you are interested in</li>
  <li>Under 'Attempts to grade' you will see the total attempts in backets, fill that number in for 'Questions per page'. If the number of attempts is very large, your browser might not be able to handle it, and you will need to break it up into segments which will individually be processed by the script.</li>
  <li>Right-click somewhere on the page (or Ctrl-S) and save the file somewhere as 'HTML Only' (on Google Chrome). The location where you save it will be the 'html_file_path' in the script</li>
  <li>Download one of the submissions and note where it is saved automatically. This is your 'browser_download_location' in the script.</li>
  <li><strong>Do not close the Moodle tab, since you must remain logged in for the downloader to work</strong></li>
</ol>

<h2>Step 2: Download files</h2>
<ol>
   <li>Download the script and open it in a text editor</li>
  <li>Update the paths according to what was determined in Step 1 and set a name for the question. This will be the name of the folder in which the files will be saved.</li>
  <li>If you have a slow internet connection or if the files are very large you can increase the 'DOWNLOAD_TIMEOUT_SECONDS' value</li><li>Ensure Python 3.7 is installed and run the file. This can be done from the command line/terminal, by navigating to the folder where the script is saved and typing <code>python AutoDownloadScript.py</code></li>
  <li>A folder will now be created and all the files will be downloaded into that folder.</li>
  
</ol>
