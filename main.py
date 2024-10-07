from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app_logger import logger
import warnings 

app = FastAPI()

# Load the Jinja2 templates from the 'templates' directory
templates = Jinja2Templates(directory="templates")

# Define a threshold to trigger a warning for large numbers
LARGE_NUMBER_THRESHOLD = 1_000_000

# Route to render the HTML form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle form submission and perform division
@app.post("/divide", response_class=HTMLResponse)
async def divide(request: Request, numerator: str = Form(...), denominator: str = Form(...)):
    logger.debug(f"Received input: numerator={numerator}, denominator={denominator}")
    
    try:
        # Validate if inputs can be converted to integers
        numerator = int(numerator)
        denominator = int(denominator)

        # Trigger a warning if the numbers are too large
        if abs(numerator) > LARGE_NUMBER_THRESHOLD or abs(denominator) > LARGE_NUMBER_THRESHOLD:
            warnings.warn(f"Large numbers detected: numerator={numerator}, denominator={denominator}",
                          UserWarning)
        
        if denominator == 0:
            logger.error("Division by zero attempted.")
            return templates.TemplateResponse("index.html", {"request": request, "error": "Division by zero is not allowed."})

        result = numerator / denominator
        logger.info(f"Division successful: {numerator} / {denominator} = {result}")
        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except ValueError as ve:
        logger.error(f"Invalid input types: {numerator}, {denominator}. Error: {str(ve)}")
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid input. Only integers are allowed."})
    
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        return templates.TemplateResponse("index.html", {"request": request, "error": "An unexpected error occurred."})

# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled Exception: {str(exc)}")
    return {"detail": "An unexpected error occurred."}
