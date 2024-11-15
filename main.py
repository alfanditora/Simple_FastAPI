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
            "PART": "domain/parts"}

@app.get("/parts")
async def parts():
    return {"Choose part": "domain/parts/id_part",
            "Adding part": "domain/newparts",
            "Update part": "domain/updateparts/id_part",
            "Delete part": "domain/deleteparts/id_part"}

@app.get('/parts/{part_id}')
async def read_part(part_id: int):
    for item in data['parts']:
        if item['id'] == part_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')

@app.post('/newparts', status_code=status.HTTP_201_CREATED)
async def create_part(part: Part):
    new_part = part.dict()
    data['parts'].append(new_part)
    with open("parts.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    return new_part

@app.put('/updateparts/{part_id}')
async def update_part(part_id: int, updated_part: Part):
    for i, item in enumerate(data['parts']):
        if item['id'] == part_id:
            data['parts'][i] = updated_part.dict()
            with open("parts.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            return data['parts'][i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')

@app.delete('/deleteparts/{part_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_part(part_id: int):
    for i, item in enumerate(data['parts']):
        if item['id'] == part_id:
            del data['parts'][i]
            with open("parts.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Part with ID {part_id} not found')
