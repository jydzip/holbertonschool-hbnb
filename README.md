# HBnB Evolution: Part 1 (Model + API)

# Installation
## 1.1 Get the API
```bash
$ git clone https://{TOKEN}@github.com/jydzip/holbertonschool-hbnb.git
$ cd holbertonschool-hbnb
```

## 1.2 Configuration environment
- Create Python environment
```bash
# For Ubuntu
$ python3 -m venv .venv

# For Windows
$ python -m venv .venv
```

- Activate Python environment
```bash
# For Ubuntu
$ source .venv/bin/activate

# For Windows
$ .venv/Scripts/activate.ps1
```

- Install requirements
```bash
$ pip install -r requirements.txt
```

# Launch API
```bash
$ python main.py
```

## Code formater
- Check if reformatted possible
```bash
$ black **/*.py --check
```

- Reformatted automatically files
```bash
$ black **/*.py
```

## Launch all tests
```bash
$ python -m unittest discover -p 'test_*.py'
```

# Containerize with Docker
## Build container
```bash
$ docker build -t api-hbnb-evolution .
```

## Start container
```bash
$ docker run -d -p 5000:5000 --name api-hbnb-evolution-container -v "$(pwd)/data:/app/data" api-hbnb-evolution
```