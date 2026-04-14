from dash import dcc
from app import app


def find_component_by_id(component, target_id):
    if hasattr(component, "id") and component.id == target_id:
        return component

    children = getattr(component, "children", None)

    if children is None:
        return None

    if not isinstance(children, (list, tuple)):
        children = [children]

    for child in children:
        result = find_component_by_id(child, target_id)
        if result is not None:
            return result

    return None


def test_header_present():
    header = find_component_by_id(app.layout, "app-header")
    assert header is not None
    assert header.children == "Soul Foods Pink Morsel Sales Visualiser"


def test_visualisation_present():
    graph = find_component_by_id(app.layout, "sales-chart")
    assert graph is not None
    assert isinstance(graph, dcc.Graph)


def test_region_picker_present():
    region_picker = find_component_by_id(app.layout, "region-filter")
    assert region_picker is not None
    assert isinstance(region_picker, dcc.RadioItems)
    assert len(region_picker.options) == 5