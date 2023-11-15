from utils.FirefoxDriver import FirefoxDriver
from utils.FileHandler import FileHandler
from utils.UserInput import UserInput

INIT_FILE = "../metadata_for_validation.csv"        # this is the file we start with for validation
VALIDATED_FILE = "validated_metadata.csv"       # this is the file created for each line validated. Then, the line is copied to this file

fh = FileHandler(INIT_FILE, VALIDATED_FILE)
ui = UserInput(init_file=INIT_FILE, export_file=VALIDATED_FILE)

# Create a new instance of Firefox driver
driver = FirefoxDriver()
driver.initiate_two_screens()

for index, row in fh.get_df().iterrows():
    print("Index: ", index)
    
    driver.switch_to.window(driver.window_handles[0])

    # Open the first link in the first window
    if row['movie_id']:
        imdb =  'https://www.imdb.com/title/' + 'tt' + str(row['movie_id'])
        driver.get(imdb)
    else: print("Movie ID not available")

    driver.switch_to.window(driver.window_handles[1])
    
    if row['link']:
        prime = 'https://www.amazon.com' + str(row['link'])
        driver.get(prime)
    else: print("Link not available")
    

    # get user input
    res_row = ui.ask_assessment(row)
    print(res_row, "\n")
    fh.save_data(res_row)

print("Validation Done!")
driver.quit()