# Schema Docs

Type: `object`

| Property | Pattern | Type | Required | Deprecated | Additional | Description |
| -------- | ------- | ---- | -------- | ---------- | ---------- | ----------- |
| [billing_address](#billing_address)|No|object|No|No| No||
| [shipping_address](#shipping_address)|No|object|No|No| No||

## <a name="billing_address"></a>Property `billing_address`

      root
 >   billing_address

Type: `object`

| Property | Pattern | Type | Required | Deprecated | Additional | Description |
| -------- | ------- | ---- | -------- | ---------- | ---------- | ----------- |
|street_address|No|string|Yes|No| No||
|city|No|string|Yes|No| No||
|state|No|string|Yes|No| No||

## <a name="shipping_address"></a>Property `shipping_address`

      root
 >   shipping_address

Type: `object`

        Same definition as [billing_address](#billing_address)

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2021-01-31 at 13:13:13 +0100