import gradio as gr

def create_chat_tab(engine, LOCALES):
    with gr.Blocks() as demo:
        with gr.Column():
            with gr.Row():
                template_box = gr.Textbox(value=LOCALES["template"],
                                          scale=3,
                                          lines=3,
                                          label=LOCALES["template_label"],
                                          info=LOCALES["template_info"])
                with gr.Column():
                    enable_rag_checkbox = gr.Checkbox(value=True,
                                                  label=LOCALES["enable_rag"])
                    show_docs_checkbox = gr.Checkbox(value=True,
                                                     label=LOCALES["show_docs"],
                                                     info=LOCALES["show_docs_info"])
                    save_history_checkbox = gr.Checkbox(value=True,
                                                        label=LOCALES["save_history"])
            def new_chat():
                return gr.Chatbot(label=LOCALES["chat"], value="", placeholder=LOCALES["hello"])
            chat_bot = new_chat()
            with gr.Row():
                def new_query():
                    return gr.Textbox(value="",
                                      label="",
                                      scale=6,
                                      lines=5)
                query_box = new_query()
                with gr.Column():
                    chat_button = gr.Button(LOCALES["enter"], scale=3)
                    clear_button = gr.Button(LOCALES["clear_history"], scale=3)
                    
            chat_button.click(
                engine.chat_engine.update, 
                [template_box, enable_rag_checkbox, show_docs_checkbox, save_history_checkbox]
            ).then(
                engine.chat_engine.ui_chat, 
                [chat_bot, query_box], 
                chat_bot
            )
            
            query_box.submit(
                engine.chat_engine.update, 
                [template_box, enable_rag_checkbox, show_docs_checkbox, save_history_checkbox]
            ).then(
                engine.chat_engine.ui_chat, 
                [chat_bot, query_box], 
                chat_bot
            ).then(new_query, None, query_box)
            
            clear_button.click(engine.chat_engine.clear_history)
            clear_button.click(new_chat, None, chat_bot)
            clear_button.click(new_query, None, query_box)
    return demo
