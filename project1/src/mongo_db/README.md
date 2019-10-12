### Running MongoDB Load Data and CLI

Pre-requisite:
- Have `mongodb` installed and the daemon running, allowing for connection at the default `localhost:27017`
  - See installation instruction here: https://docs.mongodb.com/manual/administration/install-community/
- Have `pymongo` library installed to interface with `mongodb`.
  - Install `pymongo` using pip: `pip install pymongo`
  
Run instructions:
- Assuming you are in this dir (`/project1/src/mongo_db`)
  - To load data run: `python load_data.py`
    - This might take a while, especially loading the edges.
  - Once the above loading data is finished, to start up the interface, simply run `python user_interface.py`
    - Most user input error checking should be in place, but please DO follow the instructions and input only the requested input (i.e options 1-5 means input 1-5 only, etc...)

