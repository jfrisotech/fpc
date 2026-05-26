"""
FPC Validation Criteria
Pure functions to validate generated Flutter project structures.
"""

import os
import re
from typing import List, Dict, Tuple

# ─────────────────────────────────────────────────────────────
# Data types
# ─────────────────────────────────────────────────────────────

class ValidationError:
    def __init__(self, severity: str, category: str, message: str, file: str = ""):
        self.severity = severity  # "CRITICAL" | "ERROR" | "WARNING"
        self.category = category
        self.message = message
        self.file = file

    def __repr__(self):
        return f"[{self.severity}][{self.category}] {self.message}" + (f" — {self.file}" if self.file else "")

    def to_dict(self):
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "file": self.file
        }

def error(category, msg, file=""):
    return ValidationError("ERROR", category, msg, file)

def critical(category, msg, file=""):
    return ValidationError("CRITICAL", category, msg, file)

def warning(category, msg, file=""):
    return ValidationError("WARNING", category, msg, file)


# ─────────────────────────────────────────────────────────────
# 1. Directory Structure Validation
# ─────────────────────────────────────────────────────────────

COMMON_DIRS = [
    "lib/app",
    "lib/app/config",
    "lib/app/shared",
    "lib/app/shared/theme",
    "lib/app/utils",
    "assets",
    "test",
]

COMMON_FILES = [
    "lib/main.dart",
    "lib/app/app_widget.dart",
    "lib/app/config/app_routes.dart",
    "lib/app/config/app_theme.dart",
    "lib/app/shared/theme/app_colors.dart",
    "lib/app/shared/theme/app_typography.dart",
    "lib/app/shared/theme/app_spacing.dart",
    "lib/app/shared/theme/app_dimensions.dart",
    "test/widget_test.dart",
    ".gitignore",
]

ARCH_DIRS = {
    "mvc": ["models", "views", "controllers", "services", "repositories", "widgets"],
    "mvvm": ["models", "views", "viewmodels", "services", "repositories", "widgets"],
    "clean": [
        "data", "data/datasources", "data/datasources/local", "data/datasources/remote",
        "data/models", "data/repositories",
        "domain", "domain/entities", "domain/repositories", "domain/usecases",
        "presentation", "presentation/pages", "presentation/widgets",
    ],
}

STATE_PRESENTATION_DIRS = {
    "bloc": "presentation/bloc",
    "mobx": "presentation/store",
    "getx": "presentation/controllers",
    "riverpod": "presentation/notifiers",
    "provider": "presentation/providers",
}

ARCH_FILES = {
    "mvc": {
        "models/user_model.dart",
        "controllers/auth_controller.dart",
        "services/auth_service.dart",
        "views/login_view.dart",
        "views/home_view.dart",
    },
    "mvvm": {
        "models/user_model.dart",
        "viewmodels/auth_viewmodel.dart",
        "services/auth_service.dart",
        "views/login_view.dart",
        "views/home_view.dart",
    },
    "clean": {
        "data/models/user_model.dart",
        "data/datasources/auth_remote_data_source.dart",
        "data/repositories/auth_repository_impl.dart",
        "domain/entities/user.dart",
        "domain/repositories/auth_repository.dart",
        "domain/usecases/login_usecase.dart",
        "domain/usecases/register_usecase.dart",
        "domain/usecases/logout_usecase.dart",
        "presentation/pages/login_page.dart",
    },
}

CLEAN_CORE_DIRS = [
    "core", "core/error", "core/network", "core/usecases", "core/util",
]

CLEAN_CORE_FILES = [
    "core/error/failures.dart",
    "core/network/network_info.dart",
    "core/usecases/usecase.dart",
]


