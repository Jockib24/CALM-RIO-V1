from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def responsive_image(base_path, alt="", css_class="", loading="lazy", sizes=None):
    """
    Generate a <picture> element with WebP source and JPEG/PNG fallback.

    Usage:
        {% responsive_image "images/properties/royan-appartement/face-exterior-yellow-01.webp" alt="Exterior" %}

    Assumes files exist as:
        - {base_path} (WebP)
        - {base_path}.jpg or .png (fallback)

    Args:
        base_path: Path relative to static root, WITH extension (e.g. "images/prop/photo.webp")
        alt: Alt text
        css_class: CSS classes for <img>
        loading: "lazy" | "eager" | "auto"
        sizes: sizes attribute for responsive images (e.g. "(max-width: 768px) 100vw, 50vw")
    """
    # Determine fallback extension
    if base_path.endswith(".webp"):
        fallback_path = base_path[:-5] + ".jpg"
        # Check if .png exists instead
        from django.contrib.staticfiles.finders import find

        if not find(fallback_path):
            fallback_path = base_path[:-5] + ".png"
    elif base_path.endswith(".avif"):
        fallback_path = base_path[:-5] + ".jpg"
        from django.contrib.staticfiles.finders import find

        if not find(fallback_path):
            fallback_path = base_path[:-5] + ".png"
    else:
        # Already JPEG/PNG - no WebP source
        webp_path = base_path
        fallback_path = base_path
        webp_url = static(webp_path)
        fallback_url = static(fallback_path)
        sizes_attr = f' sizes="{sizes}"' if sizes else ""
        return f'<img src="{fallback_url}" alt="{alt}" class="{css_class}" loading="{loading}"{sizes_attr}>'

    webp_url = static(base_path)
    fallback_url = static(fallback_path)

    sizes_attr = f' sizes="{sizes}"' if sizes else ""

    return f'''<picture>
    <source type="image/webp" srcset="{webp_url}"{sizes_attr}>
    <img src="{fallback_url}" alt="{alt}" class="{css_class}" loading="{loading}"{sizes_attr}>
</picture>'''


@register.simple_tag
def hero_image(base_path, alt="", css_class=""):
    """Hero image - eager loading, no lazy."""
    return responsive_image(
        base_path, alt=alt, css_class=css_class, loading="eager", sizes="100vw"
    )


@register.simple_tag
def gallery_image(base_path, alt="", css_class=""):
    """Gallery image - lazy loading."""
    return responsive_image(base_path, alt=alt, css_class=css_class, loading="lazy")


@register.simple_tag
def property_card_image(base_path, alt="", css_class=""):
    """Property card image - lazy loading with sizes."""
    return responsive_image(
        base_path,
        alt=alt,
        css_class=css_class,
        loading="lazy",
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw",
    )
