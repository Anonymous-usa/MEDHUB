//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_import

import 'package:one_of_serializer/any_of_serializer.dart';
import 'package:one_of_serializer/one_of_serializer.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/serializer.dart';
import 'package:built_value/standard_json_plugin.dart';
import 'package:built_value/iso_8601_date_time_serializer.dart';
import 'package:medhub_api/src/date_serializer.dart';
import 'package:medhub_api/src/model/date.dart';

import 'package:medhub_api/src/model/appointment_request_create.dart';
import 'package:medhub_api/src/model/appointment_request_detail.dart';
import 'package:medhub_api/src/model/department.dart';
import 'package:medhub_api/src/model/institution_public.dart';
import 'package:medhub_api/src/model/patient_register.dart';
import 'package:medhub_api/src/model/profile.dart';
import 'package:medhub_api/src/model/review_create.dart';
import 'package:medhub_api/src/model/review_detail.dart';
import 'package:medhub_api/src/model/token_obtain.dart';
import 'package:medhub_api/src/model/token_refresh_request.dart';
import 'package:medhub_api/src/model/token_refresh_response.dart';

part 'serializers.g.dart';

@SerializersFor([
  AppointmentRequestCreate,
  AppointmentRequestDetail,
  Department,
  InstitutionPublic,
  PatientRegister,
  Profile,
  ReviewCreate,
  ReviewDetail,
  TokenObtain,
  TokenRefreshRequest,
  TokenRefreshResponse,
])
Serializers serializers = (_$serializers.toBuilder()
      ..addBuilderFactory(
        const FullType(BuiltList, [FullType(InstitutionPublic)]),
        () => ListBuilder<InstitutionPublic>(),
      )
      ..addBuilderFactory(
        const FullType(BuiltList, [FullType(AppointmentRequestDetail)]),
        () => ListBuilder<AppointmentRequestDetail>(),
      )
      ..addBuilderFactory(
        const FullType(BuiltList, [FullType(ReviewDetail)]),
        () => ListBuilder<ReviewDetail>(),
      )
      ..add(const OneOfSerializer())
      ..add(const AnyOfSerializer())
      ..add(const DateSerializer())
      ..add(Iso8601DateTimeSerializer())
    ).build();

Serializers standardSerializers =
    (serializers.toBuilder()..addPlugin(StandardJsonPlugin())).build();
