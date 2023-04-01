# PDF-Processor-React-Flask

Process PDF files using React and Flask

## Installation

1. Clone the repository using `git clone`
2. Navigate to the directory using `cd PDF-Processor-React-Flask`

### Server

1. Navigate to the server directory using `cd backend`
2. Create a virtual environment on Mac and activate it using `python3 -m venv venv` and `source venv/bin/activate` or Create a virtual environment on Windows and activate it using `python -m venv venv` and `./venv/Scripts/activate`
3. Upgrade pip to the latest version using `pip install --upgrade pip`
4. Install flask using `pip install flask`
5. Install flask_cors using `pip install flask_cors`
6. Run the server using `flask run` in the virtual environment
7. The server will be running on `localhost:5000`

### Client

1. Navigate to the client directory using `cd frontend`
2. Install the dependencies using `npm install`
3. Run the client using `npm start`
4. The client will be running on `localhost:3000`

## Usage

1. Select a file from your computer
2. Click the upload button
3. Upload progress and spinner will be displayed
4. The file will be uploaded and saved in the local directory `backend/app/Downloads`

## References

https://github.com/timleungtech/pdfprocessor