def validate_directory_structure(project_path: str, arch: str, state: str, structure: str, db: str = "none") -> List[ValidationError]:
    errors = []

    def check_dir(rel_path):
        full = os.path.join(project_path, rel_path)
        if not os.path.isdir(full):
            errors.append(critical("STRUCTURE", f"Directory missing: {rel_path}"))

    def check_file(rel_path):
        full = os.path.join(project_path, rel_path)
        if not os.path.isfile(full):
            errors.append(critical("STRUCTURE", f"File missing: {rel_path}"))

    # Common dirs/files
    for d in COMMON_DIRS:
        check_dir(d)
    for f in COMMON_FILES:
        check_file(f)

    # Determine bases
    is_modular = structure == "modular"
    arch_base = "lib/app/modules/auth" if is_modular else "lib/app"
    home_base = "lib/app/modules/home" if is_modular else "lib/app"

    # Architecture-specific dirs
    arch_key = arch  # "mvc" | "mvvm" | "clean"
    if arch_key in ARCH_DIRS:
        for d in ARCH_DIRS[arch_key]:
            # Home module only needs views for now in baseline
            if arch_key in ["mvc", "mvvm"] and d == "views" and is_modular:
                check_dir(os.path.join(home_base, d))
                # For auth, views still has login_view
                check_dir(os.path.join(arch_base, d))
            else:
                check_dir(os.path.join(arch_base, d))

    # Clean Arch extra: core in lib/app
    if arch_key == "clean":
        for d in CLEAN_CORE_DIRS:
            check_dir(os.path.join("lib/app", d))
        for f in CLEAN_CORE_FILES:
            check_file(os.path.join("lib/app", f))

        # State-specific presentation dir
        state_dir = STATE_PRESENTATION_DIRS.get(state.lower())
        if state_dir:
            check_dir(os.path.join(arch_base, state_dir))

    # Architecture-specific files
    if arch_key in ARCH_FILES:
        for f in ARCH_FILES[arch_key]:
            # home_view and home_page go to home_base
            base = home_base if "home" in f else arch_base
            check_file(os.path.join(base, f))

    return errors


# ─────────────────────────────────────────────────────────────
# 2. Dart File Content Validation
# ─────────────────────────────────────────────────────────────

def validate_dart_file(file_path: str, project_name: str) -> List[ValidationError]:
    """Check for common Dart issues in generated files."""
    errors = []

    if not os.path.isfile(file_path):
        return errors

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(error("IO", f"Cannot read file: {e}", file_path))
        return errors

    rel = file_path

    # Check for placeholder strings that shouldn't be in production templates
    if "your_project" in content:
        errors.append(warning("IMPORT", f"'your_project' placeholder found — should use real package name", rel))

    if "package:your_project" in content:
        errors.append(error("IMPORT", f"Broken import: 'package:your_project' — must use '{project_name}'", rel))

    # Check for unclosed braces (rough heuristic)
    open_braces = content.count('{')
    close_braces = content.count('}')
    # Allow ±2 for template strings
    if abs(open_braces - close_braces) > 3:
        errors.append(error("SYNTAX", f"Possible unclosed braces: {open_braces} open vs {close_braces} close", rel))

    # Check for double blank lines at start (common template artifact)
    if content.startswith('\n\n\n'):
        errors.append(warning("FORMAT", "File starts with excessive blank lines", rel))

    return errors


def validate_main_dart(project_path: str, state: str, arch: str) -> List[ValidationError]:
    """Validate main.dart specific content based on preferences."""
    errors = []
    main_file = os.path.join(project_path, "lib/main.dart")

    if not os.path.isfile(main_file):
        errors.append(critical("CONTENT", "lib/main.dart missing", main_file))
        return errors

    with open(main_file, 'r') as f:
        content = f.read()

    # State management wrappers — only check what actually lives in main.dart
    # GetX: GetMaterialApp is in app_widget.dart (validated by validate_app_widget)
    # MobX: no top-level wrapper needed, uses Observer inside widgets
    expected = {
        "provider": ("MultiProvider", "package:provider/provider.dart"),
        "bloc": ("MultiBlocProvider", "package:flutter_bloc/flutter_bloc.dart"),
        "riverpod": ("ProviderScope", "package:flutter_riverpod/flutter_riverpod.dart"),
    }

    s = state.lower()
    if s in expected:
        wrapper, imp = expected[s]
        if wrapper not in content:
            errors.append(error("CONTENT", f"main.dart missing expected wrapper '{wrapper}' for {state}", main_file))
        if imp not in content:
            errors.append(error("IMPORT", f"main.dart missing import '{imp}' for {state}", main_file))

    # DI init
    if arch == "clean" or state.lower() in ["bloc", "mobx", "none"]:
        if "service_locator" not in content and "sl.init" not in content:
            errors.append(warning("DI", "main.dart might be missing service locator init", main_file))

    return errors


