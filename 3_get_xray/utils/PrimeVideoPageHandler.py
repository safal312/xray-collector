import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import sys
from unidecode import unidecode

# sys.path.append("../../")
sys.path.append("../")

from AmazonPagesHandler import AmazonPagesHandler

class PrimeVideoPageHandler(AmazonPagesHandler):
    def __init__(self, path, save_to):
        super().__init__(path, save_to)
    
    def save_metadata(self):
        df = pd.DataFrame(self.parsed)
        df.to_csv(self.save_to, index=False)
    
    def parse_files(self):
        # override the parse_files method
        for index, file in enumerate(self.files):
            print(f"Parsing {index + 1}/{len(self.files)}...")
            with open(file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), features='html.parser')

                item = {"file": "",
                        "synopsis": "",
                        "genres": "",
                        "amazon_rating": "",
                        "global_ratings": "",
                        "error": 0}

                try:
                    tags_div = soup.find("div", {"class": "dv-node-dp-badges"}).find("div", {"class": "dv-node-dp-badges"})
                    children = tags_div.find_all(recursive=False)
                    item["error"] = 1
                except:
                    print("Error in gathering tags")

                filename = os.path.normpath(file)
                filename = filename.split(os.sep)[-1]

                item["file"] = filename
                
                # get synopsis
                try:
                    item["synopsis"] = unidecode(soup.find("div", {"class": "dv-dp-node-synopsis"}).text.strip())
                except:
                    print("Synopsis not found")
                    item["error"] = 1

                # get generes
                try:
                    tags = soup.find("div", {"class": "dv-node-dp-genres"}).find_all("a")
                    genres = ",".join([tag.text for tag in tags])
                    item["genres"] = genres
                except:
                    print("Genres not found")
                    item["error"] = 1

                try:
                    for child in children:
                        # amazon rating, imdb rating, runtime, and release have aria-label
                        if child.get("aria-label"):
                            # this means it is the amazon rating tag
                            if "Amazon customers" in child["aria-label"]:
                                item["amazon_rating"] = child["aria-label"]
                                item["global_ratings"] = child.text
                            else:
                                item[child["data-automation-id"]] = child.text
                        else:
                            # this part is for the remaining badges in the last div
                            span_children = child.find_all(recursive=False)

                            for child in span_children:
                                if child.get("data-testid"):
                                    item[child["data-testid"]] = child.text
                except:
                    print("Error gathering some metadata")
                    item["error"] = 1

                # get link
                try:
                    play_btn = soup.find("div", {"class": "dv-dp-node-playback"}).find("a")["href"]
                    item["link"] = play_btn
                except:
                    print("Couldn't get the play button for: ", filename)
                    item["error"] = 1

                self.parsed.append(item)

        self.save_metadata()