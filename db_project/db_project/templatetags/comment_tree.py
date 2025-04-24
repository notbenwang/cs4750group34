from django import template

register = template.Library()

@register.inclusion_tag("posts/_comment_node.html", takes_context=True)
def render_comment(context, comment, depth=0):
    """
    Recursive inclusion tag that renders a comment *and* all its descendants.
    """
    return {
        "comment": comment,
        "depth": depth,
        "request": context["request"],        # forward original request for permission checks
    }
