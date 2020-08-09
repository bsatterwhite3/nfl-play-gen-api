# nfl-play-gen-api

This is an API designed to enable random generation (or sampling) of NFL plays. 

The API is built as a Flask app in Python with a single endpoint: `GET /plays`. This endpoint can be provided with filters
for playType and fieldPosition, and a configurable number of plays (numPlays).  

## General Use

### API Specifications

The specification for the API can be found on [swaggerhub](https://app.swaggerhub.com/apis/bsatterwhite3/nfl-play-gen-api/1.0.0) or 
in the local api-spec folder.

### Example Use
To test out the API, run the following terminal commands from the root folder:
```
docker build -t  playgen .     # Build image
docker run -d -p 5000:5000     # Run in detached mode and expose port 5000
curl http://0.0.0.0:5000/plays # GET request for /plays endpoint 
```

## Development

### Project Structure

Though the actual Flask `app.py` is in the root folder, the code primarily lives in the `playgen` directory, which
contains the following modules:
- `dataloader.py`: used to load NFL play-by-play data either from local cache or from [nflfastR](https://github.com/guga31bb/nflfastR-data#load-data-using-python) repo
- `exceptions.py`: contains custom exceptions used in part to construct HTTP error codes
- `filters.py`: contains Filter classes used to filter down data for request
- `handlers.py`: contains the bulk of the code for handling the actual HTTP request
- `playsampler.py`: module for generating (sampling) plays from the provided data

### Installing

To install the application for local development:
1. Create virtual environment of your choice with Python 3.7 installed (`conda`, `virtualenv`, `pyenv`, etc.)
2. Run `python setup.py install`

This will install the project on your local machine along with the libraries listed in the `requirements.txt` file.

### Testing

Once the project is installed locally, run `pip install -r test-requirements.txt` to install the packages for testing.

Then run `python -m pytest tests` to run the tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* The data used in this API comes from [nflfastR](https://github.com/guga31bb/nflfastR-data#load-data-using-python)
