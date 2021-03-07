# Event

- [1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > id`](#id)
- [2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > version`](#version)
- [3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor`](#actor)
  - [3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor > objectType`](#actor_objectType)
  - [3.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor > openid`](#actor_openid)
    - [3.2.1. Property `Event > actor > openid > oneOf > item 0`](#actor_openid_oneOf_i0)
- [4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb`](#verb)
  - [4.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > id`](#verb_id)
  - [4.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > display`](#verb_display)
    - [4.2.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > display > en-US`](#verb_display_en-US)
- [5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object`](#object)
  - [5.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > objectType`](#object_objectType)
  - [5.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > id`](#object_id)
    - [5.2.1. Property `Event > object > id > oneOf > item 0`](#object_id_oneOf_i0)
    - [5.2.2. Property `Event > object > id > oneOf > item 1`](#object_id_oneOf_i1)
    - [5.2.3. Property `Event > object > id > oneOf > item 2`](#object_id_oneOf_i2)
    - [5.2.4. Property `Event > object > id > oneOf > item 3`](#object_id_oneOf_i3)
    - [5.2.5. Property `Event > object > id > oneOf > item 4`](#object_id_oneOf_i4)
    - [5.2.6. Property `Event > object > id > oneOf > item 5`](#object_id_oneOf_i5)
    - [5.2.7. Property `Event > object > id > oneOf > item 6`](#object_id_oneOf_i6)
  - [5.3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition`](#object_definition)
    - [5.3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > type`](#object_definition_type)
    - [5.3.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > name`](#object_definition_name)
      - [5.3.2.1. ![badge](https://img.shields.io/badge/Optional-yellow)Pattern Property `Event > object > definition > name > (?<localeCode>^[a-z]{2,3}-[A-Z]{2,3}$)`](#object_definition_name_pattern1)
    - [5.3.3. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > object > definition > extensions`](#object_definition_extensions)
      - [5.3.3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > extensions > https://company.com/xapi/extensions/provider`](#object_definition_extensions_https___company_com_xapi_extensions_provider)
- [6. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > result`](#result)
  - [6.1. Property `Event > result > oneOf > result.score`](#result_oneOf_i0)
    - [6.1.1. Property `Event > result > oneOf > the raw score between min and max > score`](#result_oneOf_i0_score)
      - [6.1.1.1. Property `Event > result > oneOf > the raw score between min and max > score > raw`](#result_oneOf_i0_score_raw)
      - [6.1.1.2. Property `Event > result > oneOf > the raw score between min and max > score > min`](#result_oneOf_i0_score_min)
      - [6.1.1.3. Property `Event > result > oneOf > the raw score between min and max > score > max`](#result_oneOf_i0_score_max)
  - [6.2. Property `Event > result > oneOf > result.response`](#result_oneOf_i1)
    - [6.2.1. Property `Event > result > oneOf > item 1 > response`](#result_oneOf_i1_response)
  - [6.3. Property `Event > result > oneOf > result.completion_duration`](#result_oneOf_i2)
    - [6.3.1. Property `Event > result > oneOf > item 2 > duration`](#result_oneOf_i2_duration)
    - [6.3.2. Property `Event > result > oneOf > item 2 > completion`](#result_oneOf_i2_completion)
  - [6.4. Property `Event > result > oneOf > result.completion_score`](#result_oneOf_i3)
    - [6.4.1. Property `Event > result > oneOf > item 3 > completion`](#result_oneOf_i3_completion)
    - [6.4.2. Property `Event > result > oneOf > item 3 > score`](#result_oneOf_i3_score)
      - [6.4.2.1. Property `Event > result > oneOf > item 3 > score > raw`](#result_oneOf_i3_score_raw)
      - [6.4.2.2. Property `Event > result > oneOf > item 3 > score > min`](#result_oneOf_i3_score_min)
      - [6.4.2.3. Property `Event > result > oneOf > item 3 > score > max`](#result_oneOf_i3_score_max)
- [7. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context`](#context)
  - [7.1. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > registration`](#context_registration)
  - [7.2. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > contextActivities`](#context_contextActivities)
    - [7.2.1. Property `Event > context > contextActivities > oneOf > context.contextActivitiesTraining`](#context_contextActivities_oneOf_i0)
      - [7.2.1.1. Property `Event > context > contextActivities > oneOf > item 0 > parent`](#context_contextActivities_oneOf_i0_parent)
        - [7.2.1.1.1. Event > context > contextActivities > oneOf > item 0 > parent > items](#autogenerated_heading_2)
          - [7.2.1.1.1.1. Property `Event > context > contextActivities > oneOf > item 0 > parent > items > id`](#context_contextActivities_oneOf_i0_parent_items_id)
      - [7.2.1.2. Property `Event > context > contextActivities > oneOf > item 0 > grouping`](#context_contextActivities_oneOf_i0_grouping)
        - [7.2.1.2.1. Event > context > contextActivities > oneOf > item 0 > grouping > items](#autogenerated_heading_3)
          - [7.2.1.2.1.1. Property `Event > context > contextActivities > oneOf > item 0 > grouping > items > id`](#context_contextActivities_oneOf_i0_grouping_items_id)
    - [7.2.2. Property `Event > context > contextActivities > oneOf > context.contextActivitiesLOV`](#context_contextActivities_oneOf_i1)
      - [7.2.2.1. Must **not** be](#autogenerated_heading_4)
        - [7.2.2.1.1. The following properties are required](#autogenerated_heading_5)
      - [7.2.2.2. Property `Event > context > contextActivities > oneOf > item 1 > parent`](#context_contextActivities_oneOf_i1_parent)
        - [7.2.2.2.1. Event > context > contextActivities > oneOf > item 1 > parent > items](#autogenerated_heading_6)
          - [7.2.2.2.1.1. Property `Event > context > contextActivities > oneOf > item 1 > parent > items > id`](#context_contextActivities_oneOf_i1_parent_items_id)
  - [7.3. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > revision`](#context_revision)
  - [7.4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > platform`](#context_platform)
  - [7.5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > language`](#context_language)
  - [7.6. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions`](#context_extensions)
    - [7.6.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/schemaVersion`](#context_extensions_https___company_com_xapi_extensions_schemaVersion)
    - [7.6.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/schemaCompliance`](#context_extensions_https___company_com_xapi_extensions_schemaCompliance)
    - [7.6.3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/device`](#context_extensions_https___company_com_xapi_extensions_device)
    - [7.6.4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/launched-from`](#context_extensions_https___company_com_xapi_extensions_launched-from)
    - [7.6.5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/dbname`](#context_extensions_https___company_com_xapi_extensions_dbname)
    - [7.6.6. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > extensions > https://company.com/xapi/extensions/provider`](#context_extensions_https___company_com_xapi_extensions_provider)
    - [7.6.7. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > extensions > https://company.com/xapi/extensions/step`](#context_extensions_https___company_com_xapi_extensions_step)
- [8. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > timestamp`](#timestamp)

**Title:** Event

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

**Description:** Event in xAPI format
Version of this schema is indicated in $id and uses the following rules, Given a version number MODEL.REVISION.ADDITION, increment the:
 * MODEL when you make a breaking schema change which will prevent interaction with any historical data
 * REVISION when you make a schema change which may prevent interaction with some historical data
 * ADDITION when you make a schema change that is compatible with all historical data

[check here to see more examples](https://snowplowanalytics.com/blog/2014/05/13/introducing-schemaver-for-semantic-versioning-of-schemas/) we apply the same rules except we are using . instead of hyphen too separate the numbers

| Property                   | Pattern | Type   | Deprecated | Definition               | Title/Description                      |
| -------------------------- | ------- | ------ | ---------- | ------------------------ | -------------------------------------- |
| + [id](#id )               | No      | string | No         | -                        | ID of the statement                    |
| + [version](#version )     | No      | string | No         | -                        | Version of the xApi specification used |
| + [actor](#actor )         | No      | object | No         | In #/definitions/actor   | Actor                                  |
| + [verb](#verb )           | No      | object | No         | In #/definitions/verb    | Verb                                   |
| + [object](#object )       | No      | object | No         | In #/definitions/object  | Object                                 |
| - [result](#result )       | No      | object | No         | In #/definitions/result  | Result                                 |
| + [context](#context )     | No      | object | No         | In #/definitions/context | Context                                |
| + [timestamp](#timestamp ) | No      | string | No         | -                        | date time of the event is generated    |
|                            |         |        |            |                          |                                        |

## <a name="id"></a>1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > id`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** ID of the statement

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```(?<eventUUID>^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$)``` [Test](https://regex101.com/?regex=%28%3F%3CeventUUID%3E%5E%5B0-9a-f%5D%7B8%7D-%5B0-9a-f%5D%7B4%7D-4%5B0-9a-f%5D%7B3%7D-%5B89ab%5D%5B0-9a-f%5D%7B3%7D-%5B0-9a-f%5D%7B12%7D%24%29&testString=%22b0f78af6-7ad9-4726-9e02-d64c38bdd13f%22) |
|                                   |                                                                                                                                                                                                                                                                                                                                   |

**Example:** 

```json
"b0f78af6-7ad9-4726-9e02-d64c38bdd13f"
```

## <a name="version"></a>2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > version`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Default**               | `"1.0.3"`                                                                                                           |
|                           |                                                                                                                     |

**Description:** Version of the xApi specification used

| Restrictions                      |                                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[0-9]+(.[0-9]+)+$``` [Test](https://regex101.com/?regex=%5E%5B0-9%5D%2B%28.%5B0-9%5D%2B%29%2B%24) |
|                                   |                                                                                                       |

## <a name="actor"></a>3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/actor                                                                                                 |
|                           |                                                                                                                     |

**Description:** Actor

| Property                           | Pattern | Type             | Deprecated | Definition | Title/Description                                                     |
| ---------------------------------- | ------- | ---------------- | ---------- | ---------- | --------------------------------------------------------------------- |
| + [objectType](#actor_objectType ) | No      | enum (of string) | No         | -          | property is required when the Agent is in the ‘object’ of a statement |
| + [openid](#actor_openid )         | No      | Combination      | No         | -          | unique identifier of an agent                                         |
|                                    |         |                  |            |            |                                                                       |

### <a name="actor_objectType"></a>3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor > objectType`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** property is required when the Agent is in the ‘object’ of a statement

Must be one of:
* "Agent"

### <a name="actor_openid"></a>3.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > actor > openid`

| Type                      | `combining`                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** unique identifier of an agent

#### <a name="actor_openid_oneOf_i0"></a>3.2.1. Property `Event > actor > openid > oneOf > item 0`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/learners/(?<learnerGuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Flearners%2F%28%3F%3ClearnerGuid%3E%5B0-9a-fA-F%5D%7B8%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B12%7D%29%24) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

**Example:** 

```json
"https://sample.company.com/xapi/instanceDbName/learners/E6018648-F538-3BF2-D5A6-61AF33E66061"
```

## <a name="verb"></a>4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/verb                                                                                                  |
|                           |                                                                                                                     |

**Description:** Verb

| Property                    | Pattern | Type             | Deprecated | Definition | Title/Description       |
| --------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------------- |
| + [id](#verb_id )           | No      | enum (of string) | No         | -          | Verb URL                |
| + [display](#verb_display ) | No      | object           | No         | -          | description of the verb |
|                             |         |                  |            |            |                         |

### <a name="verb_id"></a>4.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > id`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** Verb URL

Must be one of:
* "https://w3id.org/xapi/adl/verbs/logged-in"
* "http://id.tincanapi.com/verb/earned"
* "https://company.com/xapi/verbs/liked"
* "https://company.com/xapi/verbs/favorited"
* "http://id.tincanapi.com/verb/rated"
* "https://company.com/xapi/verbs/searched"
* "http://adlnet.gov/expapi/verbs/completed"
* "http://adlnet.gov/expapi/verbs/launched"

**Example:** 

```json
"http://adlnet.gov/expapi/verbs/launched"
```

### <a name="verb_display"></a>4.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > display`

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

**Description:** description of the verb

| Property                        | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [en-US](#verb_display_en-US ) | No      | string | No         | -          | -                 |
|                                 |         |        |            |            |                   |

#### <a name="verb_display_en-US"></a>4.2.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > verb > display > en-US`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Example:** 

```json
"launched"
```

## <a name="object"></a>5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/object                                                                                                |
|                           |                                                                                                                     |

**Description:** Object

| Property                            | Pattern | Type             | Deprecated | Definition                         | Title/Description                                                     |
| ----------------------------------- | ------- | ---------------- | ---------- | ---------------------------------- | --------------------------------------------------------------------- |
| + [objectType](#object_objectType ) | No      | enum (of string) | No         | -                                  | property is required when the Agent is in the ‘object’ of a statement |
| + [id](#object_id )                 | No      | Combination      | No         | -                                  | ID of the object                                                      |
| + [definition](#object_definition ) | No      | object           | No         | In #/definitions/object.definition | Object definition                                                     |
|                                     |         |                  |            |                                    |                                                                       |

### <a name="object_objectType"></a>5.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > objectType`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** property is required when the Agent is in the ‘object’ of a statement

Must be one of:
* "Activity"

### <a name="object_id"></a>5.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > id`

| Type                      | `combining`                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** ID of the object

#### <a name="object_id_oneOf_i0"></a>5.2.1. Property `Event > object > id > oneOf > item 0`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/login/.*$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Flogin%2F.%2A%24) |
|                                   |                                                                                                                                                                                                               |

#### <a name="object_id_oneOf_i1"></a>5.2.2. Property `Event > object > id > oneOf > item 1`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/path-session-item/[0-9]+/pre-assessment$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Fpath-session-item%2F%5B0-9%5D%2B%2Fpre-assessment%24) |
|                                   |                                                                                                                                                                                                                                                                                   |

#### <a name="object_id_oneOf_i2"></a>5.2.3. Property `Event > object > id > oneOf > item 2`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/registration/(?<registrationGuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/post-assessment$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Fregistration%2F%28%3F%3CregistrationGuid%3E%5B0-9a-fA-F%5D%7B8%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B12%7D%29%2Fpost-assessment%24) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

#### <a name="object_id_oneOf_i3"></a>5.2.4. Property `Event > object > id > oneOf > item 3`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/certificate/(?<certificateGuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Fcertificate%2F%28%3F%3CcertificateGuid%3E%5B0-9a-fA-F%5D%7B8%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B4%7D-%5B0-9a-fA-F%5D%7B12%7D%29%24) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

#### <a name="object_id_oneOf_i4"></a>5.2.5. Property `Event > object > id > oneOf > item 4`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/forum-posts/[0-9]+$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Fforum-posts%2F%5B0-9%5D%2B%24) |
|                                   |                                                                                                                                                                                                                                       |

#### <a name="object_id_oneOf_i5"></a>5.2.6. Property `Event > object > id > oneOf > item 5`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/learning-resources/[^/]+/guid/[^/]+$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Flearning-resources%2F%5B%5E%2F%5D%2B%2Fguid%2F%5B%5E%2F%5D%2B%24) |
|                                   |                                                                                                                                                                                                                                                                                           |

#### <a name="object_id_oneOf_i6"></a>5.2.7. Property `Event > object > id > oneOf > item 6`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                 |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/search/.+$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Fsearch%2F.%2B%24) |
|                                   |                                                                                                                                                                                                                 |

**Example:** 

```json
"http://test.domain/xapi/instanceDbName/learning-resources/VDAM015/guid/EDAF7AC9-D062-0003-B5F8-ED5455AD5AB2"
```

### <a name="object_definition"></a>5.3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/object.definition                                                                                     |
|                           |                                                                                                                     |

**Description:** Object definition

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description      |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ---------------------- |
| + [type](#object_definition_type )             | No      | enum (of string) | No         | -          | Activity type          |
| + [name](#object_definition_name )             | No      | object           | No         | -          | Learning resource name |
| - [extensions](#object_definition_extensions ) | No      | object           | No         | -          | -                      |
|                                                |         |                  |            |            |                        |

#### <a name="object_definition_type"></a>5.3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > type`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** Activity type

Must be one of:
* "https://company.com/xapi/activity-types/learning-resource"
* "https://company.com/xapi/activity-types/al-questionnaire"
* "https://company.com/xapi/activity-types/login"
* "https://company.com/xapi/activity-types/certificate"
* "https://company.com/xapi/activity-types/forum-post"
* "https://company.com/xapi/activity-types/search"

**Example:** 

```json
"https://company.com/xapi/activity-types/login"
```

#### <a name="object_definition_name"></a>5.3.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > name`

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

**Description:** Learning resource name

| Property                                                                      | Pattern | Type   | Deprecated | Definition | Title/Description       |
| ----------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [(?<localeCode>^[a-z]{2,3}-[A-Z]{2,3}$)](#object_definition_name_pattern1 ) | Yes     | string | No         | -          | learning resource title |
|                                                                               |         |        |            |            |                         |

##### <a name="object_definition_name_pattern1"></a>5.3.2.1. ![badge](https://img.shields.io/badge/Optional-yellow)Pattern Property `Event > object > definition > name > (?<localeCode>^[a-z]{2,3}-[A-Z]{2,3}$)`
> All property whose name matches the regular expression 
```(?<localeCode>^[a-z]{2,3}-[A-Z]{2,3}$)``` ([Test](https://regex101.com/?regex=%28%3F%3ClocaleCode%3E%5E%5Ba-z%5D%7B2%2C3%7D-%5BA-Z%5D%7B2%2C3%7D%24%29))
must respect the following conditions

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** learning resource title

#### <a name="object_definition_extensions"></a>5.3.3. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > object > definition > extensions`

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                                                                                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [https://company.com/xapi/extensions/provider](#object_definition_extensions_https___company_com_xapi_extensions_provider ) | No      | string | No         | -          | lo provider       |
|                                                                                                                               |         |        |            |            |                   |

##### <a name="object_definition_extensions_https___company_com_xapi_extensions_provider"></a>5.3.3.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > object > definition > extensions > https://company.com/xapi/extensions/provider`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** lo provider

**Example:** 

```json
"company"
```

## <a name="result"></a>6. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > result`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/result                                                                                                |
|                           |                                                                                                                     |

**Description:** Result

### <a name="result_oneOf_i0"></a>6.1. Property `Event > result > oneOf > result.score`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/result.score                                                                                          |
|                           |                                                                                                                     |

**Description:** could be result of a vote, score of a learner on given learning object

| Property                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [score](#result_oneOf_i0_score ) | No      | object | No         | -          | -                 |
|                                    |         |        |            |            |                   |

#### <a name="result_oneOf_i0_score"></a>6.1.1. Property `Event > result > oneOf > the raw score between min and max > score`

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                             | Pattern | Type    | Deprecated | Definition | Title/Description      |
| ------------------------------------ | ------- | ------- | ---------- | ---------- | ---------------------- |
| + [raw](#result_oneOf_i0_score_raw ) | No      | integer | No         | -          | raw value of the score |
| + [min](#result_oneOf_i0_score_min ) | No      | integer | No         | -          | min possible score     |
| + [max](#result_oneOf_i0_score_max ) | No      | integer | No         | -          | max possible score     |
|                                      |         |         |            |            |                        |

##### <a name="result_oneOf_i0_score_raw"></a>6.1.1.1. Property `Event > result > oneOf > the raw score between min and max > score > raw`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** raw value of the score

**Example:** 

```json
4
```

##### <a name="result_oneOf_i0_score_min"></a>6.1.1.2. Property `Event > result > oneOf > the raw score between min and max > score > min`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** min possible score

**Example:** 

```json
0
```

##### <a name="result_oneOf_i0_score_max"></a>6.1.1.3. Property `Event > result > oneOf > the raw score between min and max > score > max`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** max possible score

**Example:** 

```json
5
```

### <a name="result_oneOf_i1"></a>6.2. Property `Event > result > oneOf > result.response`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/result.response                                                                                       |
|                           |                                                                                                                     |

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [response](#result_oneOf_i1_response ) | No      | string | No         | -          | -                 |
|                                          |         |        |            |            |                   |

#### <a name="result_oneOf_i1_response"></a>6.2.1. Property `Event > result > oneOf > item 1 > response`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Example:** 

```json
"forum message"
```

### <a name="result_oneOf_i2"></a>6.3. Property `Event > result > oneOf > result.completion_duration`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/result.completion_duration                                                                            |
|                           |                                                                                                                     |

| Property                                     | Pattern | Type    | Deprecated | Definition | Title/Description                           |
| -------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------- |
| + [duration](#result_oneOf_i2_duration )     | No      | string  | No         | -          | duration of the learning resource           |
| + [completion](#result_oneOf_i2_completion ) | No      | boolean | No         | -          | check if the learning resource is completed |
|                                              |         |         |            |            |                                             |

#### <a name="result_oneOf_i2_duration"></a>6.3.1. Property `Event > result > oneOf > item 2 > duration`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** duration of the learning resource

| Restrictions                      |                                                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^PT[0-9]+S``` [Test](https://regex101.com/?regex=%5EPT%5B0-9%5D%2BS&testString=%22PT300S%22) |
|                                   |                                                                                                 |

**Example:** 

```json
"PT300S"
```

#### <a name="result_oneOf_i2_completion"></a>6.3.2. Property `Event > result > oneOf > item 2 > completion`

| Type                      | `boolean`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** check if the learning resource is completed

**Example:** 

```json
true
```

### <a name="result_oneOf_i3"></a>6.4. Property `Event > result > oneOf > result.completion_score`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/result.completion_score                                                                               |
|                           |                                                                                                                     |

| Property                                     | Pattern | Type    | Deprecated | Definition | Title/Description                           |
| -------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------- |
| + [completion](#result_oneOf_i3_completion ) | No      | boolean | No         | -          | check if the learning resource is completed |
| + [score](#result_oneOf_i3_score )           | No      | object  | No         | -          | -                                           |
|                                              |         |         |            |            |                                             |

#### <a name="result_oneOf_i3_completion"></a>6.4.1. Property `Event > result > oneOf > item 3 > completion`

| Type                      | `boolean`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** check if the learning resource is completed

**Example:** 

```json
true
```

#### <a name="result_oneOf_i3_score"></a>6.4.2. Property `Event > result > oneOf > item 3 > score`

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                             | Pattern | Type    | Deprecated | Definition | Title/Description      |
| ------------------------------------ | ------- | ------- | ---------- | ---------- | ---------------------- |
| + [raw](#result_oneOf_i3_score_raw ) | No      | integer | No         | -          | raw value of the score |
| + [min](#result_oneOf_i3_score_min ) | No      | integer | No         | -          | min possible score     |
| + [max](#result_oneOf_i3_score_max ) | No      | integer | No         | -          | max possible score     |
|                                      |         |         |            |            |                        |

##### <a name="result_oneOf_i3_score_raw"></a>6.4.2.1. Property `Event > result > oneOf > item 3 > score > raw`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** raw value of the score

**Example:** 

```json
4
```

##### <a name="result_oneOf_i3_score_min"></a>6.4.2.2. Property `Event > result > oneOf > item 3 > score > min`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** min possible score

**Example:** 

```json
0
```

##### <a name="result_oneOf_i3_score_max"></a>6.4.2.3. Property `Event > result > oneOf > item 3 > score > max`

| Type                      | `integer`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** max possible score

**Example:** 

```json
5
```

## <a name="context"></a>7. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/context                                                                                               |
|                           |                                                                                                                     |

**Description:** Context

| Property                                           | Pattern | Type        | Deprecated | Definition                          | Title/Description                                                                    |
| -------------------------------------------------- | ------- | ----------- | ---------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| - [registration](#context_registration )           | No      | string      | No         | -                                   | Registration UUID of the session                                                     |
| - [contextActivities](#context_contextActivities ) | No      | Combination | No         | -                                   | -                                                                                    |
| - [revision](#context_revision )                   | No      | string      | No         | -                                   | revision of the learning resource                                                    |
| + [platform](#context_platform )                   | No      | string      | No         | -                                   | identify the platform <origin>:<instanceBaseName> origin can be only PRODUCT for ... |
| + [language](#context_language )                   | No      | string      | No         | -                                   | language code of the training/session                                                |
| + [extensions](#context_extensions )               | No      | object      | No         | In #/definitions/context.extensions | extra information                                                                    |
|                                                    |         |             |            |                                     |                                                                                      |

### <a name="context_registration"></a>7.1. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > registration`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** Registration UUID of the session

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```(?<registrationUUID>^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-8[0-9a-f]{3}-[0-9a-f]{12}$)``` [Test](https://regex101.com/?regex=%28%3F%3CregistrationUUID%3E%5E%5B0-9a-f%5D%7B8%7D-%5B0-9a-f%5D%7B4%7D-4%5B0-9a-f%5D%7B3%7D-8%5B0-9a-f%5D%7B3%7D-%5B0-9a-f%5D%7B12%7D%24%29&testString=%22b0f78af6-7ad9-4726-8e02-d64c38bdd13f%22) |
|                                   |                                                                                                                                                                                                                                                                                                                                   |

**Example:** 

```json
"b0f78af6-7ad9-4726-8e02-d64c38bdd13f"
```

### <a name="context_contextActivities"></a>7.2. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > contextActivities`

| Type                      | `combining`                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

#### <a name="context_contextActivities_oneOf_i0"></a>7.2.1. Property `Event > context > contextActivities > oneOf > context.contextActivitiesTraining`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/context.contextActivitiesTraining                                                                     |
|                           |                                                                                                                     |

| Property                                                    | Pattern | Type            | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [parent](#context_contextActivities_oneOf_i0_parent )     | No      | array of object | No         | -          | -                 |
| + [grouping](#context_contextActivities_oneOf_i0_grouping ) | No      | array of object | No         | -          | -                 |
|                                                             |         |                 |            |            |                   |

##### <a name="context_contextActivities_oneOf_i0_parent"></a>7.2.1.1. Property `Event > context > contextActivities > oneOf > item 0 > parent`

| Type                      | `array of object`                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |
|                      |                    |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [items](#context_contextActivities_oneOf_i0_parent_items) | -           |
|                                                           |             |

###### <a name="autogenerated_heading_2"></a>7.2.1.1.1. Event > context > contextActivities > oneOf > item 0 > parent > items

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description       |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------------- |
| + [id](#context_contextActivities_oneOf_i0_parent_items_id ) | No      | string | No         | -          | training session URL id |
|                                                              |         |        |            |            |                         |

####### <a name="context_contextActivities_oneOf_i0_parent_items_id"></a>7.2.1.1.1.1. Property `Event > context > contextActivities > oneOf > item 0 > parent > items > id`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** training session URL id

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/training-sessions/(?<trainingSessionGuid>[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Ftraining-sessions%2F%28%3F%3CtrainingSessionGuid%3E%5BA-F0-9%5D%7B8%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B12%7D%29%24&testString=%22http%3A%2F%2Ftest.domain%2Fxapi%2FinstanceDbName%2Ftraining-sessions%2F2F4D5B3B-9729-05A2-EB8A-418F4B7DDB7A%22) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

**Example:** 

```json
"http://test.domain/xapi/instanceDbName/training-sessions/2F4D5B3B-9729-05A2-EB8A-418F4B7DDB7A"
```

##### <a name="context_contextActivities_oneOf_i0_grouping"></a>7.2.1.2. Property `Event > context > contextActivities > oneOf > item 0 > grouping`

| Type                      | `array of object`                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |
|                      |                    |

| Each item of this array must be                             | Description |
| ----------------------------------------------------------- | ----------- |
| [items](#context_contextActivities_oneOf_i0_grouping_items) | -           |
|                                                             |             |

###### <a name="autogenerated_heading_3"></a>7.2.1.2.1. Event > context > contextActivities > oneOf > item 0 > grouping > items

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                                                       | Pattern | Type   | Deprecated | Definition | Title/Description      |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------- |
| + [id](#context_contextActivities_oneOf_i0_grouping_items_id ) | No      | string | No         | -          | training course URL id |
|                                                                |         |        |            |            |                        |

####### <a name="context_contextActivities_oneOf_i0_grouping_items_id"></a>7.2.1.2.1.1. Property `Event > context > contextActivities > oneOf > item 0 > grouping > items > id`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** training course URL id

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/training-courses/(?<trainingGuid>[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Ftraining-courses%2F%28%3F%3CtrainingGuid%3E%5BA-F0-9%5D%7B8%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B4%7D-%5BA-F0-9%5D%7B12%7D%29%24&testString=%22http%3A%2F%2Ftest.domain%2FinstanceDbName%2Ftraining-courses%2F2F4D5B3B-9729-05A2-EB8A-418F4B7DDB7A%22) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

**Example:** 

```json
"http://test.domain/instanceDbName/training-courses/2F4D5B3B-9729-05A2-EB8A-418F4B7DDB7A"
```

#### <a name="context_contextActivities_oneOf_i1"></a>7.2.2. Property `Event > context > contextActivities > oneOf > context.contextActivitiesLOV`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/context.contextActivitiesLOV                                                                          |
|                           |                                                                                                                     |

| Property                                                | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [parent](#context_contextActivities_oneOf_i1_parent ) | No      | array of object | No         | -          | -                 |
|                                                         |         |                 |            |            |                   |

##### <a name="autogenerated_heading_4"></a>7.2.2.1. Must **not** be

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

###### <a name="autogenerated_heading_5"></a>7.2.2.1.1. The following properties are required
* grouping

##### <a name="context_contextActivities_oneOf_i1_parent"></a>7.2.2.2. Property `Event > context > contextActivities > oneOf > item 1 > parent`

| Type                      | `array of object`                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |
|                      |                    |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [items](#context_contextActivities_oneOf_i1_parent_items) | -           |
|                                                           |             |

###### <a name="autogenerated_heading_6"></a>7.2.2.2.1. Event > context > contextActivities > oneOf > item 1 > parent > items

| Type                      | `object`                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Additional properties** | [![badge](https://img.shields.io/badge/Not+allowed-red)](# "Additional Properties not allowed.") |
|                           |                                                                                                  |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [id](#context_contextActivities_oneOf_i1_parent_items_id ) | No      | string | No         | -          | -                 |
|                                                              |         |        |            |            |                   |

####### <a name="context_contextActivities_oneOf_i1_parent_items_id"></a>7.2.2.2.1.1. Property `Event > context > contextActivities > oneOf > item 1 > parent > items > id`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

| Restrictions                      |                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^https?://[^/]+/xapi/(?<instanceDbName>[^/]+)/learning-resources/[^/]+/guid/[^/]+$``` [Test](https://regex101.com/?regex=%5Ehttps%3F%3A%2F%2F%5B%5E%2F%5D%2B%2Fxapi%2F%28%3F%3CinstanceDbName%3E%5B%5E%2F%5D%2B%29%2Flearning-resources%2F%5B%5E%2F%5D%2B%2Fguid%2F%5B%5E%2F%5D%2B%24&testString=%22http%3A%2F%2Ftest.domain%2Fxapi%2FinstanceDbName%2Flearning-resources%2FVDAM015%2Fguid%2FEDAF7AC9-D062-0003-B5F8-ED5455AD5AB2%22) |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                          |

**Example:** 

```json
"http://test.domain/xapi/instanceDbName/learning-resources/VDAM015/guid/EDAF7AC9-D062-0003-B5F8-ED5455AD5AB2"
```

### <a name="context_revision"></a>7.3. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > revision`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** revision of the learning resource

| Restrictions                      |                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[0-9]+$``` [Test](https://regex101.com/?regex=%5E%5B0-9%5D%2B%24&testString=1) |
|                                   |                                                                                    |

**Example:** 

```json
1
```

### <a name="context_platform"></a>7.4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > platform`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** identify the platform <origin>:<instanceBaseName> origin can be only PRODUCT for the moment but could be CKCONNECT, ... in the future

| Restrictions                      |                                                                                                                                                                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^(?<origin>PRODUCT):(?<instanceBaseName>[^:]+)$``` [Test](https://regex101.com/?regex=%5E%28%3F%3Corigin%3EPRODUCT%29%3A%28%3F%3CinstanceBaseName%3E%5B%5E%3A%5D%2B%29%24&testString=%22PRODUCT%3ACOMPANY%22) |
|                                   |                                                                                                                                                                                                                  |

**Example:** 

```json
"PRODUCT:COMPANY"
```

### <a name="context_language"></a>7.5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > language`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** language code of the training/session

| Restrictions                      |                                                                                                                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```(?<localeCode>^[a-z]{2,3}-[A-Z]{2,3}$)``` [Test](https://regex101.com/?regex=%28%3F%3ClocaleCode%3E%5E%5Ba-z%5D%7B2%2C3%7D-%5BA-Z%5D%7B2%2C3%7D%24%29&testString=%22es-ES%22) |
|                                   |                                                                                                                                                                                  |

**Example:** 

```json
"es-ES"
```

### <a name="context_extensions"></a>7.6. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions`

| Type                      | `object`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/context.extensions                                                                                    |
|                           |                                                                                                                     |

**Description:** extra information

| Property                                                                                                                            | Pattern | Type             | Deprecated | Definition                     | Title/Description                   |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------- | ---------- | ------------------------------ | ----------------------------------- |
| + [https://company.com/xapi/extensions/schemaVersion](#context_extensions_https___company_com_xapi_extensions_schemaVersion )       | No      | string           | No         | -                              | schema version used                 |
| + [https://company.com/xapi/extensions/schemaCompliance](#context_extensions_https___company_com_xapi_extensions_schemaCompliance ) | No      | boolean          | No         | -                              | schema compliance of this statement |
| + [https://company.com/xapi/extensions/device](#context_extensions_https___company_com_xapi_extensions_device )                     | No      | enum (of string) | No         | -                              | Device used                         |
| + [https://company.com/xapi/extensions/launched-from](#context_extensions_https___company_com_xapi_extensions_launched-from )       | No      | enum (of string) | No         | -                              | launched from                       |
| + [https://company.com/xapi/extensions/dbname](#context_extensions_https___company_com_xapi_extensions_dbname )                     | No      | string           | No         | -                              | database name                       |
| - [https://company.com/xapi/extensions/provider](#context_extensions_https___company_com_xapi_extensions_provider )                 | No      | string           | No         | -                              | lo provider                         |
| - [https://company.com/xapi/extensions/step](#context_extensions_https___company_com_xapi_extensions_step )                         | No      | number           | No         | In #/definitions/property.step | training session step               |
|                                                                                                                                     |         |                  |            |                                |                                     |

#### <a name="context_extensions_https___company_com_xapi_extensions_schemaVersion"></a>7.6.1. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/schemaVersion`

**Title:** schema version used

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Default**               | `"1.0.0"`                                                                                                           |
|                           |                                                                                                                     |

**Description:** Version of the schema that has been used during event generation

| Restrictions                      |                                                                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[0-9]+(.[0-9]+)+$``` [Test](https://regex101.com/?regex=%5E%5B0-9%5D%2B%28.%5B0-9%5D%2B%29%2B%24&testString=%221.0.0%22) |
|                                   |                                                                                                                              |

**Examples:** 

```json
"1.0.0"
```
```json
"2.5.0"
```

#### <a name="context_extensions_https___company_com_xapi_extensions_schemaCompliance"></a>7.6.2. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/schemaCompliance`

**Title:** schema compliance of this statement

| Type                      | `boolean`                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Default**               | `true`                                                                                                              |
|                           |                                                                                                                     |

**Description:** indicates if the event is compliant with this schema version, it could be false if statement generated by code does not validate but nevertheless sent

#### <a name="context_extensions_https___company_com_xapi_extensions_device"></a>7.6.3. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/device`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** Device used

Must be one of:
* "mobile-webpage"
* "desktop-webpage"
* "mobile-app"
* "server"

**Example:** 

```json
"mobile-webpage"
```

#### <a name="context_extensions_https___company_com_xapi_extensions_launched-from"></a>7.6.4. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/launched-from`

| Type                      | `enum (of string)`                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** launched from

Must be one of:
* "PRODUCT"

**Example:** 

```json
"PRODUCT"
```

#### <a name="context_extensions_https___company_com_xapi_extensions_dbname"></a>7.6.5. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > context > extensions > https://company.com/xapi/extensions/dbname`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** database name

**Example:** 

```json
"DATABASE"
```

#### <a name="context_extensions_https___company_com_xapi_extensions_provider"></a>7.6.6. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > extensions > https://company.com/xapi/extensions/provider`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** lo provider

**Example:** 

```json
"company"
```

#### <a name="context_extensions_https___company_com_xapi_extensions_step"></a>7.6.7. ![badge](https://img.shields.io/badge/Optional-yellow) Property `Event > context > extensions > https://company.com/xapi/extensions/step`

| Type                      | `number`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/definitions/property.step                                                                                         |
|                           |                                                                                                                     |

**Description:** training session step

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |
|              |        |

**Example:** 

```json
0
```

## <a name="timestamp"></a>8. ![badge](https://img.shields.io/badge/Required-blue) Property `Event > timestamp`

| Type                      | `string`                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Additional properties** | [![badge](https://img.shields.io/badge/Any+type-allowed-green)](# "Additional Properties of any type are allowed.") |
|                           |                                                                                                                     |

**Description:** date time of the event is generated

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on date