import gradio as gr
from dotenv import load_dotenv


load_dotenv()


from ..engines import UiEngine
from ..utils.locales import LOCALES
from .components import create_database_block, create_functions_block, create_tools_block


def create_ui(lang):
    global LOCALES
    LOCALES = {key: value[lang] for key, value in LOCALES.items()}
    with gr.Blocks() as demo:
        engine = UiEngine()
        gr.HTML("<center><h1>RAG Panel</h1></center>")
        search_result_state = gr.State()

        # database
        gr.HTML("<b>Database Environment</b>")
        create_database_block(engine, LOCALES)

        # tools
        gr.HTML("<b>Tools Environment")
        create_tools_block(engine, LOCALES)

        # functions
        create_functions_block(engine, search_result_state, LOCALES)
    return demo
