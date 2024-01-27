import batFramework as bf


def apply_common(w:bf.Widget):
    w.set_color(bf.color.DARK_BLUE).set_outline_width(3).set_border_radius(4).set_padding((4,6))

def style(entity):
    try:
        entity.set_padding((8,8))
        if not isinstance(entity,bf.Indicator) : 
            entity.set_color(bf.color.DARK_BLUE)
            entity.set_outline_color(bf.color.WASHED_BLUE)
            entity.set_border_radius(8)
            entity.set_outline_width(2)
        else:
            entity.set_outline_color(bf.color.DARK_BLUE)
        if isinstance(entity,bf.Label):
            entity.set_text_color(bf.color.CLOUD_WHITE)
            entity.set_color(bf.color.WASHED_BLUE)
            entity.set_border_radius(4)
            
        return entity
    except AttributeError:
        return entity