def validate_app_widget(project_path: str, state: str) -> List[ValidationError]:
    """Validate app_widget.dart."""
    errors = []
    f = os.path.join(project_path, "lib/app/app_widget.dart")
    if not os.path.isfile(f):
        errors.append(critical("CONTENT", "app_widget.dart missing", f))
        return errors

    with open(f, 'r') as fh:
        content = fh.read()

    if "class AppWidget" not in content:
        errors.append(critical("CONTENT", "AppWidget class not found in app_widget.dart", f))

    if state.lower() == "getx":
        if "GetMaterialApp" not in content:
            errors.append(error("CONTENT", "GetX selected but GetMaterialApp not used in AppWidget", f))
    else:
        if "GetMaterialApp" in content:
            errors.append(warning("CONTENT", "GetMaterialApp used but GetX was not selected", f))

    if "AppRoutes" not in content:
        errors.append(error("CONTENT", "AppRoutes not referenced in app_widget.dart", f))

    return errors


def validate_app_routes(project_path: str, arch: str, state: str, structure: str) -> List[ValidationError]:
    """Validate app_routes.dart imports and class definitions."""
    errors = []
    routes_file = os.path.join(project_path, "lib/app/config/app_routes.dart")
    if not os.path.isfile(routes_file):
        errors.append(critical("CONTENT", "app_routes.dart missing", routes_file))
        return errors

    with open(routes_file, 'r') as f:
        content = f.read()

    if "class AppRoutes" not in content:
        errors.append(critical("CONTENT", "AppRoutes class not found", routes_file))

    if "initialRoute" not in content:
        errors.append(error("CONTENT", "initialRoute not defined in AppRoutes", routes_file))

    # Check that imported files actually exist
    imports = re.findall(r"import '([^']+\.dart)'", content)
    for imp in imports:
        if imp.startswith("package:"):
            continue
        # Resolve relative to lib/app/config/
        base = os.path.join(project_path, "lib/app/config")
        resolved = os.path.normpath(os.path.join(base, imp))
        if not os.path.isfile(resolved):
            errors.append(error("IMPORT", f"app_routes.dart imports non-existent file: '{imp}' → {resolved}", routes_file))

    return errors


def validate_pubspec_deps(project_path: str, state: str, arch: str, http: str, db: str, baas: str) -> List[ValidationError]:
    """Validate pubspec.yaml has the right dependencies."""
    errors = []
    pubspec = os.path.join(project_path, "pubspec.yaml")
    if not os.path.isfile(pubspec):
        errors.append(critical("PUBSPEC", "pubspec.yaml missing", pubspec))
        return errors

    with open(pubspec, 'r') as f:
        content = f.read()

    expected_deps = {
        "provider": ["provider"],
        "bloc": ["flutter_bloc", "equatable"],
        "getx": ["get"],
        "riverpod": ["flutter_riverpod"],
        "mobx": ["mobx", "flutter_mobx"],
    }
    expected_dev_deps = {
        "mobx": ["mobx_codegen", "build_runner"],
        "hive": ["hive_generator", "build_runner"],
        "isar": ["isar_generator", "build_runner"],
        "objectbox": ["objectbox_generator", "build_runner"],
    }
    expected_db_deps = {
        "sqlite": ["sqflite", "path_provider"],
        "hive": ["hive", "hive_flutter"],
        "isar": ["isar", "isar_flutter_libs", "path_provider"],
        "objectbox": ["objectbox", "objectbox_flutter_libs", "path_provider"],
    }
    expected_baas_deps = {
        "firebase": ["firebase_core", "firebase_auth", "cloud_firestore"],
        "supabase": ["supabase_flutter"],
        "appwrite": ["appwrite"],
    }
    expected_arch_deps = {
        "clean": ["dartz", "get_it"],
    }

    def check_dep(pkg):
        if f"  {pkg}:" not in content:
            errors.append(error("PUBSPEC", f"Missing dependency: {pkg}", pubspec))

    s = state.lower()
    for dep in expected_deps.get(s, []):
        check_dep(dep)

    d = db.lower()
    for dep in expected_db_deps.get(d, []):
        check_dep(dep)

    b = baas.lower()
    for dep in expected_baas_deps.get(b, []):
        check_dep(dep)

    a = arch.lower()
    for dep in expected_arch_deps.get(a, []):
        check_dep(dep)

    # Dev deps
    for key in [s, d]:
        for dev_dep in expected_dev_deps.get(key, []):
            if f"  {dev_dep}:" not in content:
                errors.append(error("PUBSPEC", f"Missing dev dependency: {dev_dep}", pubspec))

    return errors


