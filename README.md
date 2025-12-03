# FPC - Flutter Project CLI

A powerful CLI tool for generating Flutter projects with customizable architecture patterns and state management solutions.

## Features

- 🏗️ **Multiple Architecture Patterns**: MVC, MVVM, Clean Architecture
- 🔄 **State Management Support**: Provider, BLoC, GetX, Riverpod, MobX
- 📦 **Smart Code Generation**: Generate controllers, views, models, services, and interfaces
- 🎯 **Convention Enforcement**: Automatic snake_case for files, PascalCase for classes
- 🚀 **Latest Dependencies**: Always fetches the latest package versions

## Installation

### Prerequisites

- Flutter SDK installed and in your PATH
- Python 3.7 or higher

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd fpc

# Install the package
pip install -e .
```

After installation, the `fpc` command will be available globally.

## Usage

### Create a New Project

```bash
fpc create -n my_app -p /path/to/output
```

This will prompt you to select:
- Architecture pattern (MVC, MVVM, Clean Architecture)
- State management solution (Provider, BLoC, GetX, Riverpod, MobX, None)
- HTTP client (Dio, http, Retrofit, None)
- Local database (SQLite, Hive, Isar, ObjectBox, None)
- Backend-as-a-Service (Firebase, Supabase, Appwrite, None)

### Generate Files with State Management

The `gen` command allows you to generate files with specific state management configurations:

```bash
fpc gen <type> <state_management> <path>
```

#### Generate Controllers

```bash
# MobX controller
fpc gen ctrl mobx lib/controllers/auth_controller

# Provider controller
fpc gen ctrl provider lib/controllers/user_controller

# BLoC controller
fpc gen ctrl bloc lib/controllers/home_controller

# GetX controller
fpc gen ctrl getx lib/controllers/settings_controller

# Riverpod controller
fpc gen ctrl riverpod lib/controllers/profile_controller
```

#### Generate Views

Views are generated with the appropriate state management widgets:

```bash
# MobX view (with Observer)
fpc gen view mobx lib/views/auth_view

# Provider view (with Consumer)
fpc gen view provider lib/views/user_view

# BLoC view (with BlocBuilder)
fpc gen view bloc lib/views/home_view

# GetX view (with GetView)
fpc gen view getx lib/views/settings_view

# Riverpod view (with ConsumerWidget)
fpc gen view riverpod lib/views/profile_view
```

#### Generate Other Files

```bash
# Model
fpc gen model none lib/models/user

# Service
fpc gen service none lib/services/api_service

# Interface (abstract class)
fpc gen intf none lib/interfaces/repository
```

### Add Files to Existing Project

For adding generic files without state management specifics:

```bash
fpc add -t controller -d lib/controllers -n auth
fpc add -t view -d lib/views -n home
fpc add -t model -d lib/models -n user
fpc add -t service -d lib/services -n api
```

## File Type Aliases

- `ctrl` → `controller`
- `intf` → `interface`

## Examples

### Complete workflow example

```bash
# 1. Create a new project
fpc create -n my_app -p ~/projects

# 2. Generate a MobX controller
fpc gen ctrl mobx lib/features/auth/auth_controller

# 3. Generate a matching MobX view
fpc gen view mobx lib/features/auth/auth_view

# 4. Generate a model
fpc gen model none lib/models/user

# 5. Generate an interface
fpc gen intf none lib/interfaces/auth_repository
```

## Project Structure

The generated project will have a clean, organized structure:

```
lib/
├── main.dart
├── config/
│   ├── app_config.dart
│   ├── app_routes.dart
│   └── app_theme.dart
├── controllers/      # MVC
├── viewmodels/       # MVVM
├── views/
├── models/
├── services/
└── ...
```

## State Management Templates

Each state management solution comes with its specific boilerplate:

- **MobX**: Store classes with `@observable` and `@action`
- **Provider**: `ChangeNotifier` classes
- **BLoC**: Bloc classes with events and states
- **GetX**: `GetxController` with reactive variables
- **Riverpod**: `StateNotifier` with providers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.