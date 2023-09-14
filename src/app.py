from fastapi import FastAPI, Body, Response, HTTPException
import numpy as np
from typing import List
from pydantic import BaseModel
import json
import logging
from pymilvus import Collection, connections, utility

MILVUS_ALIAS = 'default'
MILVUS_HOST = 'localhost'
MILVUS_HOST_PORT = '9091'
MILVUS_COLLECTION = 'job_description_emb'
MILVUS_ALIAS_NAME = "default"

connections.connect(
  alias=MILVUS_ALIAS_NAME
)


#search_params = {"metric_type": "L2", "params": {"nprobe": 84}, "offset": 0}

collection = Collection(MILVUS_COLLECTION)
distance_threshold = 0.2
search_params = {"metric_type": "L2",  "max_distance": distance_threshold, "params": {"nprobe": 64}}


app = FastAPI(docs_url="/swagger")


class SearchDataInput(BaseModel):
    embeddings: List[List[float]] = Body(...)
    class Config:
        schema_extra = {
            "example": {
                "embeddings": [[-1.2683e-01, -2.0361e-01,  3.2861e-01],[-1.0303e-01,  1.8164e-01, -2.5925e-02]]
            }
        }       

    
class InsertDataInput(BaseModel):
    embeddings: List[List[float]] = Body(...)
    job_ids: List[str] = Body(...)
    class Config:
        schema_extra = {
            "example": {
                "embeddings": [[-1.2683e-01, -2.0361e-01,  3.2861e-01],[-1.0303e-01,  1.8164e-01, -2.5925e-02]],
                "job_ids": ['720052108','160056105']
            }
        }             
 

    
@app.get("/health_check")
def health_check():
    message = {'message': 'Success', "status_code": 200}
    return Response(content=json.dumps(message), media_type="application/json")            
        
@app.get("/count")
def get_count():
    count = collection.num_entities
    message = {'count': count}
    return Response(content=json.dumps(message), media_type="application/json")


@app.get("/index_processing")
def index_processing():
    
    message = utility.index_building_progress(MILVUS_COLLECTION)
    return Response(content=json.dumps(message), media_type="application/json")


@app.get("/load_index")
def load_index():
    collection.load()
    message = {'message': 'Success', "status_code": 200}
    return Response(content=json.dumps(message), media_type="application/json")


@app.post("/search")
async def search_data(data: SearchDataInput):
    
    try:
        embeddings = np.array(data.embeddings).tolist()
        results = collection.search(
            data=embeddings, 
            anns_field="embeddings", 
            param=search_params,
            limit=5, 
            expr=None,
    )   
        distance_list = [i.distances for i in results]
        job_ids = [i.ids for i in results]
        result_json = {'distances': str(distance_list), 'job_ids': str(job_ids)}
        message = result_json

    except Exception as e:
        logging.exception('Error occurred while searching data: {}'.format(str(e)))
        raise HTTPException(status_code=500, detail=str(e))   
    return Response(content=json.dumps(message), media_type="application/json")



@app.put("/insert")
def insert_data(data: InsertDataInput):
    embeddings = data.embeddings
    job_ids = data.job_ids
    
    temp_data = [
        job_ids,
        embeddings 
    ]    
    insrt_flag = collection.insert(temp_data) 
    message = {'insert_count':insrt_flag.insert_count, 'timestamp': insrt_flag.timestamp,'success': insrt_flag.succ_count}
    return Response(content=json.dumps(message), media_type="application/json")

#uvicorn src.app:app --reload --host 0.0.0.0 