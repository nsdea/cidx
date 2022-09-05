# This is the runner for the Flask server

echo "Please enter your sudo password if asked."
sudo echo "Done. Server can start."


while true
do
    /stuff/./pypy3.9-v7.3.9-linux64/bin/pypy -m pip install -r requirements.txt
    echo · Started CIDX ·
    /stuff/./pypy3.9-v7.3.9-linux64/bin/pypy cidx/app.py
    echo · Stopped CIDX ·
    sleep 3
done