def validate_widget_test(project_path: str, project_name: str) -> List[ValidationError]:
    """Validate the widget_test.dart is correct."""
    errors = []
    test_file = os.path.join(project_path, "test/widget_test.dart")
    if not os.path.isfile(test_file):
        errors.append(critical("TEST", "test/widget_test.dart missing", test_file))
        return errors

    with open(test_file, 'r') as f:
        content = f.read()

    if "your_project" in content:
        errors.append(error("TEST", f"widget_test.dart uses placeholder 'your_project' instead of '{project_name}'", test_file))

    if f"package:{project_name}/" not in content:
        errors.append(error("TEST", f"widget_test.dart doesn't import from 'package:{project_name}'", test_file))

    if "AppWidget" not in content:
        errors.append(error("TEST", "widget_test.dart doesn't reference AppWidget", test_file))

    return errors


def validate_initial_unit_tests(project_path: str, arch: str, structure: str = "standard") -> List[ValidationError]:
    """Check that initial unit tests are created per architecture."""
    errors = []
    is_modular = structure == "modular"

    if arch == "mvc":
        expected = ["test/app/controllers/auth_controller_test.dart"]
    elif arch == "mvvm":
        expected = ["test/app/viewmodels/auth_viewmodel_test.dart"]
    elif arch == "clean":
        if is_modular:
            expected = [
                "test/app/modules/auth/domain/usecases/login_usecase_test.dart",
                "test/app/modules/auth/data/repositories/auth_repository_impl_test.dart",
            ]
        else:
            expected = [
                "test/app/domain/usecases/login_usecase_test.dart",
                "test/app/data/repositories/auth_repository_impl_test.dart",
            ]
    else:
        expected = []

    for test_file in expected:
        full = os.path.join(project_path, test_file)
        if not os.path.isfile(full):
            errors.append(error("TEST", f"Initial unit test missing: {test_file}", full))

    return errors


# ─────────────────────────────────────────────────────────────
# Master Validator
# ─────────────────────────────────────────────────────────────

def validate_project(project_path: str, project_name: str, arch: str, state: str,
                      structure: str, http: str, db: str, baas: str) -> List[ValidationError]:
    """Run all validations on a generated project."""
    all_errors: List[ValidationError] = []

    all_errors += validate_directory_structure(project_path, arch, state, structure, db)
    all_errors += validate_main_dart(project_path, state, arch)
    all_errors += validate_app_widget(project_path, state)
    all_errors += validate_app_routes(project_path, arch, state, structure)
    all_errors += validate_pubspec_deps(project_path, state, arch, http, db, baas)
    all_errors += validate_widget_test(project_path, project_name)
    all_errors += validate_initial_unit_tests(project_path, arch, structure)

    # Validate all .dart files for common issues
    for root, dirs, files in os.walk(os.path.join(project_path, "lib")):
        for fname in files:
            if fname.endswith(".dart"):
                fpath = os.path.join(root, fname)
                all_errors += validate_dart_file(fpath, project_name)

    for root, dirs, files in os.walk(os.path.join(project_path, "test")):
        for fname in files:
            if fname.endswith(".dart"):
                fpath = os.path.join(root, fname)
                all_errors += validate_dart_file(fpath, project_name)

    return all_errors
