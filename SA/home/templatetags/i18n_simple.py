"""
Template tag dịch đơn giản (dùng từ điển trong translations.py).

Dùng trong template:
    {% load i18n_simple %}
    {% t "Đăng xuất" %}

Tag đọc ngôn ngữ hiện tại từ request (đã được context processor gán vào
biến CURRENT_LANG), rồi tra từ điển trả về bản dịch tương ứng.
"""
from django import template
from django.utils.safestring import mark_safe
from ..translations import translate, FLAGS

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, text):
    """Dịch 'text' theo ngôn ngữ hiện tại (CURRENT_LANG trong context)."""
    lang = context.get('CURRENT_LANG', 'vi')
    return translate(text, lang)


@register.simple_tag
def flag(lang_code):
    """Trả về cờ SVG của ngôn ngữ. mark_safe để SVG render (không bị escape)."""
    return mark_safe(FLAGS.get(lang_code, ''))
