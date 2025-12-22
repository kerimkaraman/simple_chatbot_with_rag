from pymilvus import MilvusClient, DataType
from google import genai
from app.models.kb_item import KnowledgeBaseItem
from app.models.response import KBResponse
import os
from dotenv import load_dotenv

load_dotenv()

MILVUS_URI = "http://localhost:19530"
DB_NAME = "chatbots"

try:
    setup_client = MilvusClient(uri=MILVUS_URI)
    if DB_NAME not in setup_client.list_databases():
        setup_client.create_database(DB_NAME)
        print(f"Yeni Veritabanı Oluşturuldu: {DB_NAME}")
    setup_client.close()
except Exception as e:
    print(f"DB Kontrol Hatası: {e}")

milvus_client = MilvusClient(
    uri=MILVUS_URI,
    db_name=DB_NAME
)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) 

def create_chatbot_collection(chatbot_id: str):
    safe_id = chatbot_id.replace("-", "_")
    collection_name = f"CHATBOT_COLLECTION_{safe_id}"

    if milvus_client.has_collection(collection_name):
        print(f"Collection zaten mevcut: {collection_name}")
        return collection_name
    
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
        description=f"Knowledge base for chatbot {chatbot_id}"
    )

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
    schema.add_field(field_name="chatbot_id", datatype=DataType.VARCHAR, max_length=64)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
    schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=512)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)

    index_params = milvus_client.prepare_index_params()
    index_params.add_index(
        field_name="vector", 
        index_type="AUTOINDEX",
        metric_type="COSINE" 
    )

    milvus_client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params
    )
    
    print(f"Created New Collection: {collection_name}")
    return collection_name


async def insert_knowledge_item(chatbot_id: str, text: str, source: str = "manual") -> KBResponse:
    collection_name = create_chatbot_collection(chatbot_id)

    try:
        embedding_resp = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        vector_values = embedding_resp.embeddings[0].values

        kb_item = KnowledgeBaseItem(
            chatbot_id=chatbot_id,
            text=text,
            source=source,
            vector=vector_values
        )
        res = milvus_client.insert(
            collection_name=collection_name,
            data=[kb_item.model_dump()] 
        )

        print(f"KB Item Inserted Successfully (Count: {res['insert_count']})")
        
        return KBResponse(
            success=True,
            message="Bilgi bankasına başarıyla eklendi.",
            inserted_ids=res["ids"]
        )

    except Exception as e:
        print(f"Error while inserting KB Item: {e}")
        return KBResponse(
            success=False,
            message=f"Hata oluştu: {str(e)}",
            error=str(e)
        )

async def search_knowledge_base_item(chatbot_id: str, search_query: str):

    collection_name = create_chatbot_collection(chatbot_id)

    if not milvus_client.has_collection(collection_name):
        print(f"Collection bulunamadı veya boş: {collection_name}")
        return ""
    
    try:

        embedding_resp = client.models.embed_content(
            model="text-embedding-004",
            contents=search_query
        )

        query_vector = embedding_resp.embeddings[0].values

        res = milvus_client.search(
            collection_name=collection_name,
            anns_field="vector",
            data=[query_vector],
            limit=3,
            search_params={"metric_type": "COSINE", "params": {}},
            output_fields=["text", "source"]
        )

        found_texts = []

        for hit in res[0]:
            text_content = hit["entity"].get("text")
            source_name = hit["entity"].get("source", "Bilinmeyen")
            score = hit["distance"]
            found_texts.append(f"- {text_content} (Kaynak: {source_name})")
        
        return "\n\n".join(found_texts)


    except Exception as e:
        print(e)
        return ""