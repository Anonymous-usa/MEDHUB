# medhub_api.api.DefaultApi

## Load the API package
```dart
import 'package:medhub_api/api.dart';
```

All URIs are relative to *https://api.medhub.tj*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apiV1InstitutionsGet**](DefaultApi.md#apiv1institutionsget) | **GET** /api/v1/institutions/ | Список учреждений (публичный)
[**apiV1InstitutionsIdGet**](DefaultApi.md#apiv1institutionsidget) | **GET** /api/v1/institutions/{id}/ | Детальная информация об учреждении
[**apiV1PatientAppointmentsGet**](DefaultApi.md#apiv1patientappointmentsget) | **GET** /api/v1/patient/appointments/ | Список записей пациента
[**apiV1PatientAppointmentsPost**](DefaultApi.md#apiv1patientappointmentspost) | **POST** /api/v1/patient/appointments/ | Новая запись на приём
[**apiV1PatientReviewsGet**](DefaultApi.md#apiv1patientreviewsget) | **GET** /api/v1/patient/reviews/ | Список отзывов текущего пациента
[**apiV1PatientReviewsPost**](DefaultApi.md#apiv1patientreviewspost) | **POST** /api/v1/patient/reviews/ | Оставить отзыв
[**apiV1ProfileGet**](DefaultApi.md#apiv1profileget) | **GET** /api/v1/profile/ | Профиль текущего пользователя
[**apiV1ProfilePut**](DefaultApi.md#apiv1profileput) | **PUT** /api/v1/profile/ | Обновить профиль текущего пользователя
[**apiV1RegisterPatientPost**](DefaultApi.md#apiv1registerpatientpost) | **POST** /api/v1/register/patient/ | Регистрация нового пациента
[**apiV1TokenPost**](DefaultApi.md#apiv1tokenpost) | **POST** /api/v1/token/ | Получить пару JWT-токенов
[**apiV1TokenRefreshPost**](DefaultApi.md#apiv1tokenrefreshpost) | **POST** /api/v1/token/refresh/ | Обновить access-токен по refresh-токену


# **apiV1InstitutionsGet**
> BuiltList<InstitutionPublic> apiV1InstitutionsGet()

Список учреждений (публичный)

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();

try {
    final response = api.apiV1InstitutionsGet();
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1InstitutionsGet: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BuiltList&lt;InstitutionPublic&gt;**](InstitutionPublic.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1InstitutionsIdGet**
> InstitutionPublic apiV1InstitutionsIdGet(id)

Детальная информация об учреждении

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final int id = 56; // int | ID учреждения

try {
    final response = api.apiV1InstitutionsIdGet(id);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1InstitutionsIdGet: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| ID учреждения | 

### Return type

[**InstitutionPublic**](InstitutionPublic.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1PatientAppointmentsGet**
> BuiltList<AppointmentRequestDetail> apiV1PatientAppointmentsGet()

Список записей пациента

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();

try {
    final response = api.apiV1PatientAppointmentsGet();
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1PatientAppointmentsGet: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BuiltList&lt;AppointmentRequestDetail&gt;**](AppointmentRequestDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1PatientAppointmentsPost**
> AppointmentRequestCreate apiV1PatientAppointmentsPost(appointmentRequestCreate)

Новая запись на приём

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final AppointmentRequestCreate appointmentRequestCreate = ; // AppointmentRequestCreate | 

try {
    final response = api.apiV1PatientAppointmentsPost(appointmentRequestCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1PatientAppointmentsPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **appointmentRequestCreate** | [**AppointmentRequestCreate**](AppointmentRequestCreate.md)|  | 

### Return type

[**AppointmentRequestCreate**](AppointmentRequestCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1PatientReviewsGet**
> BuiltList<ReviewDetail> apiV1PatientReviewsGet()

Список отзывов текущего пациента

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();

try {
    final response = api.apiV1PatientReviewsGet();
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1PatientReviewsGet: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BuiltList&lt;ReviewDetail&gt;**](ReviewDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1PatientReviewsPost**
> ReviewCreate apiV1PatientReviewsPost(reviewCreate)

Оставить отзыв

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final ReviewCreate reviewCreate = ; // ReviewCreate | 

try {
    final response = api.apiV1PatientReviewsPost(reviewCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1PatientReviewsPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reviewCreate** | [**ReviewCreate**](ReviewCreate.md)|  | 

### Return type

[**ReviewCreate**](ReviewCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1ProfileGet**
> Profile apiV1ProfileGet()

Профиль текущего пользователя

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();

try {
    final response = api.apiV1ProfileGet();
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1ProfileGet: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Profile**](Profile.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1ProfilePut**
> Profile apiV1ProfilePut(profile)

Обновить профиль текущего пользователя

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final Profile profile = ; // Profile | 

try {
    final response = api.apiV1ProfilePut(profile);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1ProfilePut: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile** | [**Profile**](Profile.md)|  | 

### Return type

[**Profile**](Profile.md)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1RegisterPatientPost**
> PatientRegister apiV1RegisterPatientPost(patientRegister)

Регистрация нового пациента

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final PatientRegister patientRegister = ; // PatientRegister | 

try {
    final response = api.apiV1RegisterPatientPost(patientRegister);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1RegisterPatientPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **patientRegister** | [**PatientRegister**](PatientRegister.md)|  | 

### Return type

[**PatientRegister**](PatientRegister.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1TokenPost**
> TokenObtain apiV1TokenPost(tokenObtain)

Получить пару JWT-токенов

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final TokenObtain tokenObtain = ; // TokenObtain | 

try {
    final response = api.apiV1TokenPost(tokenObtain);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1TokenPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tokenObtain** | [**TokenObtain**](TokenObtain.md)|  | 

### Return type

[**TokenObtain**](TokenObtain.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apiV1TokenRefreshPost**
> TokenRefreshResponse apiV1TokenRefreshPost(tokenRefreshRequest)

Обновить access-токен по refresh-токену

### Example
```dart
import 'package:medhub_api/api.dart';

final api = MedhubApi().getDefaultApi();
final TokenRefreshRequest tokenRefreshRequest = ; // TokenRefreshRequest | 

try {
    final response = api.apiV1TokenRefreshPost(tokenRefreshRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling DefaultApi->apiV1TokenRefreshPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tokenRefreshRequest** | [**TokenRefreshRequest**](TokenRefreshRequest.md)|  | 

### Return type

[**TokenRefreshResponse**](TokenRefreshResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

