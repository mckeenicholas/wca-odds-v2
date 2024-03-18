curl -o wca_results.zip https://s3.us-west-2.amazonaws.com/assets.worldcubeassociation.org/export/results/WCA_export063_20240303T000038Z.tsv.zip
unzip wca_results.zip
rm wca_results.zip
python droprows.py
rm -rf wca_results/*.tsv