import os

def extract_remaining(main_df, TARGET_DIR):
    """
    Extracts the remaining entries for downloading the movie's prime video page from the main dataframe.
    The movie home pages are downloaded under their respective batch-directories.
    We check if the file is already downloaded by using the unique filename (fname).

    Args:
        main_df (pd.DataFrame): The main dataframe containing the metadata of the movies.
        TARGET_DIR (str): The target directory to save the metadata.
    
    Returns:
        pd.DataFrame: The dataframe containing the remaining files to be downloaded.
    """
    files = os.listdir(f"./metadata/{TARGET_DIR}")

    main_df['fname_html'] = main_df['fname'] + ".html"
    df = main_df[~main_df['fname_html'].isin(files)]
    return df

def get_remaining_xrays(main_df, TARGET_DIR, xray_dir="../data/3_xrays"):
    """
    Returns dataframe containing the remaining movies whose xrays are to be downloaded.
    We check if the xray is already downloaded by using the unique filename (fname).

    Args:
        main_df (pd.DataFrame): The main dataframe containing the metadata of the movies with xrays.
        TARGET_DIR (str): The target directory to save the metadata.
    
    Returns:
        pd.DataFrame: The dataframe containing the remaining movies with xrays to be downloaded.
    """
    if not os.path.exists(xray_dir): os.mkdir(xray_dir)
    if not os.path.exists(f"{xray_dir}/{TARGET_DIR}"): os.mkdir(f"{xray_dir}/{TARGET_DIR}")

    files = os.listdir(f"{xray_dir}/{TARGET_DIR}")

    df = main_df[~main_df['fname'].isin(files)]
    return df