import os

def extract_remaining(main_df, TARGET_DIR):
    files = os.listdir(f"./metadata/{TARGET_DIR}")

    main_df['fname_html'] = main_df['fname'] + ".html"
    df = main_df[~main_df['fname_html'].isin(files)]
    return df

def get_remaining_xrays(main_df, TARGET_DIR):
    if not os.path.exists("./xrays"): os.mkdir("./xrays")
    if not os.path.exists(f"./xrays/{TARGET_DIR}"): os.mkdir(f"./xrays/{TARGET_DIR}")

    files = os.listdir(f"./xrays/{TARGET_DIR}")

    df = main_df[~main_df['fname'].isin(files)]
    return df