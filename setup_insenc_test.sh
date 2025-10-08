if [ -d .insertion_encoding ]
then
    cd .insertion_encoding
    git pull
    cd ..
else
    git clone --depth 1 https://github.com/Ollson2921/cperms_ins_enc.git .insertion_encoding
fi

cd .insertion_encoding
pip install --force-reinstall --no-cache-dir .
cd ..
