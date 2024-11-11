import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

with open("parts.json", "r") as read_file: 
    data = json.load(read_file)

app = FastAPI()

class Part(BaseModel):
    id: int
    name: str
    description: str
    price: float

@app.get('/')
async def message():
    return {"FastAPI": "Keyboard PARTS",
            "Alfandito Rais Akbar": "18222037",
            "GET PART"   : "get part from database",
            "POST PART"  : "add part to database",
            "PUT PART "  : "update part to database",
            "DELETE PART": "delete part from database"}

@app.get('/parts/{part_id}')
async def read_part(part_id: int):
    for item in data['parts']:
        if item['id'] == part_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')

@app.post('/parts', status_code=status.HTTP_201_CREATED)
async def create_part(part: Part):
    new_part = part.dict()
    data['parts'].append(new_part)
    with open("parts.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    return new_part

@app.put('/parts/{part_id}')
async def update_part(part_id: int, updated_part: Part):
    for i, item in enumerate(data['parts']):
        if item['id'] == part_id:
            data['parts'][i] = updated_part.dict()
            with open("parts.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            return data['parts'][i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')

@app.delete('/parts/{part_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_part(part_id: int):
    for i, item in enumerate(data['parts']):
        if item['id'] == part_id:
            del data['parts'][i]
            with open("parts.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')
