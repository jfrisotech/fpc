# Guia de Python para Desenvolvedores Flutter & Dart

> Um manual prático e didático para entender o código Python do **FPC**, fazendo comparações diretas com o ecossistema Flutter/Dart.

---

## 1. Introdução: Por que Python no FPC?

Se você desenvolve em Flutter, está acostumado com **Dart**, tipagem estática e compilação AOT/JIT. O **FPC** foi escrito em **Python** porque Python é excelente para ferramentas de automação de sistema, manipulação de arquivos de texto/templates e execução rápida em qualquer máquina sem compilação prévia.

---

## 2. Tabela de Equivalência de Sintaxe (Dart vs. Python)

| Conceito | Dart | Python (FPC) | Explicação Didática |
|---|---|---|---|
| **Ponto e Vírgula** | Obrigatório (`int a = 10;`) | Não usa (`a = 10`) | Em Python, o fim da linha define o fim da instrução. |
| **Blocos de Código** | Chaves `{ ... }` | Indentação (4 espaços) | O alinhamento dos espaços define o que está dentro de `if`, `for` e funções. |
| **Variáveis Nulas** | `String? name;` | `name: Optional[str] = None` | Em Python importa-se `Optional` do módulo `typing`. |
| **Mapas / JSON** | `Map<String, dynamic>` | `dict` ou `Dict[str, Any]` | Dicionários em Python usam chaves (`{"key": "value"}`). |
| **Listas** | `List<String> list = [];` | `list: List[str] = []` | Listas dinâmicas delimitadas por colchetes `[]`. |
| **Interpolação de Texto** | `'Olá $name, valor: ${item.id}'` | `f'Olá {name}, valor: {item.id}'` | As strings precedidas de `f` (chamadas f-strings) avaliam expressões entre `{}`. |
| **Construtor** | `class Foo { Foo(); }` | `class Foo: def __init__(self):` | O método especial `__init__` é o construtor da classe. |
| **Referência de Instância** | `this.name = name;` | `self.name = name` | `self` é o primeiro parâmetro explícito de qualquer método de instância. |
| **Processos Externos** | `Process.run('flutter', args)` | `subprocess.run(['flutter', *args])` | Executa comandos no sistema operacional. |

---

## 3. Entendendo Classes e Métodos em Python

Em Dart, uma classe de serviço típica é:

```dart
class FlutterGenerator {
  final ProjectManager projectManager;

  FlutterGenerator({ProjectManager? manager})
      : projectManager = manager ?? ProjectManager();

  void generateFile(String type, String path) {
    print("Gerando $type em $path");
  }
}
```

No Python do FPC (`fpc/generators/generator.py`), isso é escrito assim:

```python
from typing import Optional
from fpc.project_manager import ProjectManager

class FlutterGenerator:
    """Documentação da classe (docstring)."""

    def __init__(self, manager: Optional[ProjectManager] = None):
        # 'self' representa 'this'
        self.project_manager = manager or ProjectManager()

    def generate_file(self, file_type: str, path: str) -> None:
        """Gera um arquivo."""
        print(f"Gerando {file_type} em {path}")
```

### O que significa `@staticmethod`?
Em Dart, você define métodos estáticos com `static void foo()`. Em Python, usamos o decorador `@staticmethod`:

```python
class TemplateManager:
    @staticmethod
    def get_template_content(file_type: str, name: str) -> str:
        # Não precisa de instância (não usa 'self')
        return "// Template"
```

---

## 4. Tipagem em Python (`typing`)

Python é uma linguagem de tipagem dinâmica, mas o FPC usa **Type Hints** modernos (equivalentes aos tipos do Dart) para clareza e segurança:

```python
from typing import Dict, List, Optional, Any, Set, Tuple

# Um mapa onde as chaves são strings e os valores podem ser qualquer coisa:
preferences: Dict[str, Any] = {
    'architecture': 'Clean Architecture',
    'state_management': 'Cubit'
}

# Um conjunto que impede duplicatas (como Set<String> no Dart):
deps_to_fetch: Set[str] = set()
deps_to_fetch.add('flutter_bloc')
deps_to_fetch.add('flutter_bloc') # Ignorado automaticamente
```

---

## 5. Manipulação de Arquivos e Strings Multilinha

No Dart, você usaria `''' ... '''` para strings com várias linhas. O Python funciona exatamente igual, usando aspas triplas `"""` ou `'''`:

```python
def get_cubit_controller_template(class_name: str) -> str:
    # F-string multilinha com interpolação
    return f"""import 'package:flutter_bloc/flutter_bloc.dart';

class {class_name}Cubit extends Cubit<{class_name}State> {{
  {class_name}Cubit() : super({class_name}Initial());
}}
"""
```

> **Atenção para chaves duplicadas `{{` e `}}`**:
> Quando uma string começa com `f"""`, o Python tentará interpretar tudo que estiver entre `{}`. Por isso, as chaves do código Dart que devem ser literais precisam ser duplicadas (`{{` e `}}`).

---

## 6. Como o FPC Executa Comandos (`subprocess.run`)

O equivalente ao `Process.run()` do Dart é o módulo `subprocess` do Python:

```python
import subprocess

# Executa 'flutter pub add flutter_bloc equatable' dentro da pasta do projeto
result = subprocess.run(
    ['flutter', 'pub', 'add', 'flutter_bloc', 'equatable'],
    cwd='/caminho/do/projeto',
    check=True # Lança exceção caso o comando retorne código de erro != 0
)
```

- `['flutter', 'pub', ...]`: Lista de argumentos separados (evita problemas com espaços em nomes de pastas).
- `cwd`: *Current Working Directory* (pasta onde o comando será executado).
- `check=True`: Garante que se o comando falhar, o Python interrompe a execução com erro claro.

---

## 7. Como os Testes Funcionam (`pytest`)

No Flutter, você roda testes com `flutter test`. No Python, o FPC usa o **`pytest`**:

- O pytest procura arquivos que começam com `test_` (ex: `tests/test_pubspec.py`).
- Usa a instrução `assert` em vez de `expect()`:

```python
# Dart:
# expect(args.contains('flutter_bloc'), isTrue);

# Python (pytest):
assert 'flutter_bloc' in args
```

### Rodando os testes:
No terminal da raiz do projeto:
```bash
pytest
```
Ou para ver os testes um a um:
```bash
pytest -v
```

