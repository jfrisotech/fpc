def get_entity_template(name: str) -> str:
    return f'''class {name}Entity {{
  final String id;
  
  const {name}Entity({{required this.id}});
}}
'''
