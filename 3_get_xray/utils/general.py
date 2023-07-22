import os

def extract_remaining(main_df):
    files = os.listdir("./metadata/com")

    main_df['fname_html'] = main_df['fname'] + ".html"
    df = main_df[~main_df['fname_html'].isin(files)]
    return df

def get_remaining_xrays(main_df):
    files = os.listdir("./xrays/com")

    main_df['fname'] = main_df['file'].str.replace(".html", "")

    df = main_df[~main_df['fname'].isin(files)]
    return df