# prepare the container and install the dependencies
BASE_DIR="/webapp"
# install the dependencies
pip install -r ${BASE_DIR}/requirements.txt
python -m build
cp -r dist/ templates/