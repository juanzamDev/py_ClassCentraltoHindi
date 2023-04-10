from bs4 import BeautifulSoup, Comment
from mtranslate import translate
import concurrent.futures

# read html file locally
with open("C:/Users/karen/OneDrive/Documentos/AI/ClassCentral_Hindi/freecertificates.html", "rb") as fp:
  response = fp.read().decode("utf-8-sig").split("\n", 1)[1]

# parse the HTML
soup = BeautifulSoup(response, "html.parser")

# Remove all comments
for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    comment.extract()

# Update the index link ">
report_index = soup.find('a', href='https://www.classcentral.com/report/')
report_index['href'] = 'report.html'

# add style attribute to <div> element
header_navigation = soup.find('div', class_='site-header__navigation-row')
header_navigation['style'] = 'height: 49px;'

# Delete both containers
footer_container = soup.find('footer', class_='sticky-footer bg-gray-xxlight')
footer_container.extract()
width_container = soup.find('section', class_='width-page margin-vert-xlarge small-down-padding-horz-medium border-box')
width_container.extract()

# find all text elements in the HTML
text_elements = soup.find_all(string=True)

# define a function to translate a text element
def translate_element(element):
    if element.parent.name in ['script', 'style']:
        return str(element)
    try:
        translated_text = translate(element, 'hi')
        return translated_text
    except:
        return str(element)
    
# use multi-threading to translate the text elements
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(translate_element, text_elements)

# update the HTML with the translated text
for element, translated_text in zip(text_elements, results):
    element.replace_with(translated_text)

# save the modified HTML
with open("C:/Users/karen/OneDrive/Documentos/AI/ClassCentral_Hindi/translate.html", "w", encoding="utf-8") as file:
  file.write(soup.prettify())