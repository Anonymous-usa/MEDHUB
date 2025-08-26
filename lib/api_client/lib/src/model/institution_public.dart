//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:medhub_api/src/model/department.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'institution_public.g.dart';

/// InstitutionPublic
///
/// Properties:
/// * [id] 
/// * [name] 
/// * [slug] 
/// * [description] 
/// * [institutionType] 
/// * [ownershipType] 
/// * [region] 
/// * [address] 
/// * [phone] 
/// * [email] 
/// * [logoUrl] 
/// * [isTop] 
/// * [departments] 
@BuiltValue()
abstract class InstitutionPublic implements Built<InstitutionPublic, InstitutionPublicBuilder> {
  @BuiltValueField(wireName: r'id')
  int get id;

  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'slug')
  String get slug;

  @BuiltValueField(wireName: r'description')
  String? get description;

  @BuiltValueField(wireName: r'institution_type')
  InstitutionPublicInstitutionTypeEnum get institutionType;
  // enum institutionTypeEnum {  hospital,  clinic,  laboratory,  other,  };

  @BuiltValueField(wireName: r'ownership_type')
  InstitutionPublicOwnershipTypeEnum get ownershipType;
  // enum ownershipTypeEnum {  state,  private,  };

  @BuiltValueField(wireName: r'region')
  String get region;

  @BuiltValueField(wireName: r'address')
  String get address;

  @BuiltValueField(wireName: r'phone')
  String get phone;

  @BuiltValueField(wireName: r'email')
  String get email;

  @BuiltValueField(wireName: r'logo_url')
  String? get logoUrl;

  @BuiltValueField(wireName: r'is_top')
  bool? get isTop;

  @BuiltValueField(wireName: r'departments')
  BuiltList<Department>? get departments;

  InstitutionPublic._();

  factory InstitutionPublic([void updates(InstitutionPublicBuilder b)]) = _$InstitutionPublic;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(InstitutionPublicBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<InstitutionPublic> get serializer => _$InstitutionPublicSerializer();
}

class _$InstitutionPublicSerializer implements PrimitiveSerializer<InstitutionPublic> {
  @override
  final Iterable<Type> types = const [InstitutionPublic, _$InstitutionPublic];

  @override
  final String wireName = r'InstitutionPublic';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    InstitutionPublic object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(int),
    );
    yield r'name';
    yield serializers.serialize(
      object.name,
      specifiedType: const FullType(String),
    );
    yield r'slug';
    yield serializers.serialize(
      object.slug,
      specifiedType: const FullType(String),
    );
    if (object.description != null) {
      yield r'description';
      yield serializers.serialize(
        object.description,
        specifiedType: const FullType(String),
      );
    }
    yield r'institution_type';
    yield serializers.serialize(
      object.institutionType,
      specifiedType: const FullType(InstitutionPublicInstitutionTypeEnum),
    );
    yield r'ownership_type';
    yield serializers.serialize(
      object.ownershipType,
      specifiedType: const FullType(InstitutionPublicOwnershipTypeEnum),
    );
    yield r'region';
    yield serializers.serialize(
      object.region,
      specifiedType: const FullType(String),
    );
    yield r'address';
    yield serializers.serialize(
      object.address,
      specifiedType: const FullType(String),
    );
    yield r'phone';
    yield serializers.serialize(
      object.phone,
      specifiedType: const FullType(String),
    );
    yield r'email';
    yield serializers.serialize(
      object.email,
      specifiedType: const FullType(String),
    );
    if (object.logoUrl != null) {
      yield r'logo_url';
      yield serializers.serialize(
        object.logoUrl,
        specifiedType: const FullType(String),
      );
    }
    if (object.isTop != null) {
      yield r'is_top';
      yield serializers.serialize(
        object.isTop,
        specifiedType: const FullType(bool),
      );
    }
    if (object.departments != null) {
      yield r'departments';
      yield serializers.serialize(
        object.departments,
        specifiedType: const FullType(BuiltList, [FullType(Department)]),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    InstitutionPublic object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required InstitutionPublicBuilder result,
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
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.name = valueDes;
          break;
        case r'slug':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.slug = valueDes;
          break;
        case r'description':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.description = valueDes;
          break;
        case r'institution_type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(InstitutionPublicInstitutionTypeEnum),
          ) as InstitutionPublicInstitutionTypeEnum;
          result.institutionType = valueDes;
          break;
        case r'ownership_type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(InstitutionPublicOwnershipTypeEnum),
          ) as InstitutionPublicOwnershipTypeEnum;
          result.ownershipType = valueDes;
          break;
        case r'region':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.region = valueDes;
          break;
        case r'address':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.address = valueDes;
          break;
        case r'phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.phone = valueDes;
          break;
        case r'email':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.email = valueDes;
          break;
        case r'logo_url':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.logoUrl = valueDes;
          break;
        case r'is_top':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(bool),
          ) as bool;
          result.isTop = valueDes;
          break;
        case r'departments':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltList, [FullType(Department)]),
          ) as BuiltList<Department>;
          result.departments.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  InstitutionPublic deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = InstitutionPublicBuilder();
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

class InstitutionPublicInstitutionTypeEnum extends EnumClass {

  @BuiltValueEnumConst(wireName: r'hospital')
  static const InstitutionPublicInstitutionTypeEnum hospital = _$institutionPublicInstitutionTypeEnum_hospital;
  @BuiltValueEnumConst(wireName: r'clinic')
  static const InstitutionPublicInstitutionTypeEnum clinic = _$institutionPublicInstitutionTypeEnum_clinic;
  @BuiltValueEnumConst(wireName: r'laboratory')
  static const InstitutionPublicInstitutionTypeEnum laboratory = _$institutionPublicInstitutionTypeEnum_laboratory;
  @BuiltValueEnumConst(wireName: r'other')
  static const InstitutionPublicInstitutionTypeEnum other = _$institutionPublicInstitutionTypeEnum_other;

  static Serializer<InstitutionPublicInstitutionTypeEnum> get serializer => _$institutionPublicInstitutionTypeEnumSerializer;

  const InstitutionPublicInstitutionTypeEnum._(String name): super(name);

  static BuiltSet<InstitutionPublicInstitutionTypeEnum> get values => _$institutionPublicInstitutionTypeEnumValues;
  static InstitutionPublicInstitutionTypeEnum valueOf(String name) => _$institutionPublicInstitutionTypeEnumValueOf(name);
}

class InstitutionPublicOwnershipTypeEnum extends EnumClass {

  @BuiltValueEnumConst(wireName: r'state')
  static const InstitutionPublicOwnershipTypeEnum state = _$institutionPublicOwnershipTypeEnum_state;
  @BuiltValueEnumConst(wireName: r'private')
  static const InstitutionPublicOwnershipTypeEnum private = _$institutionPublicOwnershipTypeEnum_private;

  static Serializer<InstitutionPublicOwnershipTypeEnum> get serializer => _$institutionPublicOwnershipTypeEnumSerializer;

  const InstitutionPublicOwnershipTypeEnum._(String name): super(name);

  static BuiltSet<InstitutionPublicOwnershipTypeEnum> get values => _$institutionPublicOwnershipTypeEnumValues;
  static InstitutionPublicOwnershipTypeEnum valueOf(String name) => _$institutionPublicOwnershipTypeEnumValueOf(name);
}

