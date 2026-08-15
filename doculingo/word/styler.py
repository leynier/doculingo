from docx.text.paragraph import Paragraph
from docx.text.run import Run


def copy_run_style(run: Run, new_run: Run) -> None:
    if run.bold:
        new_run.bold = run.bold
    if run.italic:
        new_run.italic = run.italic
    if run.underline:
        new_run.underline = bool(run.underline)
    new_run.font.size = run.font.size
    new_run.font.name = run.font.name
    if run.font.color.rgb:
        new_run.font.color.rgb = run.font.color.rgb


def copy_paragraph_style(para: Paragraph, new_para: Paragraph) -> None:
    new_para.paragraph_format.left_indent = para.paragraph_format.left_indent
    new_para.paragraph_format.right_indent = para.paragraph_format.right_indent
    new_para.paragraph_format.space_before = para.paragraph_format.space_before
    new_para.paragraph_format.space_after = para.paragraph_format.space_after
    new_para.paragraph_format.line_spacing = para.paragraph_format.line_spacing
    new_para.paragraph_format.keep_together = para.paragraph_format.keep_together
    new_para.paragraph_format.keep_with_next = para.paragraph_format.keep_with_next
    new_para.paragraph_format.page_break_before = para.paragraph_format.page_break_before
    new_para.paragraph_format.widow_control = para.paragraph_format.widow_control
    new_para.style = para.style
    if para.alignment:
        new_para.alignment = para.alignment
