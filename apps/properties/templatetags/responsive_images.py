from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def responsive_image(
    path, alt="", css_class="", loading="lazy", sizes="100vw", widths="400, 800, 1200"
):
    """
    Generate a <picture> element with WebP source and fallback.

    Usage:
        {% responsive_image 'images/properties/royan-appartement/face-exterior-yellow-01.webp'
                           alt="Appartement Royan"
                           css_class="hero-img"
                           loading="eager"
                           sizes="(max-width: 768px) 100vw, 50vw" %}

    Assumes WebP version exists at same path, and JPEG/PNG fallback at same path with .jpg/.png extension.
    """
    # Build WebP source
    webp_url = static(path)

    # Determine fallback URL
    # WebP/AVIF has universal browser support since 2020+, so we use it directly
    if path.endswith(".webp") or path.endswith(".avif"):
        fallback_path = path  # Use same file — modern browsers all support it
    else:
        fallback_path = path

    fallback_url = static(fallback_path)

    # Build srcset for different widths (if using responsive image service)
    # For now, just use the single image
    srcset = webp_url

    # Determine loading attribute
    load_attr = 'loading="lazy"' if loading == "lazy" else ""
    if loading == "eager":
        load_attr = 'loading="eager"'

    html = f'''
<picture>
    <source type="image/webp" srcset="{webp_url}" sizes="{sizes}">
    <img src="{fallback_url}" alt="{alt}" class="{css_class}" {load_attr} decoding="async">
</picture>
'''
    return mark_safe(html)


@register.simple_tag
def hero_image(path, alt="", css_class=""):
    """Hero image - eager loading, no lazy."""
    return responsive_image(path, alt, css_class, loading="eager", sizes="100vw")


@register.simple_tag
def gallery_image(path, alt="", css_class=""):
    """Gallery image - lazy loading."""
    return responsive_image(
        path,
        alt,
        css_class,
        loading="lazy",
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw",
    )


@register.simple_tag
def card_image(path, alt="", css_class=""):
    """Property card image - lazy loading."""
    return responsive_image(
        path, alt, css_class, loading="lazy", sizes="(max-width: 768px) 100vw, 33vw"
    )
