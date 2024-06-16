import os
import json
import hashlib
from fastapi import FastAPI, HTTPException, Form
from uuid import uuid4
from fastapi import File, UploadFile
#from src.recog_image.interface import recog_image
#from src.gen_resp.interface import gen_response


app = FastAPI()

# 确保目录存在
os.makedirs("public/user", exist_ok=True)
os.makedirs("public/user/img", exist_ok=True)
os.makedirs("public/qa", exist_ok=True)
os.makedirs("public/qa/img", exist_ok=True)
os.makedirs("public/recipe", exist_ok=True)
os.makedirs("public/sharedRecipe", exist_ok=True)
os.makedirs("public/sharedRecipe/img", exist_ok=True)
os.makedirs("public/illustration", exist_ok=True)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 用户注册
@app.post("/register/")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), avatar: UploadFile = File(None)):
    user_id = str(uuid4())
    avatar_path = None
    if avatar:
        avatar_path = f"public/user/img/{user_id}.jpg"
        with open(avatar_path, "wb") as image_file:
            image_file.write(await avatar.read())
    
    user_data = {
        "username": username,
        "email": email,
        "hashedPassword": hash_password(password),
        "avatar": "",
        "qa": [],
        "recipe": [],
        "sharedRecipe": []
    }
    
    with open(f"public/user/{user_id}.json", 'w') as f:
        json.dump(user_data, f)
    
    return {"user_id": user_id, "message": "User registered successfully", "statusCode": 200}

# 用户登录
@app.post("/login/")
async def login(email: str = Form(...), password: str = Form(...)):
    for filename in os.listdir("public/user"):
        with open(f"public/user/{filename}", 'r') as f:
            user_data = json.load(f)
            if user_data["email"] == email and user_data["hashedPassword"] == hash_password(password):
                return {"user_id": filename.split('.')[0], "message": "Login successful", "statusCode": 200}
    raise HTTPException(status_code=401, detail="Invalid email or password")
