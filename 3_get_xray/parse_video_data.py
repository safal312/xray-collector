from utils.PrimeVideoPageHandler import PrimeVideoPageHandler

pvph = PrimeVideoPageHandler(path="./metadata/com", save_to="./parsed_metadata/com/meta_en_prime.csv")
pvph.parse_files()