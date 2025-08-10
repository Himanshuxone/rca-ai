from sqlalchemy.inspection import inspect
from datetime import datetime, date
from decimal import Decimal

def model_to_dict_recursive(obj, visited=None):
    """Recursively convert SQLAlchemy model to dict (handles relationships, datetimes, decimals)."""
    if visited is None:
        visited = set()

    # Prevent infinite recursion on circular relationships
    if id(obj) in visited:
        return None
    visited.add(id(obj))

    # Primitive types stay as-is
    if obj is None or isinstance(obj, (int, str, float, bool)):
        return obj
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, list):
        return [model_to_dict_recursive(i, visited) for i in obj]

    # SQLAlchemy model
    if hasattr(obj, '__table__'):
        data = {}
        mapper = inspect(obj).mapper
        # Columns
        for column in mapper.column_attrs:
            value = getattr(obj, column.key)
            data[column.key] = model_to_dict_recursive(value, visited)
        # Relationships
        for rel in mapper.relationships:
            value = getattr(obj, rel.key)
            if value is not None:
                data[rel.key] = model_to_dict_recursive(value, visited)
        return data

    # Fallback
    return str(obj)
