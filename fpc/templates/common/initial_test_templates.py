"""
Initial unit test templates for each architecture.
All tests follow a TODO skeleton pattern for quick project bootstrapping.
"""


def get_mvc_controller_test(project_name: str, is_modular: bool) -> str:
    base = f'package:{project_name}/app'
    prefix = f'{base}/modules/auth' if is_modular else base
    return f'''import 'package:flutter_test/flutter_test.dart';
import '{prefix}/controllers/auth_controller.dart';

void main() {{
  group('AuthController', () {{
    late AuthController sut;

    setUp(() {{
      // TODO: Pass required mock dependencies here
      sut = AuthController();
    }});

    test('initial state: isLoading should be false', () {{
      expect(sut, isNotNull);
      // TODO: Assert initial loading state
      // expect(sut.isLoading, isFalse);
    }});

    test('login - should set loading state and return success', () async {{
      // TODO: Mock AuthService.login(), call sut.login(), assert state
    }});

    test('logout - should clear user session', () async {{
      // TODO: Mock AuthService.logout(), call sut.logout(), assert state
    }});
  }});
}}
'''


def get_mvvm_viewmodel_test(project_name: str, is_modular: bool) -> str:
    base = f'package:{project_name}/app'
    prefix = f'{base}/modules/auth' if is_modular else base
    return f'''import 'package:flutter_test/flutter_test.dart';
import '{prefix}/viewmodels/auth_viewmodel.dart';

void main() {{
  group('AuthViewModel', () {{
    late AuthViewModel sut;

    setUp(() {{
      // TODO: Pass required mock dependencies here
      sut = AuthViewModel();
    }});

    test('initial state: isLoading should be false', () {{
      expect(sut, isNotNull);
      // TODO: expect(sut.isLoading, isFalse);
    }});

    test('login - should update state on success', () async {{
      // TODO: Mock service, call sut.login(), verify state changes
    }});

    test('login - should handle errors gracefully', () async {{
      // TODO: Mock service to throw, verify error state
    }});

    test('logout - should clear authenticated user', () async {{
      // TODO: Mock service, call sut.logout(), verify state
    }});
  }});
}}
'''


def get_clean_usecase_test(project_name: str, is_modular: bool) -> str:
    base = f'package:{project_name}/app'
    prefix = f'{base}/modules/auth' if is_modular else base
    return f'''import 'package:flutter_test/flutter_test.dart';
import 'package:dartz/dartz.dart';
import '{prefix}/domain/usecases/login_usecase.dart';
import '{prefix}/domain/repositories/auth_repository.dart';
import '{prefix}/domain/entities/user.dart';
import '{base}/core/error/failures.dart';

// TODO: Replace with a proper mock library like mocktail
class _FakeAuthRepository implements AuthRepository {{
  @override
  Future<Either<Failure, User>> login(String email, String password) async {{
    return Right(User(uid: '1', name: 'Test User', email: email));
  }}

  @override
  Future<Either<Failure, bool>> register(
      String name, String email, String password) async {{
    return const Right(true);
  }}

  @override
  Future<Either<Failure, void>> logout() async {{
    return const Right(null);
  }}
}}


void main() {{
  group('LoginUseCase', () {{
    late LoginUseCase sut;

    setUp(() {{
      sut = LoginUseCase(_FakeAuthRepository());
    }});

    test('should return User when repository succeeds', () async {{
      final result = await sut(
        LoginParams(email: 'test@test.com', password: 'pass123'),
      );
      expect(result.isRight(), isTrue);
      // TODO: also assert the returned User properties
    }});

    test('should return Failure when repository fails', () async {{
      // TODO: Use a _FailingAuthRepository that returns Left(ServerFailure(...))
      // and verify result.isLeft() == true
    }});
  }});
}}
'''


def get_clean_repository_impl_test(project_name: str, is_modular: bool) -> str:
    base = f'package:{project_name}/app'
    prefix = f'{base}/modules/auth' if is_modular else base
    return f'''import 'package:flutter_test/flutter_test.dart';
// TODO: import 'package:mocktail/mocktail.dart'; (add mocktail to dev_dependencies)
// import '{prefix}/data/repositories/auth_repository_impl.dart';
// import '{prefix}/data/datasources/auth_remote_data_source.dart';
// import '{base}/core/network/network_info.dart';

void main() {{
  group('AuthRepositoryImpl', () {{
    // TODO: Declare mocks
    // late MockAuthRemoteDataSource mockRemoteDataSource;
    // late MockNetworkInfo mockNetworkInfo;
    // late AuthRepositoryImpl sut;

    setUp(() {{
      // TODO: Initialize mocks and inject them into AuthRepositoryImpl
      // mockRemoteDataSource = MockAuthRemoteDataSource();
      // mockNetworkInfo = MockNetworkInfo();
      // sut = AuthRepositoryImpl(
      //   remoteDataSource: mockRemoteDataSource,
      //   networkInfo: mockNetworkInfo,
      // );
    }});

    group('login', () {{
      test('should return User when device is online and call succeeds',
          () async {{
        // TODO: Mock networkInfo.isConnected = true
        // TODO: Mock remoteDataSource.login() to return a UserModel
        // TODO: Call sut.login(), expect Right(user)
      }});

      test('should return NetworkFailure when device is offline', () async {{
        // TODO: Mock networkInfo.isConnected = false
        // TODO: Call sut.login(), expect Left(NetworkFailure)
      }});

      test('should return ServerFailure when remote call throws', () async {{
        // TODO: Mock networkInfo.isConnected = true
        // TODO: Mock remoteDataSource.login() to throw
        // TODO: Call sut.login(), expect Left(ServerFailure)
      }});
    }});

    group('register', () {{
      test('should return true on success', () async {{
        // TODO: Similar pattern
      }});
    }});

    group('logout', () {{
      test('should return void on success', () async {{
        // TODO: Similar pattern
      }});
    }});
  }});
}}
'''
