# FPC - Flutter Project CLI

A powerful, **context-aware** CLI tool for generating Flutter projects with customizable architecture patterns, dynamic imports, state management solutions, and a premium UX.

## 🌟 Features

- 🏗️ **Multiple Architecture Patterns**: MVC, MVVM, Clean Architecture.
- 🧠 **Context-Aware Scaffolding (`.fpc.json`)**: Remembers your project choices so you don't have to repeat flags!
- 🔄 **State Management Support**: Provider, BLoC, GetX, Riverpod, MobX.
- 📦 **Smart & Dynamic Code Generation**: Generates controllers, views, models, services, and interfaces with **dynamic imports** based on your database/HTTP preferences (e.g., auto-injects Hive or Firestore annotations).
- 🎯 **Headless Mode**: Fully automate project scaffolding without interactive prompts using CLI flags.
- 🚀 **Robust Dependency Injection**: Modifies `pubspec.yaml` natively using an AST parser (`ruamel.yaml`), preserving comments and indentation.
- 💅 **Premium Terminal UI**: Beautiful progress spinners, colored logs, and interactive menus powered by `Rich`.

---

## 💻 Installation

### Prerequisites

- Flutter SDK installed and in your `PATH`
- Python 3.7 or higher

### Fresh Install (From Source)

```bash
# Clone the repository
git clone <repository-url>
cd fpc

# Install the package globally in developer mode
python3 -m pip install -e .
```

After installation, the `fpc` command will be available globally in your terminal.

### Updating the CLI

When new updates are pushed to the repository, you can update your local FPC instance by pulling the latest changes and upgrading the dependencies:

```bash
cd /path/to/fpc
git pull origin main
python3 -m pip install --upgrade -e .
```

---

## 🛠 Usage

### 1. Create a New Project

**Interactive Mode:**
```bash
fpc create -n my_app -p /path/to/output
```
This launches a beautiful interactive UI that prompts you to select:
- Architecture pattern (MVC, MVVM, Clean Architecture)
- State management solution (Provider, BLoC, GetX, Riverpod, MobX, None)
- HTTP client (Dio, http, None)
- Local database (SQLite, Hive, Isar, ObjectBox, None)
- Backend-as-a-Service (Firebase, Supabase, Appwrite, None)

**Headless Mode (CI/CD / Automation):**
You can bypass the interactive menus by passing all arguments directly:
```bash
fpc create -n my_app -p ~/projects --arch mvc --state bloc --db hive --http dio --baas firebase
```
*Note: Run `fpc create --help` to see all available headless choices.*

> **What happens under the hood?**
> A hidden `.fpc.json` file is generated at the root of your newly created Flutter project. This acts as the project's brain!

---

### 2. Generate Context-Aware Files

Because of the `.fpc.json` configuration, running commands inside your project folder no longer requires explicitly mentioning the state management. The CLI knows your project!

```bash
# General syntax
fpc gen <type> <path>
```

#### Generate Controllers & Views

```bash
# Automatically pulls your default State Management from .fpc.json
fpc gen ctrl lib/controllers/auth_controller

fpc gen view lib/views/auth_view
```
*(If the project is BLoC, it generates `BlocBuilder`. If MobX, it wraps with `Observer`, etc.)*

**Overriding the default:**
You can still force a specific state management structure by using the `-s` or `--state` flag:
```bash
fpc gen view lib/features/settings/settings_view -s getx
```

#### Generate Smart Models
Models are generated dynamically based on your HTTP and DB choices. For instance, if your project uses `Dio` and `Hive`, generating a model will automatically inject `@HiveType`!

```bash
fpc gen model lib/models/product
```

#### Generate Services and Interfaces
```bash
fpc gen service lib/services/api_service
fpc gen intf lib/interfaces/repository
```

---

### 3. Add Generic Files (No State Management)

For adding base structures without specific templates:

```bash
fpc add -t controller -d lib/controllers -n auth
fpc add -t view -d lib/views -n home
```

---

## 📋 File Type Aliases

For writing commands faster, use abbreviations:
- `ctrl` → `controller`
- `intf` → `interface`

---

## 🏗️ Project Structure Expectations

The generated skeleton enforces clean boundaries:

```text
lib/
├── main.dart
├── config/              # Routes, Themes and BaaS initialization
│   ├── app_config.dart
│   ├── app_routes.dart
│   └── app_theme.dart
├── shared/              # Reusable design system / constants
│   └── theme/
├── controllers/         # (Depends on MVC vs MVVM vs Clean Arch)
├── views/
├── models/
└── ...
```

---

## 🤝 Contributing

Contributions are welcome! If you're planning to submit a PR to add a new State Management or Architecture option, please remember to update the corresponding template generator functions inside `templates/` and update `generator.py` to respect the newly available headless flags.

## 📄 License

This project is licensed under the MIT License.