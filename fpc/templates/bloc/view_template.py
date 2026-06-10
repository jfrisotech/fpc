def get_bloc_view_template(class_name: str, base_name: str = None) -> str:
    from fpc.core.utils import to_pascal_case, to_snake_case
    b_name = base_name or (class_name[:-4] if class_name.endswith('View') else class_name)
    bloc_class = f"{to_pascal_case(b_name)}Bloc"
    state_class = f"{to_pascal_case(b_name)}State"
    loaded_state = f"{to_pascal_case(b_name)}Loaded"
    increment_event = f"{to_pascal_case(b_name)}Increment"
    controller_file = f"{to_snake_case(b_name)}_controller.dart"
    
    view_class = class_name
    if not view_class.endswith('View'):
        view_class += 'View'

    return f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../controllers/{controller_file}';

class {view_class} extends StatelessWidget {{
  const {view_class}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return BlocProvider(
      create: (context) => {bloc_class}(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('{view_class}'),
        ),
        body: Center(
          child: BlocBuilder<{bloc_class}, {state_class}>(
            builder: (context, state) {{
              if (state is {loaded_state}) {{
                return Text('Value: ${{state.value}}');
              }}
              return const Text('Initial State');
            }},
          ),
        ),
        floatingActionButton: Builder(
          builder: (context) {{
            return FloatingActionButton(
              onPressed: () {{
                context.read<{bloc_class}>().add({increment_event}());
              }},
              child: const Icon(Icons.add),
            );
          }},
        ),
      ),
    );
  }}
}}
"""
