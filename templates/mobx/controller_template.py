def get_mobx_controller_template(class_name: str) -> str:
    return f"""import 'package:mobx/mobx.dart';

part '{class_name.lower()}_controller.g.dart';

class {class_name}Controller = _{class_name}Controller with _${class_name}Controller;

abstract class _{class_name}Controller with Store {{
  @observable
  int value = 0;

  @action
  void increment() {{
    value++;
  }}
}}
"""
