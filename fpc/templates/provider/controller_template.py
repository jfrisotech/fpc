def get_provider_controller_template(class_name: str) -> str:
    name = class_name
    if not name.endswith('Controller'):
        name += 'Controller'
    return f"""import 'package:flutter/foundation.dart';

class {name} extends ChangeNotifier {{
  int _value = 0;
  int get value => _value;

  void increment() {{
    _value++;
    notifyListeners();
  }}
}}
"""
