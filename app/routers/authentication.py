from sqlalchemy.orm import Session
from .. import schemas, models, database
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..hashing import Hash
from ..configs.tokenConfig import Settings

setting = Settings()

router = APIRouter(
    tags=['Authentication']
)

hash = Hash()
@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid Credentials")
    
    if not hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Invalid Credentials")
    

    # Generate JWT Token and return it
    return user