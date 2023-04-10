from bs4 import BeautifulSoup
import os
import concurrent.futures

# set the input and output directories
input_dir = "C:/Users/karen/OneDrive/Documentos/AI/ClassCentral_Hindi/html"
output_dir = "C:/Users/karen/OneDrive/Documentos/AI/ClassCentral_Hindi/html/complete"

# define the batch size
batch_size = 16
#
# define a function to translate a batch of HTML files
def html_batch(file_paths):
    for file_path in file_paths:
        # read the HTML file
        with open(file_path, encoding="utf-8") as fp:
            response = fp.read()

        # parse the HTML
        soup = BeautifulSoup(response, "lxml")

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

        # save the modified HTML
        file_name = os.path.basename(file_path)
        output_file_path = os.path.join(output_dir, file_name)
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))

# get a list of all HTML files in the input directory
file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.html')]

# split the file paths into batches and translate each batch
for i in range(0, len(file_paths), batch_size):
    batch = file_paths[i:i+batch_size]
    html_batch(batch)