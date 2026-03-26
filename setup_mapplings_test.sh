if [ -d .MapplePy ]
then
    cd .MapplePy
    git pull
    cd ..
else
    git clone --depth 1 https://github.com/Ollson2921/MapplePy.git .MapplePy
fi

cd .MapplePy
pip install --force-reinstall --no-cache-dir .
cd ..
