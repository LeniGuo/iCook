# API说明

public目录下有user，qa，recipe，sharedRecipe四个文件夹，分别用于储存用户信息，每条问答信息，生成的菜谱信息，以及用户自己分享的菜谱信息，每个文件夹下的JSON文件，用唯一的id号命名，img文件夹下的图片用其对应内容条目的id号进行命名
```
public
├── README.md
├──user
   ├──img # avatar
├──qa
├──recipe
├──illustration # illustration of generated recipe
├──sharedRecipe
   ├──img # illustration of shaed recipe
```

**各文件夹下的JSON文件中存储的信息**

user文件夹下的JSON文件包含：
```
username
email
hashedPassword
avatar
qa (列表，用于存储qa信息的id号，即qa下JSON文件的文件名，以便检索）
recipe (列表，用于存储recipe信息的id号，即recipe下JSON文件的文件名，以便检索）
sharedRecipe (列表，用于存储sharedRecipe信息的id号，即sharedRecipe下JSON文件的文件名，以便检索）
```



qa文件夹下的JSON文件包含：

```
userID（用于存储user信息的id号，即user文件夹下JSON文件的文件名）
query（query的文本信息，字符串类型）
img
labels
selectedLabels
flag（判断生成的信息是菜谱还是建议，菜谱为1，建议为0）
answer（生成的回答信息，可能是建议，也可能是菜谱）
```
如果answer是菜谱则其包含：
```
dish
description
ingredients（列表，包含所用的食材及其用量，如2 eggs）
steps（列表）
illustration（生成的菜谱配图，存放在publi/illustration文件夹下，用qa_id命名）
```



recipe文件夹下的JSON文件包含：

```
dish
description
ingredients（列表，包含所用的食材及其用量，如2 eggs）
steps
ingredientsCompleted（列表，存储布尔类型，为是否完成的标识）
stepsCompleted（列表，存储布尔类型，为是否完成的标识）
```



sharedRecipe文件夹下的JSON文件包含：

```
dish
description
ingredients（列表，包含所用的食材及其用量，如2 eggs）
steps
image（分享的菜谱配图地址，配图存放在public/sharedRecipe/img文件夹下）
uploader（分享用户的id号）
```