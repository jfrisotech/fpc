def get_bloc_controller_template(class_name: str) -> str:
    return f"""import 'package:flutter_bloc/flutter_bloc.dart';

// Events
abstract class {class_name}Event {{}}

class {class_name}Increment extends {class_name}Event {{}}

// States
abstract class {class_name}State {{}}

class {class_name}Initial extends {class_name}State {{}}

class {class_name}Loaded extends {class_name}State {{
  final int value;
  {class_name}Loaded(this.value);
}}

// Bloc
class {class_name}Bloc extends Bloc<{class_name}Event, {class_name}State> {{
  {class_name}Bloc() : super({class_name}Initial()) {{
    on<{class_name}Increment>((event, emit) {{
      // TODO: Implement logic
      emit({class_name}Loaded(1));
    }});
  }}
}}
"""