''''
# 用户输入文字和上传图片后生成回答
@app.post("/submit-query/")
async def submit_query(user_id: str = Form(...), query: str = Form(...), file: UploadFile = File(None)):
    qa_id = f"{user_id}_{uuid4()}"
    qa_data = {"userID": user_id, "query": query, "img": None, "labels": [], "selectedLabels": [], "flag": 0, "answer": None}
    
    if file:
        # TODO：支持更多格式的图片
        img_path = f"public/qa/img/{qa_id}.jpg"
        with open(img_path, "wb") as image_file:
            image_file.write(await file.read())
        labels = recog_image(img_path)
        qa_data["img"] = img_path
        qa_data["labels"] = labels
        
        with open(f"public/qa/{qa_id}.json", 'w') as f:
            json.dump(qa_data, f)
        
        # 返回标签供用户选择
        return {"qa_id": qa_id, "labels": qa_data["labels"]}
    
    else:
        response = gen_response(query, [])
        qa_data["answer"] = response

        with open(f"public/qa/{qa_id}.json", 'w') as f:
            json.dump(qa_data, f)
        
        return {"qa_id": qa_id, "answer": qa_data["answer"]}

@app.post("/select-labels/{qa_id}")
async def select_labels(qa_id: str, selected_labels: List[str]):
    qa_path = f"public/qa/{qa_id}.json"
    if not os.path.exists(qa_path):
        raise HTTPException(status_code=404, detail="Query not found")
    
    with open(qa_path, 'r') as f:
        qa_data = json.load(f)
    
    qa_data["selectedLabels"] = selected_labels
    response = gen_response(qa_data["query"], selected_labels)
    qa_data["answer"] = response
    
    with open(qa_path, 'w') as f:
        json.dump(qa_data, f)
    
    return qa_data

# 用户确定生成食谱后生成菜谱
@app.post("/generate-recipe/{qa_id}")
async def generate_recipe(qa_id: str):
    qa_path = f"public/qa/{qa_id}.json"
    if not os.path.exists(qa_path):
        raise HTTPException(status_code=404, detail="Query not found")
    
    with open(qa_path, 'r') as f:
        qa_data = json.load(f)
    
    if qa_data["answer"]["flag"] != 1:
        raise HTTPException(status_code=400, detail="The response is not a recipe")

    # TODO
    recipe_id = f"{qa_data['userID']}_{uuid4()}"
    recipe_data = {
        "dish": qa_data["answer"]["dish"],
        "description": qa_data["answer"]["description"],
        "ingredients": qa_data["answer"]["ingredients"],
        "steps": qa_data["answer"]["steps"],
        "ingredientsCompleted": [0] * len(qa_data["answer"]["ingredients"]),
        "stepsCompleted": [0] * len(qa_data["answer"]["steps"]),
        "illustration": qa_data["answer"]["illustration"]
    }
    
    with open(f"public/recipe/{recipe_id}.json", 'w') as f:
        json.dump(recipe_data, f)
    
    # 更新用户信息
    user_path = f"public/user/{qa_data['userID']}.json"
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    user_data["recipe"].append(recipe_id)
    with open(user_path, 'w') as f:
        json.dump(user_data, f)
    
    return {"recipe_id": recipe_id, "message": "Recipe generated successfully"}

# 用户分享自己的食谱
@app.post("/share-recipe/")
async def share_recipe(user_id: str = Form(...), dish: str = Form(...), description: str = Form(...), ingredients: List[str] = Form(...), steps: List[str] = Form(...)):
    shared_recipe_id = f"{user_id}_{uuid4()}"
    shared_recipe_data = {
        "dish": dish,
        "description": description,
        "ingredients": ingredients,
        "steps": steps,
        "uploader": user_id
    }
    
    with open(f"public/sharedRecipe/{shared_recipe_id}.json", 'w') as f:
        json.dump(shared_recipe_data, f)
    
    # 更新用户信息
    user_path = f"public/user/{user_id}.json"
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    user_data["sharedRecipe"].append(shared_recipe_id)
    with open(user_path, 'w') as f:
        json.dump(user_data, f)
    
    return {"shared_recipe_id": shared_recipe_id, "message": "Recipe shared successfully"}

@app.post("/share-recipe/")
async def share_recipe(user_id: str = Form(...), dish: str = Form(...), description: str = Form(...), ingredients: List[str] = Form(...), steps: List[str] = Form(...), image: UploadFile = File(None)):
    shared_recipe_id = f"{user_id}_{uuid4()}"
    image_path = None

    if image:
        image_path = f"public/sharedRecipe/img/{shared_recipe_id}.jpg"
        with open(image_path, "wb") as image_file:
            image_file.write(await image.read())

    shared_recipe_data = {
        "dish": dish,
        "description": description,
        "ingredients": ingredients,
        "steps": steps,
        "image": image_path,
        "uploader": user_id
    }
    
    with open(f"public/sharedRecipe/{shared_recipe_id}.json", 'w') as f:
        json.dump(shared_recipe_data, f)
    
    user_path = f"public/user/{user_id}.json"
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    user_data["sharedRecipe"].append(shared_recipe_id)
    with open(user_path, 'w') as f:
        json.dump(user_data, f)
    
    return {"shared_recipe_id": shared_recipe_id, "message": "Recipe shared successfully"}


# 用户上传照片更换头像
@app.post("/upload-avatar/")
async def upload_avatar(user_id: str = Form(...), file: UploadFile = File(...)):
    user_path = f"public/user/{user_id}.json"
    if not os.path.exists(user_path):
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar_path = f"public/user/img/{user_id}.jpg"
    with open(avatar_path, "wb") as image_file:
        image_file.write(await file.read())
    
    return {"message": "Avatar uploaded successfully"}

# 用户在个人主页查看自己生成的和分享的菜谱
# TODO：根据展示内容更改
@app.get("/user-recipes/{user_id}")
async def get_user_recipes(user_id: str):
    user_path = f"public/user/{user_id}.json"
    if not os.path.exists(user_path):
        raise HTTPException(status_code=404, detail="User not found")
    
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    
    generated_recipes = []
    for recipe_id in user_data["recipe"]:
        with open(f"public/recipe/{recipe_id}.json", 'r') as f:
            generated_recipes.append(json.load(f))
    
    shared_recipes = []
    for shared_recipe_id in user_data["sharedRecipe"]:
        with open(f"public/sharedRecipe/{shared_recipe_id}.json", 'r') as f:
            shared_recipes.append(json.load(f))
    
    return {"generated_recipes": generated_recipes, "shared_recipes": shared_recipes}

# 用户查看分享的菜谱
# TODO：如果菜谱过多需要批量传输，此功能可暂时不加
@app.get("/shared-recipes/")
async def get_shared_recipes():
    shared_recipes = []
    for filename in os.listdir("public/sharedRecipe"):
        with open(f"public/sharedRecipe/{filename}", 'r') as f:
            shared_recipes.append(json.load(f))
    return {"shared_recipes": shared_recipes}

# 用户查看生成的菜谱
@app.get("/user-generated-recipes/{user_id}/{recipe_id}")
async def get_user_generated_recipe(user_id: str, recipe_id: str):
    user_path = f"public/user/{user_id}.json"
    if not os.path.exists(user_path):
        raise HTTPException(status_code=404, detail="User not found")
    
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    
    if recipe_id not in user_data["recipe"]:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe_path = f"public/recipe/{recipe_id}.json"
    if not os.path.exists(recipe_path):
        raise HTTPException(status_code=404, detail="Recipe file not found")
    
    with open(recipe_path, 'r') as f:
        recipe_data = json.load(f)
    
    return recipe_data

# 用户反转生成的菜谱中食材的标记
@app.post("/mark-ingredient-completed/{recipe_id}/{ingredient_index}")
async def mark_ingredient_completed(recipe_id: str, ingredient_index: int):
    recipe_path = f"public/recipe/{recipe_id}.json"
    if not os.path.exists(recipe_path):
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    with open(recipe_path, 'r') as f:
        recipe_data = json.load(f)
    
    if ingredient_index < 0 or ingredient_index >= len(recipe_data["ingredientsCompleted"]):
        raise HTTPException(status_code=400, detail="Invalid ingredient index")
    
    recipe_data["ingredientsCompleted"][ingredient_index] = 1 - recipe_data["ingredientsCompleted"][ingredient_index]
    
    with open(recipe_path, 'w') as f:
        json.dump(recipe_data, f)
    
    return {"message": "Successfully reversed"}

# 用户反转生成的菜谱中步骤的标记
@app.post("/mark-step-completed/{recipe_id}/{step_index}")
async def mark_step_completed(recipe_id: str, step_index: int):
    recipe_path = f"public/recipe/{recipe_id}.json"
    if not os.path.exists(recipe_path):
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    with open(recipe_path, 'r') as f:
        recipe_data = json.load(f)
    
    if step_index < 0 or step_index >= len(recipe_data["stepsCompleted"]):
        raise HTTPException(status_code=400, detail="Invalid step index")
    
    recipe_data["stepsCompleted"][step_index] = 1 - recipe_data["stepsCompleted"][step_index]
    
    with open(recipe_path, 'w') as f:
        json.dump(recipe_data, f)
    
    return {"message": "Successfully reversed"}
'''

if __name__ == "__main__":
    import uvicorn
    # 在iCook目录下运行 python api/interface.py 启动接口
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)