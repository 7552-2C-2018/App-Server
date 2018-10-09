cd app/

python -m pytest tests/* --cov-config .coveragerc --cov=$(pwd)/server
COVERALLS_REPO_TOKEN=9x7MsRmf6WGLZOCLpvRTW55OOxqZA63NeT0RL
