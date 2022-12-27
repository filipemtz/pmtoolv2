
from typing import Dict, List
from django.template import loader


def render_selector(options: List[Dict], 
                    name: str, 
                    id, 
                    onselect_event: str = '', 
                    selector_class='',
                    template='scrum/selector.html'
                    ) -> str:
    status_selector_html = loader.get_template(template).render({
        "name": name,
        "id": id,
        "options": options,
        'onselect_event': onselect_event,
        'selector_class': selector_class,
    })
    return status_selector_html


def render_image_selector(options: List[Dict], name: str, id, onselect_event: str = '') -> str:
    selector_html = loader.get_template('scrum/img_selector.html').render({
        "name": name,
        "id": id,
        "options": options,
        'onselect_event': onselect_event,
    })
    return selector_html
