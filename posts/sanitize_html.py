import bleach

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union({
    'p', 'br', 'hr',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'b', 'em', 'i', 'u',
    'blockquote',
    'ul', 'ol', 'li',
    'pre', 'code',
    'img',
    'figure', 'figcaption',
    'iframe',
})


ALLOWED_ATTRIBUTES = {
    '*': ['class'],  # allow editor CSS classes
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height', 'title', 'loading'],
    'iframe': [
        'src', 'width', 'height',
        'allow', 'allowfullscreen', 'frameborder'
    ],
}

ALLOWED_PROTOCOLS = ['http', 'https']


def sanitize_html_content(content):
    cleaner = bleach.Cleaner(
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )

    cleaned = cleaner.clean(content)

    # Automatically fix links
    cleaned = bleach.linkify(
        cleaned,
        callbacks=bleach.linkifier.DEFAULT_CALLBACKS
    )

    return cleaned
