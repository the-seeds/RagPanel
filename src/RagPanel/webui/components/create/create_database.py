import os
import gradio as gr
from ..info import info_clear_database, info_create_database, info_destroy_database


locales = None
def create_database_block(engine, LOCALES):
    global locales
    locales = LOCALES
    with gr.Blocks() as demo:
        with gr.Row():
            storage = os.getenv("STORAGE", engine.supported_storages[0])
            storage_choice = gr.Dropdown(
                label=LOCALES["kv_storage"],
                info="please start selected storage service first",
                choices=engine.supported_storages,
                value=storage,
                allow_custom_value=True
            )

            storage_path = get_storage_path(storage)
            storage_choice.change(get_storage_path, storage_choice, storage_path)

            collection = gr.Textbox(
                value="init",
                label="collection name",
            )

        with gr.Row():
            vectorstore = os.getenv('VECTORSTORE', engine.supported_vectorstores[0])
            vectorstore_choice = gr.Dropdown(
                label=LOCALES["vectorstore"],
                info="please start selected vector store service first",
                choices=engine.supported_vectorstores,
                value=vectorstore,
                allow_custom_value=True
            )

            vectorstore_path = get_vectorstore_path(vectorstore)
            vectorstore_choice.change(get_vectorstore_path, vectorstore_choice, vectorstore_path)
            
            vectorstore_token = get_vectorstore_token(vectorstore)
            vectorstore_choice.change(get_vectorstore_token, vectorstore_choice, vectorstore_token)

        with gr.Row():
            database_confirm_btn = gr.Button(locales["apply_and_save"])
            database_clear_btn = gr.Button(locales["clear_database"])

    database_confirm_btn.click(engine.create_database,
                                [collection, storage_choice, storage_path, vectorstore_choice, vectorstore_path, vectorstore_token]
                                ).success(info_create_database)
    database_clear_btn.click(engine.clear_database).success(info_clear_database)
    return demo


def get_storage_path(storage):
    default_path = ""
    if storage is not None:
        if storage == 'redis':
            default_path = os.getenv("REDIS_URI", "redis://localhost:6379")
        elif storage == 'es':
            default_path = os.getenv("ELASTICSEARCH_URI", "http://localhost:9001")
    else:
        default_path = os.getenv("REDIS_URI", "redis://localhost:6379")
    storage_path = gr.Textbox(
        label=locales["kv_storage_uri"],
        value=default_path,
        scale=2
    )
    return storage_path


def get_vectorstore_path(vectorstore):
    label = locales["vectorstore_uri"]
    info = "the uri of your vectorstore"
    if vectorstore is not None:
        if vectorstore == 'chroma':
            default_path = os.getenv("CHROMA_PATH", "./chroma")
            label = locales["vectorstore_path"]
            info = "the path of your vectorstore"
        elif vectorstore == 'milvus':
            default_path = os.getenv("MILVUS_URI", "http://localhost:19530")
    else:
        default_path = os.getenv("CHROMA_PATH", "./chroma")
    vectorstore_path = gr.Textbox(
        label=label,
        info=info,
        value=default_path,
        scale=2
    )
    return vectorstore_path


def get_vectorstore_token(vectorstore):
    visible = False
    if vectorstore == 'milvus':
        visible = True
    vectorstore_token = gr.Textbox(
        label=locales["vectorstore_token"],
        info="the token of your vectorstore (ignore this if not set)",
        value="0",
        visible=visible
    )
    return vectorstore_token
