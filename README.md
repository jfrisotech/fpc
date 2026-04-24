# FPC - Flutter Project CLI 🚀

A powerful, **context-aware** CLI tool designed to professionalize Flutter development. FPC generates production-ready codebases with customizable architecture patterns, automatic testing structures, and a premium developer experience.

---

## 🌟 Why FPC?

Most CLI tools generate generic code. FPC is different because it is **Context-Aware**:
- **It remembers your stack**: Through a `.fpc.json` file, FPC knows if your project uses BLoC, Riverpod, or GetX. You don't need to pass flags every time you generate a file.
- **Dynamic Boilerplate**: If you use Hive, your generated models automatically include `@HiveType`. If you use Clean Architecture, your repositories automatically include `NetworkInfo` and `Either` error handling.
- **Automatic Testing**: Every file generated in `lib/` automatically creates its twin in `test/`, following best practices for Unit and Widget testing.

---

## 💻 Installation

### Prerequisites
- [Flutter SDK](https://docs.flutter.dev/get-started/install) installed and in your `PATH`.
- [Python 3.8+](https://www.python.org/) installed.

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd fpc

# Install globally in editable mode (recommended for developers)
python3 -m pip install -e .
```

---

## 🛠️ Usage Guide

### 1. Health Check
Before starting, ensure your environment is ready:
```bash
fpc doctor
```
The "Doctor" will check if Flutter, Git, and Python are correctly configured and if you are inside an FPC project.

### 2. Creating or Initializing a Project
- **New Project:** `fpc create -n my_app` (Starts an interactive wizard).
- **Existing Project:** `fpc init` (Adds FPC intelligence to any Flutter project).

### 3. Smart Code Generation
FPC uses the project configuration to generate the right code for your specific stack.

| Command | Description |
|---------|-------------|
| `fpc gen feature <name>` | Scaffolds a complete module (Data, Domain, Presentation) |
| `fpc gen view <path>` | Creates a Widget (Stateless/Stateful/Observer/Consumer) |
| `fpc gen ctrl <path>` | Creates a Controller or ViewModel with DI support |
| `fpc gen model <path>` | Creates a Model with JSON serialization and DB annotations |
| `fpc gen service <path>`| Creates a DataSource (Local or Remote) |

### 4. Workflow Shortcuts (Aliases)
Save time with built-in aliases for common Flutter operations:
- `fpc get` → `flutter pub get`
- `fpc build` → Runs `build_runner build`
- `fpc watch` → Runs `build_runner watch`
- `fpc clean` → `flutter clean`
- `fpc upgrade` → `flutter pub upgrade`

---

## 🏗️ Supported Architectures

### Clean Architecture (Enterprise)
Focuses on separation of concerns and testability.
- **Data Layer**: DataSources (Local/Remote), Models, and Repository Implementations.
- **Domain Layer**: Entities, Repository Contracts, and UseCases.
- **Presentation Layer**: Pages, Widgets, and State Management (BLoC/Provider/etc).

### MVVM (Model-View-ViewModel)
Ideal for reactive applications.
- Includes a dedicated `repositories` layer and constructor-based DI for ViewModels.

### MVC (Model-View-Controller)
Classic and straightforward.
- Updated with Repository patterns to avoid fat controllers.

---

## 🧪 Testing Strategy

FPC enforces a "Test-First" culture.
- **Location**: All tests are generated in the `test/` directory, mirroring the `lib/` structure.
- **Unit Tests**: Generated for logic classes (Controllers, Services, Repositories).
- **Widget Tests**: Generated for UI classes (Views).
- **Mocking**: Templates include placeholders for `mockito` or `mocktail`.

---

## 🛠️ Developer Guide (Internal Architecture)

FPC is built with a **Service-Oriented Architecture** in Python:

- **`fpc/cli.py`**: The entry point. Handles command-line arguments.
- **`fpc/config_manager.py`**: Manages the `.fpc.json` state.
- **`fpc/template_manager.py`**: The "registry" that maps architectures and state managements to specific code templates.
- **`fpc/project_manager.py`**: Orchestrates shell commands and Flutter SDK interactions.
- **`fpc/generators/`**: Contains the logic for building folder structures and updating the `pubspec.yaml`.

### How to add a new State Management or Template?
1. **Create the Template**: Add a new python file in `fpc/templates/common/` (or a specific architecture folder) with a function `get_yourtype_template(name)`.
2. **Register in TemplateManager**: Open `fpc/template_manager.py` and add your new template to the mapping logic in `get_template_content`.
3. **Update CLI**: If it's a new state management solution, add it to the `choices` in `fpc/cli.py`.

### Running Internal Tests
To ensure you haven't broken the CLI logic:
```bash
pip install pytest
pytest tests/
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.