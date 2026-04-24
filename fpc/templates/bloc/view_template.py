def get_bloc_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../controllers/{class_name.lower()}_controller.dart';

class {class_name}View extends StatelessWidget {{
  const {class_name}View({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return BlocProvider(
      create: (context) => {class_name}Bloc(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('{class_name} View'),
        ),
        body: Center(
          child: BlocBuilder<{class_name}Bloc, {class_name}State>(
            builder: (context, state) {{
              if (state is {class_name}Loaded) {{
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
                context.read<{class_name}Bloc>().add({class_name}Increment());
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
