from fastapi import APIRouter, File, Form, UploadFile
from database import get_connection
import os
import shutil
import pandas as pd
import hashlib
import uuid
from otp import generate_otp


router = APIRouter()

# ✅ SEND OTP
@router.post("/send-otp")
def send_otp(data: dict):
    email = data["email"]
    otp = generate_otp()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR REPLACE INTO otp_verification (email, otp) VALUES (?, ?)",
        (email, otp)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("OTP:", otp)  # 🔥 For testing (replace with email API)

    return {"message": "OTP sent"}


UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Create User
@router.post("/create-user/")
async def create_user(
    first_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    otp: str = Form(...),
    image: UploadFile = File(...)
):
    file_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex[:8]}_{image.filename}"

    # Verify OTP
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM otp_verification WHERE email=? AND otp=?",
        (email, otp)
    )
    result = cur.fetchone()
    if not result:
        cur.close()
        conn.close()
        return {"status": False, "message": "Invalid OTP"}

    cur.execute(
        "UPDATE otp_verification SET is_verified=TRUE WHERE email=?",
        (email,)
    )

    # Save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Hash password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Upsert user - delete if exists, insert new
    cur.execute("DELETE FROM users WHERE email = ?", (email,))
    cur.execute("INSERT INTO users (first_name, email, password, image_url) VALUES (?, ?, ?, ?)",
                (first_name, email, hashed_password, file_path))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": True, "message": "User created"}

# ✅ Get Users
@router.get("/users/")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

# ✅ Download Excel
@router.get("/download-excel/")
def download_excel():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM users", conn)

    file = "users.xlsx"
    df.to_excel(file, index=False)

    conn.close()
    return {"file": file}

# ✅ Upload Excel
@router.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_excel(path)

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO users (first_name, email, password, image_url) VALUES (?, ?, ?, ?)",
            (row.get('first_name') or row.get('username', ''), row['email'], row['password'], row.get('image_url', ''))
        )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Upload successful"}


@router.post("/verify-otp")
def verify_otp(data: dict):
    email = data["email"]
    otp = data["otp"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM otp_verification WHERE email=? AND otp=?",
        (email, otp)
    )

    result = cur.fetchone()

    if not result:
        return {"status": False, "message": "Invalid OTP"}

    cur.execute(
        "UPDATE otp_verification SET is_verified=TRUE WHERE email=?",
        (email,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": True}


# DELETE /users/{user_id}
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return {"status": deleted, "message": "User deleted" if deleted else "User not found"}


# PUT /users/{user_id} - Update user (no OTP required)
@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    first_name: str = Form(None),
    email: str = Form(None),
    image: UploadFile = File(None)
):
    import os
    import uuid
    from fastapi import File, Form, UploadFile
    UPLOAD_DIR = "media"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Check if user exists
    cur.execute("SELECT image_url FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return {"status": False, "message": "User not found"}
    
    updates = []
    params = []
    if first_name:
        updates.append("first_name = ?")
        params.append(first_name)
    if email:
        updates.append("email = ?")
        params.append(email)
    if image and image.filename:
        # Delete old image
        old_image = user[0]
        if old_image and os.path.exists(old_image):
            os.remove(old_image)
        # Save new image
        file_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex[:8]}_{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        updates.append("image_url = ?")
        params.append(file_path)
    
    if updates:
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cur.execute(query, params)
        conn.commit()
    
    cur.close()
    conn.close()
    return {"status": True, "message": "User updated"}

