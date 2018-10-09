cd app/

python -m pytest tests/* --cov-config .coveragerc --cov=$(pwd)/server
COVERALLS_REPO_TOKEN=4ZaiSkgMAMVuoXYLjYadlWE9oMbvlyxfls6F4 coveralls
