from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from providers import PROVIDER_MAP

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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
    # Fetches the last 20 completed generations, newest first
        return db.query(models.Generation).filter(models.Generation.status == "completed").order_by(models.Generation.created_at.desc()).limit(20).all()