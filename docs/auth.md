

# DRF/React User Management 
Client and Staff Roles with Client Activation
## 1. Django Models
- **`user_management_app.User`**: custom user model (inheriting from `AbstractUser`).
- **`client_management_app.ClientProfile`**: Contains client-specific information. Nullable `OneToOneField` to `User`

## 2. Authentication (DRF + Tokens)
**Token Strategy:**
- `JWT` (JSON Web Tokens): Highly recommended for SPAs. Use `djangorestframework-simplejwt`- Provides refresh tokens and token expiration, enhancing security.
- DRF's Built-in `TokenAuthentication`: Uses persistent tokens stored in the database.
- CORS (Cross-Origin Resource Sharing): `django-cors-headers`

## 3. Serializers (DRF)
### UserSerializer

* **Purpose:** For displaying user details after login, for profile views
* **Key Feature:** Excludes sensitive fields like `password`.
* **Variations:** `StaffUserSerializer` showing more admin details vs. a `ClientUserSerializer`

### ClientProfileSerializer

* **Purpose:** Used by staff for CRUD (Create, Read, Update, Delete) operations on existing `ClientProfile` records (specifically GET, PUT, PATCH methods).
* **Fields:** Includes profile fields and user field details (which might be read-only or use a nested `UserSerializer`).

### StaffClientProfileCreateSerializer

* **Purpose:** Used exclusively by staff via a protected endpoint to create a new `ClientProfile` *before* the associated client user account exists.
* **Fields:** Includes only profile-specific fields (e.g., `email`, `full_name`, `company_name`).
* **Exclusions:** Does **not** include the `user` field.

### ClientActivationCheckSerializer

* **Purpose:** Used in the first step of the public client activation process to verify if a pending profile exists for a given email.
* **Input:** `{ "email": "client@email.com" }`

### ClientActivationCompleteSerializer

* **Purpose:** Used in the final step of the public client activation process.
* **Input:** `{ "email": "...", "password": "...", "password_confirm": "..." }`
* **Functionality:**
    * Validates that `password` and `password_confirm` fields match.
    * Includes the necessary fields to create the associated `User` account upon successful validation.

### LoginSerializer

* **Source:** Typically provided by authentication libraries like `dj-rest-auth` or `djoser`.
* **Purpose:** Handles user login requests.
* **Input:** `{ "email": "...", "password": "..." }` (or potentially `username` instead of `email`).

## 4. API Endpoints (DRF APIView)

### Staff-Only Endpoints 
`/api/v1/staff/`
#### POST /api/v1/staff/client-profiles/
- **Action:** Create a new `ClientProfile` (without linking a user yet).
- **Authentication:** Requires Staff authentication token (`IsAuthenticated`, `IsStaffUser` permission).
- **Serializer:** `StaffClientProfileCreateSerializer`
- **Logic:** Saves a new `ClientProfile` instance with `user=None`. The provided `email` is stored on the profile itself for later lookup during activation.
#### GET /api/v1/staff/client-profiles/
- **Action:** List all client profiles.
- **Authentication:** Staff Token.
- **Serializer:** `ClientProfileSerializer`.
#### GET, PUT, PATCH, DELETE /api/v1/staff/client-profiles/{pk}/`
- **Action:** Retrieve, update, partially update, or delete a specific client profile.
- **Authentication:** Staff Token.
- **Serializer:** `ClientProfileSerializer`.
### Client Activation Endpoints (Public - No Auth Required Initially)
#### POST /api/v1/client/activation/check-profile/
- **Action:** Check if an inactive client profile exists for the given email.
- **Authentication:** Public.
- **Request Body:** `{ "email": "client@email.com" }`
- **Serializer:** `ClientActivationCheckSerializer` (for validation).
- **Logic:**
  - Validate input `email` format.
  - Query `ClientProfile` where `email=input_email` and `user=None`.
  - Return `200 OK` (or `204 No Content`) if found.
  - Return `404 Not Found` if no matching profile exists or if it's already linked (user is not None).
  - Return `400 Bad Request` for invalid `email` format.
- **React Usage:** Frontend calls this first. If successful (`2xx`), it shows the password creation form.
#### POST /api/v1/client/activation/complete/
- **Action:** Create the User account, link it to the `ClientProfile`, and log the new client in.
- **Authentication:** Public.
- **Request Body:**
```
{ "email": "...", "password": "...", "password_confirm": "..." }
```
- **Serializer:** `ClientActivationCompleteSerializer` (validates passwords match).
- **Logic:**
  - Validate input using the serializer.
  - Re-verify: Find the `ClientProfile` where `email=input_email` and `user=None`. Return `404` or `400` if not found or already active.
  - Create the accounts.
    - User: `User.objects.create_user(...)` Set `is_client=True`, `is_active=True`.
    - Populate fields `email`, `first_name`, `last_name` from the profile data.
    - Set the validated `password`.
  - Link Profile: `profile.user = new_user` and `rofile.save()`
  - Generate Tokens: Create JWT access/refresh tokens (or a DRF token) for `new_user`.
  - Return Response: Return `200 OK` or `201 Created` with the authentication tokens and potentially basic user info (`UserSerializer`).
  - React Usage: Frontend calls this after the user submits the password form. On success, it stores the tokens securely and redirects the user to the client dashboard.
### Standard Authentication Endpoints
#### POST /api/v1/auth/login/
- **Authentication:** Public.
- **Action:** Authenticates existing users (both clients and staff).
- **Returns:** Auth tokens (JWT access/refresh or DRF token) and user details (including `is_client`, `is_staff_member` flags).
#### POST /api/v1/auth/logout/
- **Authentication:** Requires valid Auth Token.
- **Action:** Invalidates the token
- **Password Reset Endpoints:** `/api/v1/auth/password/reset/`
### Protected Data Endpoints (Require Auth Token)
#### GET /api/v1/client/...
- **Authentication:** Requires valid Auth Token (`IsAuthenticated`).
- **Permissions:** Use custom permissions (`IsClientUser`).
#### GET /api/v1/staff/users/...
- **Authentication:** Requires valid Auth Token (`IsAuthenticated`).
- **Permissions:** Use custom permissions (`IsStaffUser`).
### Permissions
`rest_framework.permissions.IsAuthenticated`: Base check for logged-in users.
### Custom Permissions:
#### IsClientUser(BasePermission)
Checks `request.user.is_authenticated` and `request.user.is_client`.
#### IsStaffUser(BasePermission) 
Checks request.user.is_authenticated and `request.user.is_staff_member`\
`permission_classes = [IsAuthenticated, IsClientUser]`

## 5. React Frontend
