//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'appointment_request_detail.g.dart';

/// AppointmentRequestDetail
///
/// Properties:
/// * [id] 
/// * [doctorPhone] 
/// * [patientPhone] 
/// * [note] 
/// * [status] 
/// * [createdAt] 
@BuiltValue()
abstract class AppointmentRequestDetail implements Built<AppointmentRequestDetail, AppointmentRequestDetailBuilder> {
  @BuiltValueField(wireName: r'id')
  int get id;

  @BuiltValueField(wireName: r'doctor_phone')
  String get doctorPhone;

  @BuiltValueField(wireName: r'patient_phone')
  String get patientPhone;

  @BuiltValueField(wireName: r'note')
  String? get note;

  @BuiltValueField(wireName: r'status')
  AppointmentRequestDetailStatusEnum get status;
  // enum statusEnum {  pending,  accepted,  rejected,  };

  @BuiltValueField(wireName: r'created_at')
  DateTime get createdAt;

  AppointmentRequestDetail._();

  factory AppointmentRequestDetail([void updates(AppointmentRequestDetailBuilder b)]) = _$AppointmentRequestDetail;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(AppointmentRequestDetailBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<AppointmentRequestDetail> get serializer => _$AppointmentRequestDetailSerializer();
}

class _$AppointmentRequestDetailSerializer implements PrimitiveSerializer<AppointmentRequestDetail> {
  @override
  final Iterable<Type> types = const [AppointmentRequestDetail, _$AppointmentRequestDetail];

  @override
  final String wireName = r'AppointmentRequestDetail';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    AppointmentRequestDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(int),
    );
    yield r'doctor_phone';
    yield serializers.serialize(
      object.doctorPhone,
      specifiedType: const FullType(String),
    );
    yield r'patient_phone';
    yield serializers.serialize(
      object.patientPhone,
      specifiedType: const FullType(String),
    );
    if (object.note != null) {
      yield r'note';
      yield serializers.serialize(
        object.note,
        specifiedType: const FullType(String),
      );
    }
    yield r'status';
    yield serializers.serialize(
      object.status,
      specifiedType: const FullType(AppointmentRequestDetailStatusEnum),
    );
    yield r'created_at';
    yield serializers.serialize(
      object.createdAt,
      specifiedType: const FullType(DateTime),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    AppointmentRequestDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required AppointmentRequestDetailBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.id = valueDes;
          break;
        case r'doctor_phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.doctorPhone = valueDes;
          break;
        case r'patient_phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.patientPhone = valueDes;
          break;
        case r'note':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.note = valueDes;
          break;
        case r'status':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(AppointmentRequestDetailStatusEnum),
          ) as AppointmentRequestDetailStatusEnum;
          result.status = valueDes;
          break;
        case r'created_at':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(DateTime),
          ) as DateTime;
          result.createdAt = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  AppointmentRequestDetail deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = AppointmentRequestDetailBuilder();
    final serializedList = (serialized as Iterable<Object?>).toList();
    final unhandled = <Object?>[];
    _deserializeProperties(
      serializers,
      serialized,
      specifiedType: specifiedType,
      serializedList: serializedList,
      unhandled: unhandled,
      result: result,
    );
    return result.build();
  }
}

class AppointmentRequestDetailStatusEnum extends EnumClass {

  @BuiltValueEnumConst(wireName: r'pending')
  static const AppointmentRequestDetailStatusEnum pending = _$appointmentRequestDetailStatusEnum_pending;
  @BuiltValueEnumConst(wireName: r'accepted')
  static const AppointmentRequestDetailStatusEnum accepted = _$appointmentRequestDetailStatusEnum_accepted;
  @BuiltValueEnumConst(wireName: r'rejected')
  static const AppointmentRequestDetailStatusEnum rejected = _$appointmentRequestDetailStatusEnum_rejected;

  static Serializer<AppointmentRequestDetailStatusEnum> get serializer => _$appointmentRequestDetailStatusEnumSerializer;

  const AppointmentRequestDetailStatusEnum._(String name): super(name);

  static BuiltSet<AppointmentRequestDetailStatusEnum> get values => _$appointmentRequestDetailStatusEnumValues;
  static AppointmentRequestDetailStatusEnum valueOf(String name) => _$appointmentRequestDetailStatusEnumValueOf(name);
}

