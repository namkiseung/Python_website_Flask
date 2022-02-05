from markdown_editor import web_edit
from markdown_editor.editor import MarkdownDocument

MY_HTML_HEAD = 'Editor title'

def action_send(document):
    send_markdown_text(document.text)
    # or
    send_raw_html_code(document.getHtml())
    # or
    send_html_with_styles(document.getHtmlPage())
    return html_to_display_as_result, keep_running_local_server

if __name__ == '__main__':
    doc = MarkdownDocument()
    web_edit.start(doc,custom_actions=[('Save', action_send),],title=MY_HTML_HEAD)