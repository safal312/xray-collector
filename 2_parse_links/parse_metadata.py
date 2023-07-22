import sys
sys.path.append('../')

from AmazonPagesHandler import AmazonPagesHandler

aph = AmazonPagesHandler(path="../1_get_links/all_pages/com", save_to="./metadata/com/meta_en_prime.csv")
aph.parse_files()