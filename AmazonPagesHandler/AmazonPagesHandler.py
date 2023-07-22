import os
import csv
from bs4 import BeautifulSoup

class AmazonPagesHandler:
    def __init__(self, path, save_to):
        self.path = path
        self.files = [os.path.join(path, p) for p in os.listdir(path)]
        self.parsed = []
        self.save_to = save_to
    
    def save_metadata(self):
        with open(self.save_to, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.parsed)
    
    def parse_files(self):
        for index, file in enumerate(self.files):
            print(f"Parsing {index + 1}/{len(self.files)}...")
            with open(file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), features='html.parser')
                
                for movie in soup.find_all("div", {"class": "s-list-col-right"}):
                    movie_title = movie.find("h2").find("a")
                    title = movie_title.text.strip()
                    link = movie_title["href"]

                    tags = []
                    spans = movie.find("div", {"class": "a-size-base"}).find_all('span')
                    for span in spans:
                        if span.text != "" and span.text !=" | ":
                            tags.append(span.text)

                    tags = "|".join(tags).strip()

                    self.parsed.append([title, link, tags])
        
        self.save_metadata()
        