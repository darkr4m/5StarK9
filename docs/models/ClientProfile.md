# Client Profile

## Description

**Appplication:** `clients_app`
**Class** `ClientProfile(models.Model)` - Represents a client (dog owner) in the system. This model stores essential contact information and tracking details about their services received.

## Fields

| Field                      | Type            | Relationships | Constraints | Validation | Description / Help Text | Verbose Names |
| -------------------------- | --------------- | ------------- | ----------- | ---------- | ----------------------- | ------------- |
| `id`                       | 'AutoField`     |               |
| `first_name`               | `CharField`     |
| `last_name`                | `CharField`     |
| `email`                    | `EmailField`    |
| `phone_number`             | `CharField`     |
| `alternate_phone_number`   | `CharField`     |
| `preferred_contact_method` | `CharField`     |
| `emergency_contact_name`   | `CharField`     |
| `emergency_contact_phone`  | `CharField`     |
| `notes`                    | `TextField`     |
| `client_status`            | `CharField`     |
| `referral_source`          | `CharField`     |
| `is_active`                | `BooleanField`  |
| `created_at`               | `DateTimeField` |
| `updated_at`               | `DateTimeField` |

## Validators

## Serializers

## String Representation

## Methods

`get_full_name(self)` - Returns the client's full name

**Returns:** `first_name` `last_name` ("Keith Hiamond")

## Meta Information

- `ordering = ['last_name', 'first_name']`: Specifies that when querying multiple `Client` objects without an explicit `order_by()` clause, the results should be sorted primarily by `last_name` (ascending) and secondarily by `first_name` (ascending).
- `verbose_name = "Client"`: Sets the user-friendly singular name for the model, used in the Django admin interface ("Add Client")
- `verbose_name_plural = "Clients"`: Sets the user-friendly plural name for the model, used in the Django admin interface ("View Clients")

## JSON Structure
