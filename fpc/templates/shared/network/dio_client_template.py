def get_dio_client_content() -> str:
    return '''import 'package:dio/dio.dart';
import '../../config/environment.dart';
import '../storage/secure_storage_service.dart';

class DioClient {
  final Dio dio;
  final SecureStorageService? secureStorage;

  DioClient({
    Dio? dioOverride,
    String? baseUrl,
    this.secureStorage,
  }) : dio = dioOverride ??
            Dio(
              BaseOptions(
                baseUrl: baseUrl ?? Environment.apiBaseUrl,
                connectTimeout: const Duration(seconds: 15),
                receiveTimeout: const Duration(seconds: 15),
                sendTimeout: const Duration(seconds: 15),
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                },
              ),
            ) {
    if (secureStorage != null) {
      dio.interceptors.add(
        InterceptorsWrapper(
          onRequest: (options, handler) async {
            final token = await secureStorage!.getToken();
            if (token != null && token.isNotEmpty) {
              options.headers['Authorization'] = 'Bearer $token';
            }
            return handler.next(options);
          },
        ),
      );
    }

    if (Environment.enableLogging) {
      dio.interceptors.add(
        LogInterceptor(
          request: true,
          requestHeader: true,
          requestBody: true,
          responseHeader: false,
          responseBody: true,
          error: true,
        ),
      );
    }
  }
}
'''
