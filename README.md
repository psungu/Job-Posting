Firstly, to clone the repo following command should be executed on desired path.

```python 
$git clone https://github.com/psungu/Job-Posting.git
```

# For Notebooks

NOTE: This part is not encapsulated!
Related libraries should be installed via pip/conda.

EDA.ipynb includes basic data cleaning only for job descriptions and analysis \
In the repo, cleaned top 100 entry is added as .csv file.

model.ipynb includes generating embeddings with pre-trained Sentence Transformer model namely: "paraphrase-MiniLM-L6-v2" the main reason of choosing this model is small size. 
Tried bigger models (at least embedding dim = 768) but it takes time to generate embeddings. Source: https://www.sbert.net/docs/pretrained_models.html. \
After embeddings are generated, it is saved to .npy file. In the repo, top 100 job description encodings are added. 


# For Milvus
Firstly, Docker should be installed. Source: https://docs.docker.com/get-docker/ \
Be sure that Docker is running. \
Then, Milvus installation steps should be followed. Please install in same directory with the repository directory, other cases are not tested. \
Source: https://milvus.io/docs/install_standalone-docker.md. 

```python 
$wget https://github.com/milvus-io/milvus/releases/download/v2.3.0/milvus-standalone-docker-compose.yml -O docker-compose.yml
$docker compose up -d
```

# For FastAPI

Firstly, run the following command. Pymilvus in the environment.yml is problematic. 

```python 
$pip install pymilvus 
```
Then, run the following commands.

```python 
$docker build .
$uvicorn src.app:app --host 0.0.0.0
```
Finally, our API is up and reachable from http://0.0.0.0:8000/swagger

![image](https://github.com/psungu/Job-Posting/assets/52814705/e8b38d1b-4f3d-48ff-944e-1dec18b4fbb3)

**search** endpoint is the crutial for the project. For small demo, please open the model.ipynb and the following cells:

```python 
#Creates a collection:
%pip install pymilvus
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

#Connects to a server:
connections.connect(alias="default")

fields = [
    FieldSchema(name="job_ids", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=250),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=384)
]
schema = CollectionSchema(fields, "APIs")
```

```python
#indexing
job_description_emb= Collection("job_description_emb", schema)
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}
job_description_emb.create_index("embeddings", index)
```

```python 
#insert embeddings
sample_embeddings= np.load('sample_embeddings.npy')
sample_data = pd.read_csv('cleaned_jobpostings_sample.csv')

insert_data = [list(sample_data['Job Id']), sample_embeddings]
job_description_emb.insert(insert_data)
job_description_emb.flush()
```

Now, in the swagger **/count** will show the number of entries in Milvus.

![image](https://github.com/psungu/Job-Posting/assets/52814705/73804960-f51d-4d1c-b0ca-96a1591b34fc)

**/search** will return the top 5 most similar Job_Ids and Distance. Note that index=0 is requested embedding. \
The following example shows that Job_ids 'f8e7c2fe7bfda8455ca2e18eb1beea5a' and '5c90575d962b567019643d4a8cea127f' are the having the same job descriptions based on this result.

![image](https://github.com/psungu/Job-Posting/assets/52814705/ae4edbbd-f5f0-46af-8cd5-b2b01f0fbe67)

When we checked the dataset, we see that Job descriptions are the same but cities are different. Based on the task, embedding vectors are from only Job Descriptions. Is the following example counted as duplicate entry or not? If it is not duplicate (because cities are different), it is not possible that detecting EXACT duplicated entries just by looking at the Job Descriptions. 

![image](https://github.com/psungu/Job-Posting/assets/52814705/ac51a4a9-410c-4b45-b949-b122bc400983)


For indexing **index_processing** endpoint can be useful also:

![image](https://github.com/psungu/Job-Posting/assets/52814705/60f06e43-2984-4a2d-8899-22f6455218cf)

To load index **load_index** can be useful:

![image](https://github.com/psungu/Job-Posting/assets/52814705/7fe2c853-92f5-4cca-9270-c66e2e155cab)

It is also possible to **insert** new embeddings and Job_ids via **insert** endpoint:

![image](https://github.com/psungu/Job-Posting/assets/52814705/46028c7c-1c33-4f08-9391-7fbea8f4259c)

