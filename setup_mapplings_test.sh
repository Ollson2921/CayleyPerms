if [ -d .mapplings ]
then
    cd .mapplings
    git pull
    cd ..
else
    git clone --depth 1 https://github.com/Ollson2921/MapplePy.git .mapplings
fi

cd .mapplings
pip install --force-reinstall --no-cache-dir .
cd ..
