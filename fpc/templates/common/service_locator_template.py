def get_service_locator_content() -> str:
    return '''import 'package:get_it/get_it.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // Common services
  // sl.registerLazySingleton(() => ApiService());
  
  // Repositories
  // sl.registerLazySingleton<AuthRepository>(() => AuthRepositoryImpl(sl()));
  
  // UseCases
  // sl.registerLazySingleton(() => LoginUseCase(sl()));
  
  // State Management (Controllers/ViewModels/Blocs)
  // sl.registerFactory(() => AuthViewModel(sl()));
}
'''
