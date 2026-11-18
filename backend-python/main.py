from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles # NEW
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from providers import PROVIDER_MAP
import os
import base64
import uuid

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# This tells FastAPI to serve the images folder so the browser can see them
os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate", response_model=schemas.GenerationResponse)
def generate_image(request: schemas.GenerationRequest, db: Session = Depends(get_db)):
    db_generation = models.Generation(
        prompt=request.prompt,
        model_id=request.model_id,
        status="processing"
    )
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)

    provider_class = PROVIDER_MAP.get(request.model_id)
    if not provider_class:
        db_generation.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid model_id")
    
    try:
        provider = provider_class()
        image_url = provider.generate(request.prompt, request.width, request.height)
        
        # NEW: Check if the provider returned a base64 image (like Cloudflare)
        if image_url.startswith("data:image"):
            # Extract the base64 data part
            header, encoded = image_url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            
            # Create a unique filename
            filename = f"{uuid.uuid4()}.jpg"
            filepath = f"images/{filename}"
            
            # Save the file to the images folder
            with open(filepath, "wb") as f:
                f.write(image_bytes)
                
            # Update the URL to point to our own FastAPI server
            image_url = f"http://localhost:8000/images/{filename}"
        
        db_generation.image_url = image_url
        db_generation.status = "completed"
        db.commit()
        db.refresh(db_generation)
        
        return db_generation
    except Exception as e:
        db_generation.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=list[schemas.GenerationResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.Generation).filter(models.Generation.status == "completed").order_by(models.Generation.created_at.desc()).limit(20).all()