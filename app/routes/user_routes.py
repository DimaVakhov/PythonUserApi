from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import User
from app.auth import create_access_token, verify_password, verify_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

@router.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = User.load_from_db(form_data.username)
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
        token = create_access_token(data={"sub": user.login, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

@router.post("/create")
async def create_user(role: str, login: str, password: str):
    try:
        user = User(role, login, password)
        user.save_to_db()
        return {"status": "success", "message": f"User {login} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/delete")
async def delete_user(login: str, token: str = Depends(oauth2_scheme)):
    user  = verify_token(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        User.delete_from_db(login)
        return {"status": "success", "message": f"User {login} was deleted"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {login} not found")

@router.get("/")
async def list_users():
    users = User.display_users()
    return {"status": "success", "data": users}

@router.get("/{login}")
async def get_one_user(login: str):
    try:
        user = User.load_from_db(login)
        return {"status": "success", "data": {"role": user.role, "login": user.login}}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {login} not found")

@router.put("/change-password")
async def change_password(old_password: str, new_password: str, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    login = payload["sub"]

    try:
        user = User.load_from_db(login)
        user.change_password(old_password, new_password)
        return {"status": "success", "message": "Password updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
