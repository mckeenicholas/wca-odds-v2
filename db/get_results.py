import os
import csv
import requests
import zipfile
import glob


def download_file(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Download the file
    file_path = os.path.join(output_dir, "wca_results.zip")
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return file_path


def unzip_file(file_path, output_dir):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)


def process_competitions(input_file, output_file):
    with open(input_file, "r") as src, open(output_file, "w", newline="") as res:
        csrc = csv.reader(src, delimiter="\t")
        cres = csv.writer(res, delimiter=",")
        for row in csrc:
            newrow = [row[0], row[16], row[17], row[18]]
            cres.writerow(newrow)


def process_results(input_file, output_file):
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
    # url = "https://www.worldcubeassociation.org/export/results/WCA_export.tsv"
    output_dir = "results_dump"

    # Download and unzip the file
    file_path = download_file(url, output_dir)
    unzip_file(file_path, output_dir)

    # Process the files
    process_competitions(
        f"{output_dir}/WCA_export_Competitions.tsv", f"{output_dir}/Competitions.csv"
    )
    process_results(f"{output_dir}/WCA_export_Results.tsv", f"{output_dir}/Results.csv")

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
        os.remove(file_name, FileExistsError=False)


if __name__ == "__main__":
    main()
