def get_http_client_content() -> str:
    return '''import 'package:http/http.dart' as http;
import '../../config/environment.dart';

class HttpClient {
  final http.Client client;
  final String baseUrl;

  HttpClient({http.Client? clientOverride, String? baseUrl})
      : client = clientOverride ?? http.Client(),
        baseUrl = baseUrl ?? Environment.apiBaseUrl;

  void close() {
    client.close();
  }
}
'''
