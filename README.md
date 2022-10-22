# Assignment

## About the project
Test automation for hashing application.

Test cases based on Application Specification
1. Test app should answer only from PORT environment variable
2. Test app returns job identifier from hash request
3. Test app doesn't return encoded password for invalid job identifier - string
4. Test app doesn't return encoded password for invalid job identifier - int
5. Test app returns encoded password for valid job identifier
6. Test app handles not supported HTTP method DELETE
7. Test app handles not supported HTTP method PUT
8. Test app handles not supported HTTP method PATCH
9. Test app can handle multiple requests simultaneously
10. Test app should complete any inflight request after shutdown
11. Test app returns empty stats after startup


## Getting started

### Installation
1. Install hash app.
2. Clone repo 
```
git clone https://github.com/dach19/assignment.git
```

3. Create python virtual environment
```
python3 -m venv venv
```

4. Activate environment
```
source venv/bin/activate
```

5. Install dependencies
```
pip install -r requirements.txt
```


## Usage

To run the tests, follow next commands
```
python -m py.test --base-url=http://127.0.0.1 --port=8081
```

To run single test
```
python -m py.test test_hash_endpoint.py --base-url=http://127.0.0.1 --port=8081
```