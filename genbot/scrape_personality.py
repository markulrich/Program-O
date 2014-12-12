# Scrapes the information for the Chat Bot's personality from dbpedia

import json, os, sys

from urllib2 import urlopen, URLError, HTTPError
from tempfile import mkstemp
from shutil import move


PERSONALITY_FILE = 'personality.json'

# Used to download the json file from dbpedia
def dl_file(name):
    # Opens the file
    try:
        name = ''.join(e for e in name if (e.isalnum() | e.isspace()))
        url = "http://dbpedia.org/data/" + name.replace(" ", "_") + ".json"
        f = urlopen(url)
        print "downloading " + url

        # Writes the file
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

        return os.path.basename(url)

    # Error handling
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


# Borrowed from StackOverflow in order to fix the broken json files given by some dbpedia pages
# by searching for a particular string pattern /U and removing it from the file.
def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))

    new_file.close()
    os.close(fh)
    old_file.close()

    os.remove(file_path)

    move(abs_path, file_path)


# Takes the raw json file given by dbpedia and processes it in order to be useful for the aiml file.
# - Filters only for key values that start with "http://dbpedia.org"
#       - Removes the url part from the key leaving only the name of the classification of the value i.e. givenName
#       - Removes the url 
#
#
def write_aiml_json_file(filename, aiml_filename):
    # Loads up the raw json file
    replace(filename, "\U", "")  # checks for signs of broken json file and fixes it if found
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()

    # Formats the raw json file
    formatted = {}
    for firstkey in data:  # the raw json file is stored in a strange way requiring two for loops to get the actual valuable keys
        for key in data[firstkey]:
            if (key.startswith("http://dbpedia.org")):
                ind = key.rfind("/") + 1
                newkey = key[ind:]
                if (newkey != "wikiPageRedirects") & (newkey != "abstract"):  # both of these property/value pairs can
                    # cause problems and they don't provide anything useful so they are filtered out
                    data_list = data[firstkey][key]
                    for i in range(len(data_list)):
                        value = data_list[i]["value"]
                        if data_list[i]["type"] == "uri":
                            ind2 = value.rfind("/") + 1
                            value = value[ind2:]
                        if (isinstance(value, basestring)):
                            value = value.replace("_", " ")
                        formatted[newkey] = value

                        # Writes the formatted json file
    with open(aiml_filename, 'w') as outfile:
        json.dump(formatted, outfile)

    # for key in formatted:
    # 	print str(key)
    # 	print " : " + str(formatted[key])


def main(person_name, fileName):
    filename = dl_file(person_name)
    write_aiml_json_file(filename, fileName)

if __name__ == '__main__':
    name = sys.argv[1]
    directory = '../bots/{}/'.format(name)
    fileName = directory + PERSONALITY_FILE
    main(name.replace('_', ' ').title(), fileName)
