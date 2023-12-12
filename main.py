from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
import fitz  # PyMuPDF library
from transformers import AutoTokenizer, AutoModelWithLMHead
import nest_asyncio
from pyngrok import ngrok
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Path to store uploaded files
upload_directory = '/content/uploaded_files'
text_directory = '/content/text_files'


# Home route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}


@app.post("/file")
async def upload_file(file: UploadFile = File(...)):
    # Do here your stuff with the file
    return {"filename": file.filename}

@app.post("/extract-text")
async def extract_text_from_pdf(file: UploadFile = UploadFile(...)):
    try:
        # Read PDF content
        pdf_content = await file.read()

        # Open PDF with PyMuPDF
        pdf_document = fitz.open("pdf", pdf_content)

        # Initialize an empty string to store extracted text
        text = ""

        # Iterate through pages and extract text
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        # Close the PDF document
        pdf_document.close()

        return JSONResponse(content={"extracted_text": text}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def extract_text_from_pdf(file: UploadFile = UploadFile(...)):
    try:
        # Read PDF content
        pdf_content = await file.read()

        # Open PDF with PyMuPDF
        pdf_document = fitz.open("pdf", pdf_content)

        # Initialize an empty string to store extracted text
        text = ""

        # Iterate through pages and extract text
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        # Initialize the model and tokenizer
        tokenizer=AutoTokenizer.from_pretrained('T5-base')
        model=AutoModelWithLMHead.from_pretrained('T5-base', return_dict=True)

        # Encode the text
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt",truncation=True)

        # Generate the summary
        outputs = model.generate(inputs,
        max_length=1000, min_length=100)

        # Decode the summary
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return JSONResponse(content={"summary": summary}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example Usage:
# Send a PDF file to http://your-fastapi-host/extract-text using your frontend.


# specify a port
port = 8000
ngrok_tunnel = ngrok.connect(port)

# where we can visit our fastAPI app
print('Public URL:', ngrok_tunnel.public_url)


nest_asyncio.apply()

# finally run the app
uvicorn.run(app, port=port)
