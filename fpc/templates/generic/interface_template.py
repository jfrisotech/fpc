def get_interface_template(class_name: str) -> str:
    return f"""abstract class I{class_name} {{
  // TODO: Define interface methods
  Future<void> exampleMethod();
}}
"""
