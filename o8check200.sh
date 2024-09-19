script_dir=$(dirname "$0")
cd $script_dir
wget http://localhost:8000/o8_check > response.txt
rm response.txt