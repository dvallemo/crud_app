from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post (BaseModel):
    title: str
    content: str
    published: bool = True #if user does not provide a value, default will be set to true
    rating: Optional[int] = None

my_posts = [

    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    
    {"title": "favorite foods", "content": "I like pizza", "id": 2}

    ]

def find_post(id): #find a post given an id
    for p in my_posts: #iterate over my_posts array
        if p["id"] == id: #p=the specific post given an id input, if p has an id which equals to the id inputed
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

#request Get method url: "/", checks line by line

#path operation or route
@app.get("/") #decorator http get method
def root():
    return {"message": "Welcom to my API"}

@app.get("/posts")
def get_posts(): 
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): #Post pydantic class stored in post variable
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict) #converts new_post into a python dictionary(same as post.dict()), appends new post in my_posts aray
    return {"data": post_dict}
#title string, content string, Boolean published (maybe)

@app.get("/posts/{id}")
def get_post(id: int): #fastapi validates that its int only
    post = find_post(id) #created new varaible post that stores in the post that was found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"Post Detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    #if id of post does not exist
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post wid id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #no need to send data back when using delete status code

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    #if id of post does not exist
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post wid id {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
        


