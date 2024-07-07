# Send a HEAD request and capture the location header
location=$(curl -s -I https://www.worldcubeassociation.org/export/results/WCA_export.tsv | grep -i location)
url=$(echo $location | awk '{print $2}' | tr -d '\r')

# Specify the output directory and download the file
output_dir="results_dump"
mkdir -p "$output_dir"
curl -o "$output_dir/wca_results.zip" "$url"

# Unzip the downloaded file
unzip "$output_dir/wca_results.zip" -d "$output_dir"

# Run your script to process the files
python3 droprows.py "$output_dir"/WCA_export_Competitions.tsv "$output_dir"/WCA_export_Results.tsv "$output_dir"/Competitions.csv "$output_dir"/Results.csv

# Remove the downloaded zip file and extracted files
rm -f "$output_dir/wca_results.zip" "$output_dir"/*.tsv "$output_dir"/metadata.json "$output_dir"/README.md
