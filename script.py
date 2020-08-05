import requests
import bs4
import os

def get_word(word, output_file):
  # Prepare url by concatenating desired word to the end open
  # Merriam-Webster generic dictionary url
  url = "https://www.merriam-webster.com/dictionary/" + word

  # Just to make sure it works, disguise request as if it were
  # a real person making it
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

  # Retrieve website in the form of "resposne"
  response = requests.get(url, headers=headers)

  # Store website to html file inside websites folder
  with open(output_file, "w+") as fp:
    fp.write(response.text)



def extract_definition(word, input_file):
  # Retrieve website from html file inside websites folder
  website = ""
  with open(input_file, "r") as fp:
    website = fp.read()

  # Parse html file with Beautiful Soup
  soup = bs4.BeautifulSoup(website, 'html.parser')

  # Begin extracting the most relevant section
  definition_wrapper = soup.select_one("#definition-wrapper.container")

  # Extract header sections, which contain part of speech
  row_headers = definition_wrapper.select("div.row.entry-header")
  # Extract dictionary entries, which contain definition(s)
  dictionary_entires = definition_wrapper.select("div[id^=dictionary-entry-]")

  # Iterate over retrieved definitions
  index = 0
  while index < len(dictionary_entires):

    # Extract part of speech
    part_of_speech = row_headers[index]\
      .select_one("span.fl").get_text()

    # Extract all definitions the specific entry might have
    definitions = dictionary_entires[index]\
      .select("div.vg")

    resulting_definition = ""
    
    # Iterate over every definition in dictinary entry
    for definition in definitions:
      current_definition = ""

      # Extract sub-definitions and concatenate formatted definitions to current_definition
      sub_definitions = definition.select("div.has-num")
      for sub_definition in sub_definitions:
        current_definition += sub_definition.get_text() + "\n"

      # Concatenate current definition(s) to resulting definitions
      resulting_definition += current_definition + "\n"

    # Display this entry to the user
    print("-" * 10 + " Definition #" + str(index + 1) + " " + "-" * 10)
    print("Part of speech: " + part_of_speech)
    print(resulting_definition)
    print()


    index += 1


def get_definition(word):
  # Make word lowercase and remove surrounding whitespace
  word = word.lower().strip()

  # Name of the file in which the website will be stored
  filename = "websites/" + word + ".html"

  if not os.path.isfile(filename):
    get_word(word, filename)
  extract_definition(word, filename)

get_definition("baby")
