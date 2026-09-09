from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Document


#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Document API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents")
def create_document(name: str, content: str):
    db: Session = SessionLocal()

    document = Document(
        name=name,
        content=content,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    db.close()

    return {
        "id": document.id,
        "name": document.name,
        "content": document.content,
    }


@app.get("/documents")
def get_documents():
    db: Session = SessionLocal()

    documents = db.query(Document).all()

    result = [
        {
            "id": document.id,
            "name": document.name,
            "content": document.content,
        }
        for document in documents
    ]

    db.close()

    return result
