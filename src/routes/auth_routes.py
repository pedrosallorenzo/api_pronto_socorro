# Expõe o cadastro de funcionários e o login de maneira "limpa"
# OBS.: A regra fica no service


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_session
from src.schemas.auth import StaffSignupIn, LoginIn, TokenOut
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup-staff")
def signup_staff(payload: StaffSignupIn, db: Session = Depends(get_session)):
    try:
        return {"id_funcionario": AuthService(db).signup_staff(**payload.model_dump())}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_session)):
    try:
        token, cargo = AuthService(db).login(payload.cpf, payload.senha)
        return {"access_token": token, "cargo": cargo}
    except Exception as e:
        raise HTTPException(401, str(e))
