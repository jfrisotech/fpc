def get_unit_test_template(class_name: str, file_path: str) -> str:
    return f'''import 'package:flutter_test/flutter_test.dart';
// import 'package:mockito/annotations.dart';
// import '{file_path}';

void main() {{
  group('{class_name} Unit Tests', () {{
    setUp(() {{
      // Setup for the tests
    }});

    test('should do something correctly', () {{
      // Arrange
      // Act
      // Assert
    }});
  }});
}}
'''

def get_widget_test_template(class_name: str, file_path: str) -> str:
    return f'''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
// import '{file_path}';

void main() {{
  group('{class_name} Widget Tests', () {{
    testWidgets('should render correctly', (WidgetTester tester) async {{
      // Build our app and trigger a frame.
      // await tester.pumpWidget(MaterialApp(home: {class_name}()));
      
      // expect(find.byType({class_name}), findsOneWidget);
    }});
  }});
}}
'''
