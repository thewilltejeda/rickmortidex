from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse


from time import sleep
from random import randint
from typing import Optional

import json
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('rick_and_morty_dataset.json', 'r') as f:
    data = json.load(f)

@app.get("/data", response_class=HTMLResponse)
async def get_data(search_input: Optional[str] = Query(None)):

    results = data
    html_content = ""

    sleep(2)

    # Filter data based on search input
    if search_input:
        filteredData = []
        for person in data:
            if search_input.strip().lower() in person["name"].lower():
                if person not in filteredData:
                    filteredData.append(person)

        results = filteredData

    if results:
        for item in results:
            # Generate HTML content for each item
            html_content += f"""
                <div class="flex flex-col flex-wrap justify-center items-center bg-white rounded-2xl max-w-xs overflow-hidden p-4 border border-white h-full w-full">
                    <img src="{item['image']}" class="rounded-2xl h-full w-full" />            
                    <div class="flex flex-col text-xs gap-2 p-4 h-full w-full my-auto">
                        <h3 class="mt-4 font-bold text-center text-4xl drop-shadow-2xl">{item['name']}</h3>
                        <p><strong>Id</strong>: {item['id']}</p>
                        <p><strong>Species</strong>: {item['species']}</p>
                        <p><strong>Origin</strong>: {item['origin']['name']}</p>
                        <p><strong>Location</strong>: {item['location']['name']}</p>
                        <p><strong>Episodes:</strong> {len(item['episode'])}</p>
                        <p><strong>Status</strong>: {item['status']}</p>
                    </div>
                </div>
            """

    else: 
            # Generate HTML content for no results found
            html_content = f""" 
                <div 
                    id="error"
                    class="flex-1 justify-center p-16 w-full"
                    hx-swap-oob="true"
                    hx-swap="outerHTML"
                    
                >
                    <img  class="mx-auto rounded-full w-32 h-32 md:w-64 md:h-64" src="https://i.giphy.com/media/RH1IFq2GT0Oau8NRWX/giphy.webp" />
                    <p class="pt-3 text-white text-center text-xl font-bold">Oh No! Nothing was found :(</p>
                </div>

            """

    return html_content


# Run the FastAPI application using uvicorn server
if __name__ == "__main__":
    uvicorn.run("backend:app", port=8000, reload=True)


