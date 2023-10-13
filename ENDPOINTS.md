# API Endpoints

List of all api endpoints.

### Table of Contents

- [Auth](#auth)
    - [Login](#login)
    - [Register](#register)
    - [Refresh Token](#refresh-token)
    - [Forgot Password](#forgot-password)
    - [Reset Password](#reset-password)
- [Profile](#profile)
    - [Get Profile](#get-profile)
    - [Update Profile](#update-profile)
    - [Change Password](#change-password)
    - [Notifications](#profile-notifications)
        - [Get Notifications](#get-notifications)
        - [Mark Notification as Read](#mark-notification-as-read)
        - [Mark All Notifications as Read](#mark-all-notifications-as-read)
    - [Bookings](#profile-bookings)
        - [Get Bookings](#get-bookings)
        - [Get Booking](#get-booking)
        - [Cancel Booking](#cancel-booking)
- [Tenants](#tenants)
    - [Get Tenants](#get-tenants)
    - [Get Tenant](#get-tenant)
    - [Send Notification to Tenant](#send-notification-to-tenant)
- [Properties](#properties)
    - [Get Properties](#get-properties)
    - [Get Property](#get-property)
    - [Create Property](#create-property)
    - [Update Property](#update-property)
    - [Delete Property](#delete-property)
    - [Upload Property Image](#upload-property-image)
    - [Reviews](#property-reviews)
        - [Get Property Reviews](#get-property-reviews)
        - [Add Property Review](#add-property-review)
        - [Update Property Review](#update-property-review)
        - [Delete Property Review](#delete-property-review)
    - [Bookings](#property-bookings)
        - [Get Property Bookings](#get-property-bookings)
        - [Book Property](#book-property)
    - [Tenants](#property-tenants)
        - [Get Property Tenants](#get-property-tenants)
        - [Add Tenant to Property](#add-tenant-to-property)
        - [Remove Tenant from Property](#remove-tenant-from-property)
- [Payments](#payments)
    - [Get Payments](#get-payments)
    - [Get Payment](#get-payment)
    - [Mark Payment as Paid](#mark-payment-as-completed)
    - [Mark Payment as Declined](#mark-payment-as-declined)
    - [Delete Payment](#delete-payment)
- [Common Responses](#common-responses)
    - [Success](#success)
    - [Error](#error)
    - [Validation Error](#validation-error)
    - [Unauthorized](#unauthorized)
    - [Forbidden](#forbidden)
    - [Not Found](#not-found)
    - [Method Not Allowed](#method-not-allowed)
    - [Internal Server Error](#internal-server-error)

# Auth

## Login

```http request
POST /auth/login
```

### Request

```json
{
  "email": "test@mail.com",
  "password": "secretpassword"
}
```

### Response

```json
{
  "status": "success",
  "message": "Login successful",
  "userId": "<user-id>",
  "firstName": "John",
  "lastName": "Doe",
  "email": "johndoe@mail.com",
  "accessToken": "<access-token>",
  "refreshToken": "<refresh-token>"
}
```

## Register

```http request
POST /auth/register
```

### Request

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "johndoe@mail.com",
  "phoneNumber": "+254712345678",
  "password": "secretpassword",
  "passwordConfirmation": "secretpassword"
}
```

### Response

```json
{
  "status": "success",
  "message": "Registration successful",
  "userId": "<user-id>",
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "+254712345678",
  "email": "johndoe@mail.com",
  "accessToken": "<access-token>",
  "refreshToken": "<refresh-token>"
}
```

## Refresh Token

```http request
POST /auth/refresh-token
```

### Request

```json
{
  "token": "<refresh-token>"
}
```

### Response

```json
{
  "status": "success",
  "message": "Token refreshed",
  "data": {
    "accessToken": "<access-token>"
  }
}
```

## Forgot Password

```http request
POST /auth/forgot-password
```

### Request

```json
{
  "email": "test@mail.com"
}
```

### Response

```json
{
  "status": "success",
  "message": "Password reset email sent"
}
```

## Reset Password

```http request
POST /auth/reset-password
```

### Request

```json
{
  "refreshToken": "<refresh-token>",
  "password": "newsecretpassword"
}
```

### Response

```json
{
  "status": "success",
  "message": "Password reset successful"
}
```

# Profile

- Requires authentication

## Get Profile

```http request
GET /profile
```

### Response

```json
{
  "status": "success",
  "message": "Profile retrieved",
  "data": {
    "id": "<user-id>",
    "firstName": "John",
    "lastName": "Doe",
    "phoneNumber": "+254712345678",
    "email": "johndoe@mail.com",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Update Profile

```http request
PUT /profile
```

### Request

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "+254712345678"
}
```

### Response

```json
{
  "status": "success",
  "message": "Profile updated",
  "data": {
    "id": "<user-id>",
    "firstName": "John",
    "lastName": "Doe",
    "phoneNumber": "+254712345678",
    "email": "johndoe@mail.com",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Change Password

- Requires authentication

```http request
PUT /profile/change-password
```

### Request

```json
{
  "oldPassword": "oldsecretpassword",
  "newPassword": "newsecretpassword",
  "confirmPassword": "newsecretpassword"
}
```

### Response

```json
{
  "status": "success",
  "message": "Password changed"
}
```

## Profile Notifications

- Requires authentication

### Get Notifications

```http request
GET /profile/notifications
```

### Response

```json
{
  "status": "success",
  "message": "Notifications retrieved",
  "data": [
    {
      "id": "<notification-id>",
      "type": "booking",
      "message": "Booking request for <property-name> has been accepted",
      "seen": false,
      "createdAt": "2021-01-01T00:00:00.000Z",
      "seenAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

### Mark Notification as Read

```http request
PUT /profile/notifications/<notification-id>
```

### Response

```json
{
  "status": "success",
  "message": "Notification marked as read"
}
```

### Mark All Notifications as Read

```http request
PUT /profile/notifications
```

### Response

```json
{
  "status": "success",
  "message": "Notifications marked as read"
}
```

## Profile Bookings

- Requires authentication

### Get Bookings

```http request
GET /profile/bookings
```

### Response

```json
{
  "status": "success",
  "message": "Bookings retrieved",
  "data": [
    {
      "id": "<booking-id>",
      "propertyId": "<property-id>",
      "startDate": "2021-01-01",
      "endDate": "2021-01-01",
      "status": "pending",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

### Get Booking

- Requires authentication

```http request
GET /profile/bookings/<booking-id>
```

### Response

```json
{
  "status": "success",
  "message": "Booking retrieved",
  "data": {
    "id": "<booking-id>",
    "propertyId": "<property-id>",
    "startDate": "2021-01-01",
    "endDate": "2021-01-01",
    "status": "pending",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

### Cancel Booking

- Requires authentication

```http request
POST /profile/bookings/<booking-id>
```

### Response

```json
{
  "status": "success",
  "message": "Booking cancelled"
}
```

# Tenants

## Get Tenants

- Requires authentication
- Requires admin privileges

```http request
GET /tenants
```

### Response

```json
{
  "status": "success",
  "message": "Tenants retrieved",
  "data": [
    {
      "id": "<user-id>",
      "firstName": "John",
      "propertyId": "<property-id>",
      "lastName": "Doe",
      "phoneNumber": "+254712345678",
      "email": "johndoe@mail.com",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

## Get Tenant

- Requires authentication
- Requires admin privileges

```http request
GET /tenants/<user-id>
```

### Response

```json
{
  "status": "success",
  "message": "Tenant retrieved",
  "data": {
    "id": "<user-id>",
    "firstName": "John",
    "propertyId": "<property-id>",
    "lastName": "Doe",
    "phoneNumber": "+254712345678",
    "email": "johndoe@mail.com",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Send Notification to Tenant

- Requires authentication
- Requires admin privileges

```http request
POST /tenants/<user-id>/notifications
```

### Request

```json
{
  "message": "Notification message"
}
```

### Response

```json
{
  "status": "success",
  "message": "Notification sent"
}
```

# Properties

## Get Properties

```http request
GET /properties
```

### Response

```json
{
  "status": "success",
  "message": "Properties retrieved",
  "data": [
    {
      "id": "<property-id>",
      "name": "Property Name",
      "description": "Property description",
      "location": "Property location",
      "price": 1000,
      "ownerId": "<user-id>",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z",
      "images": [
        {
          "id": "<image-id>",
          "url": "https://property-image-url.com",
          "createdAt": "2021-01-01T00:00:00.000Z",
          "updatedAt": "2021-01-01T00:00:00.000Z"
        }
      ],
      "reviews": [
        {
          "id": "<review-id>",
          "propertyId": "<property-id>",
          "userId": "<user-id>",
          "rating": 5,
          "comment": "Review comment",
          "createdAt": "2021-01-01T00:00:00.000Z",
          "updatedAt": "2021-01-01T00:00:00.000Z"
        }
      ]
    }
  ]
}
```

## Get Property

```http request
GET /properties/<property-id>
```

### Response

```json
{
  "status": "success",
  "message": "Property retrieved",
  "data": {
    "id": "<property-id>",
    "name": "Property Name",
    "description": "Property description",
    "location": "Property location",
    "price": 1000,
    "ownerId": "<user-id>",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z",
    "images": [
      {
        "id": "<image-id>",
        "url": "https://property-image-url.com",
        "createdAt": "2021-01-01T00:00:00.000Z",
        "updatedAt": "2021-01-01T00:00:00.000Z"
      }
    ],
    "reviews": [
      {
        "id": "<review-id>",
        "propertyId": "<property-id>",
        "userId": "<user-id>",
        "rating": 5,
        "comment": "Review comment",
        "createdAt": "2021-01-01T00:00:00.000Z",
        "updatedAt": "2021-01-01T00:00:00.000Z"
      }
    ]
  }
}
```

## Create Property

- Requires authentication
- Requires admin privileges

```http request
POST /properties
```

### Request

```json
{
  "name": "Property Name",
  "description": "Property description",
  "address": "Property address",
  "city": "Property city",
  "state": "Property state",
  "zip": "Property zip",
  "type": "Property type",
  "price": 1000,
  "maxOccupancy": 5
}
```

### Response

```json
{
  "status": "success",
  "message": "Property created",
  "data": {
    "id": "<property-id>",
    "name": "Property Name",
    "description": "Property description",
    "address": "Property address",
    "city": "Property city",
    "state": "Property state",
    "zip": "Property zip",
    "type": "Property type",
    "price": 1000,
    "maxOccupancy": 5,
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z",
    "images": [],
    "reviews": []
  }
}
```

## Update Property

- Requires authentication
- Requires admin privileges

```http request
PUT /properties/<property-id>
```

### Request

```json
{
  "name": "Property Name",
  "description": "Property description",
  "address": "Property address",
  "city": "Property city",
  "state": "Property state",
  "zip": "Property zip",
  "type": "Property type",
  "price": 1000,
  "maxOccupancy": 5
}
```

### Response

```json
{
  "status": "success",
  "message": "Property updated",
  "data": {
    "id": "<property-id>",
    "name": "Property Name",
    "description": "Property description",
    "address": "Property address",
    "city": "Property city",
    "state": "Property state",
    "zip": "Property zip",
    "type": "Property type",
    "price": 1000,
    "maxOccupancy": 5,
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z",
    "images": [],
    "reviews": []
  }
}
```

## Delete Property

- Requires authentication
- Requires admin privileges

```http request
DELETE /properties/<property-id>
```

### Response

```json
{
  "status": "success",
  "message": "Property deleted"
}
```

## Upload Property Image

- Requires authentication
- Requires admin privileges

```http request
POST /properties/<property-id>/images
```

### Request
- Form data

```json
{
  "image": "<image-file>"
}
```

### Response

```json
{
  "status": "success",
  "message": "Image uploaded",
  "data": {
    "id": "<image-id>",
    "url": "https://property-image-url.com",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Property Reviews

### Get Property Reviews

```http request
GET /properties/<property-id>/reviews
```

### Response

```json
{
  "status": "success",
  "message": "Reviews retrieved",
  "data": [
    {
      "id": "<review-id>",
      "propertyId": "<property-id>",
      "userId": "<user-id>",
      "rating": 5,
      "comment": "Review comment",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

### Add Property Review

- Requires authentication

```http request
POST /properties/<property-id>/reviews
```

### Request

```json
{
  "rating": 5,
  "comment": "Review comment"
}
```

### Response

```json
{
  "status": "success",
  "message": "Review added",
  "data": {
    "id": "<review-id>",
    "propertyId": "<property-id>",
    "userId": "<user-id>",
    "rating": 5,
    "comment": "Review comment",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

### Update Property Review

- Requires authentication

```http request
PUT /properties/<property-id>/reviews/<review-id>
```

### Request

```json
{
  "rating": 5,
  "comment": "Review comment"
}
```

### Response

```json
{
  "status": "success",
  "message": "Review updated",
  "data": {
    "id": "<review-id>",
    "propertyId": "<property-id>",
    "userId": "<user-id>",
    "rating": 5,
    "comment": "Review comment",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

### Delete Property Review

- Requires authentication

```http request
DELETE /properties/<property-id>/reviews/<review-id>
```

### Response

```json
{
  "status": "success",
  "message": "Review deleted"
}
```

## Property Bookings

### Get Property Bookings

```http request
GET /properties/<property-id>/bookings
```

### Response

```json
{
  "status": "success",
  "message": "Bookings retrieved",
  "data": [
    {
      "id": "<booking-id>",
      "propertyId": "<property-id>",
      "startDate": "2021-01-01",
      "endDate": "2021-01-01",
      "status": "pending",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

### Book Property

- Requires authentication

```http request
POST /properties/<property-id>/bookings
```

### Request

```json
{
  "startDate": "2021-01-01",
  "endDate": "2021-01-01"
}
```

### Response

```json
{
  "status": "success",
  "message": "Booking request sent",
  "data": {
    "id": "<booking-id>",
    "propertyId": "<property-id>",
    "startDate": "2021-01-01",
    "endDate": "2021-01-01",
    "status": "pending",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Property Tenants

### Get Property Tenants

```http request
GET /properties/<property-id>/tenants
```

### Response

```json
{
  "status": "success",
  "message": "Tenants retrieved",
  "data": [
    {
      "id": "<user-id>",
      "firstName": "John",
      "propertyId": "<property-id>",
      "lastName": "Doe",
      "phoneNumber": "+254712345678",
      "email": "johndoe@mail.com"
    }
  ]
}
```

### Add Tenant to Property

- Requires authentication
- Requires admin privileges

```http request
POST /properties/<property-id>/tenants/<user-id>
```

### Response

```json
{
  "status": "success",
  "message": "Tenant added"
}
```

### Remove Tenant from Property

- Requires authentication
- Requires admin privileges

```http request
DELETE /properties/<property-id>/tenants/<user-id>
```

### Response

```json
{
  "status": "success",
  "message": "Tenant removed"
}
```

# Payments

## Get Payments

- Requires authentication
- Requires admin privileges

```http request
GET /payments
```

### Response

```json
{
  "status": "success",
  "message": "Payments retrieved",
  "data": [
    {
      "id": "<payment-id>",
      "propertyId": "<property-id>",
      "tenantId": "<user-id>",
      "amount": 1000,
      "status": "pending",
      "createdAt": "2021-01-01T00:00:00.000Z",
      "updatedAt": "2021-01-01T00:00:00.000Z"
    }
  ]
}
```

## Get Payment

- Requires authentication
- Requires admin privileges

```http request
GET /payments/<payment-id>
```

### Response

```json
{
  "status": "success",
  "message": "Payment retrieved",
  "data": {
    "id": "<payment-id>",
    "propertyId": "<property-id>",
    "tenantId": "<user-id>",
    "amount": 1000,
    "status": "pending",
    "createdAt": "2021-01-01T00:00:00.000Z",
    "updatedAt": "2021-01-01T00:00:00.000Z"
  }
}
```

## Mark Payment as Completed

- Requires authentication
- Requires admin privileges

```http request
POST /payments/<payment-id>/complete
```

### Response

```json
{
  "status": "success",
  "message": "Payment marked as completed"
}
```

## Mark Payment as Declined

- Requires authentication
- Requires admin privileges

```http request
POST /payments/<payment-id>/decline
```

### Response

```json
{
  "status": "success",
  "message": "Payment marked as declined"
}
```

## Delete Payment

- Requires authentication
- Requires admin privileges

```http request
DELETE /payments/<payment-id>
```

## Response

```json
{
  "status": "success",
  "message": "Payment deleted"
}
```

# Common Responses

## Success

```json
{
  "status": "success",
  "message": "Success message",
  "data": {
    "key": "value"
  }
}
```

## Error

```json
{
  "status": "error",
  "message": "Error message"
}
```

## Validation Error

```json
{
  "status": "error",
  "message": "Validation error",
  "data": {
    "errors": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

## Unauthorized

```json
{
  "status": "error",
  "message": "Unauthorized"
}
```

## Forbidden

```json
{
  "status": "error",
  "message": "Forbidden"
}
```

## Not Found

```json
{
  "status": "error",
  "message": "Not found"
}
```

## Method Not Allowed

```json
{
  "status": "error",
  "message": "Method not allowed"
}
```

## Internal Server Error

```json
{
  "status": "error",
  "message": "Internal server error"
}
```
