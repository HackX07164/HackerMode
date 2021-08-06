wget https://github.com/Arab-developers/HackerMode/archive/refs/heads/future.zip
unzip future.zip
rm future.zip
mv HackerMode-future HackerMode
clear
echo "# start installing.../"
python3 -B HackerMode install
alias HackerMode='source /data/data/com.termux/files/home/.HackerMode/HackerMode/bin/activate'
echo Enter HackerMode to start...
echo -e "\033[0m"
