cd app/

python -m pytest tests/* --cov-config .coveragerc --cov=$(pwd)/server
COVERALLS_REPO_TOKEN=ZhlPFnicY6u0teN8LKtKAS2DbuuKxWTio coveralls
