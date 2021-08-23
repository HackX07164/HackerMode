rm -rif HackerMode
rm -rif ~/.HackerMode
git clone https://github.com/Arab-developers/HackerMode
echo -e "\n# start installing.../"
python3 -B HackerMode install
alias HackerMode="source $HOME/.HackerMode/HackerMode/bin/activate"
rm HackerModeInstall