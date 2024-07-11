import os
import csv
import requests
import zipfile
import glob


def download_file(url, output_dir):
    """
    Download a file from a given URL and save it to the specified directory.

    Parameters
    ----------
    url : str
        The URL of the file to download.
    output_dir : str
        The directory where the downloaded file will be saved.

    Returns
    -------
    str
        The file path of the downloaded file.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "wca_results.zip")

    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return file_path


def unzip_file(file_path, output_dir):
    """
    Unzip a file to a specified directory.

    Parameters
    ----------
    file_path : str
        The path to the zip file to unzip.
    output_dir : str
        The directory where the contents of the zip file will be extracted.

    Returns
    -------
    None
    """
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)


def process_competitions(input_file, output_file):
    """
    Process the competitions data file, converting it from TSV to CSV format.

    Parameters
    ----------
    input_file : str
        The path to the input competitions data file (TSV format).
    output_file : str
        The path to the output competitions data file (CSV format).

    Returns
    -------
    None
    """
    with open(input_file, "r") as src, open(output_file, "w", newline="") as res:
        csrc = csv.reader(src, delimiter="\t")
        cres = csv.writer(res, delimiter=",")
        for row in csrc:
            newrow = [row[0], row[16], row[17], row[18]]
            cres.writerow(newrow)


def process_results(input_file, output_file):
    """
    Process the results data file, converting it from TSV to CSV format.

    Parameters
    ----------
    input_file : str
        The path to the input results data file (TSV format).
    output_file : str
        The path to the output results data file (CSV format).

    Returns
    -------
    None
    """
    with open(input_file, "r") as src, open(output_file, "w", newline="") as res:
        csrc = csv.reader(src, delimiter="\t")
        cres = csv.writer(res, delimiter=",")
        for row in csrc:
            newrow = [
                row[0],
                row[1],
                row[2],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11],
                row[12],
                row[13],
            ]
            cres.writerow(newrow)


def main():
    """
    Main function to download WCA results, process them into CSV format,
    and clean up unnecessary files.
    """
    url = "https://www.worldcubeassociation.org/export/results/WCA_export.tsv"
    output_dir = "results_dump"
    sep = os.path.sep

    # Download and unzip the file
    file_path = download_file(url, output_dir)
    unzip_file(file_path, output_dir)

    # Process the files
    process_competitions(
        f"{output_dir}{sep}WCA_export_Competitions.tsv",
        f"{output_dir}{sep}Competitions.csv",
    )
    process_results(
        f"{output_dir}{sep}WCA_export_Results.tsv", f"{output_dir}{sep}Results.csv"
    )

    # Remove the downloaded zip file and extracted files
    os.remove(file_path)

    remove_files = glob.glob(os.path.join(output_dir, "*.tsv"))
    remove_files.extend(
        [
            os.path.join(output_dir, "metadata.json"),
            os.path.join(output_dir, "README.md"),
        ]
    )

    for file_name in remove_files:
        os.remove(file_name)


if __name__ == "__main__":
    main()
