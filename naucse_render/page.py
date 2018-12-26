from pathlib import Path, PosixPath
from urllib.parse import urlparse
import types

import jinja2

from .load import read_yaml
from .templates import environment, vars_functions
from .markdown import convert_markdown
from .notebook import convert_notebook


def to_list(value):
    if isinstance(value, str):
        return [value]
    return value


def to_html_list(value, inline=False):
    return [convert_markdown(item, inline=inline) for item in to_list(value)]


def lesson_url(lesson_name, *, page='index', _anchor=''):
    url = f'naucse:page?lesson={lesson_name}'
    if page != 'index':
        url += f'&page={page}'
    if _anchor:
        url += f'#{_anchor}'
    return url


def static_url(filename, *, _anchor=''):
    url = f'naucse:static?filename={filename}'
    if _anchor:
        url += f'#{_anchor}'
    return url


def rewrite_relative_url(url, slug):
    parsed = urlparse(url)
    if parsed.scheme or parsed.hostname:
        return url

    parts = list(PosixPath(parsed.path).parts)

    if parts and parts[0] == 'static':
        return static_url('/'.join(parts[1:]), _anchor=parsed.fragment)

    dotdots = 0
    while parts and parts[0] == '..':
        dotdots += 1
        del parts[0]

    if dotdots == 2:
        group, name = parts
        return lesson_url(f'{group}/{name}', _anchor=parsed.fragment)
    elif dotdots == 1:
        group, name = slug.split('/')
        [name] = parts
        return lesson_url(f'{group}/{name}', _anchor=parsed.fragment)

    if parsed.path.startswith('.'):
        raise ValueError(url)
    return url


def render_page(lesson_slug, page_slug, info, vars=None):
    print(f'Rendering page {lesson_slug} ({page_slug})')
    if vars is None:
        vars = {}

    lesson_directory = Path('lessons', lesson_slug)
    env = environment.overlay(loader=jinja2.FileSystemLoader('lessons'))

    page = {
        'title': info['title'],
        'attribution': to_html_list(info['attribution'], inline=True),
        'license': info['license'],
        'slug': page_slug,
        'vars': {**vars, **info.get('vars', {})},
    }
    if 'license_code' in info:
        page['license_code'] = info['license_code']

    page_name = page_slug + '.' + info['style']

    solutions = []

    def convert_page_url(url):
        return rewrite_relative_url(url, lesson_slug)

    def page_markdown(text, **kwargs):
        return convert_markdown(
            text,
            convert_url=convert_page_url,
            **kwargs,
        )

    path = lesson_directory / page_name

    if info.get('jinja', True):
        text = env.get_template(f'{lesson_slug}/{page_name}').render(
            lesson_url=lesson_url,
            subpage_url=lambda page: lesson_url(lesson_slug, page=page),
            static=static_url,
            lesson=types.SimpleNamespace(slug=lesson_slug),
            **{'$solutions': solutions, '$markdown': page_markdown},
            **vars_functions(vars),
        )
    else:
        text = path.read_text(encoding='utf-8')

    if info['style'] == 'md':
        text = page_markdown(text)
    elif info['style'] == 'ipynb':
        text = convert_notebook(text, convert_url=convert_page_url)
    else:
        raise ValueError(info['style'])

    page['content'] = text
    page['solutions'] = [{'content': s} for s in solutions]
    page['source_file'] = str(path)
    if 'css' in info:
        page['css'] = info['css']
    if 'latex' in info:
        page['modules'] = {'katex': '0.7.1'}
    return page