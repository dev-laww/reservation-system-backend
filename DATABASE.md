# Database Models

## Table of Contents

- [User](#user)
- [Property](#property)
- [Image](#image)
- [Review](#review)
- [Booking](#booking)
- [Notification](#notification)
- [Payment](#payment)

## User

| Field      | Type    | Description                    |
|------------|---------|--------------------------------|
| id         | Integer | Unique identifier for the user |
| email      | String  | User's email address           |
| password   | String  | User's password                |
| first_name | String  | User's first name              |
| last_name  | String  | User's last name               |
| phone      | String  | User's phone number            |
| admin      | Boolean | User's admin status            |

## Property

| Field       | Type    | Description                        |
|-------------|---------|------------------------------------|
| id          | Integer | Unique identifier for the property |
| name        | String  | Property's name                    |
| description | String  | Property's description             |
| type        | String  | Property's type                    |
| address     | String  | Property's address                 |
| city        | String  | Property's city                    |
| state       | String  | Property's state                   |
| zip         | String  | Property's zip code                |

## Image

| Field      | Type    | Description                     |
|------------|---------|---------------------------------|
| id         | Integer | Unique identifier for the image |
| url        | String  | Image's url                     |
| propertyId | Integer | Property's id                   |

## Review

| Field       | Type    | Description                      |
|-------------|---------|----------------------------------|
| id          | Integer | Unique identifier for the review |
| user_id     | Integer | User's id                        |
| property_id | Integer | Property's id                    |
| rating      | Integer | Review's rating                  |
| comment     | String  | Review's comment                 |

## Booking

| Field       | Type    | Description                       |
|-------------|---------|-----------------------------------|
| id          | Integer | Unique identifier for the booking |
| user_id     | Integer | User's id                         |
| property_id | Integer | Property's id                     |
| start_date  | Date    | Booking's start date              |
| end_date    | Date    | Booking's end date                |
| status      | String  | Booking's status                  |

## Notification

| Field   | Type    | Description                            |
|---------|---------|----------------------------------------|
| id      | Integer | Unique identifier for the Notification |
| user_id | Integer | User's id                              |
| message | String  | Notification's message                 |
| seen    | Boolean | Notification's seen status             |
| seen_at | Date    | Notification's seen date               |

## Payment

| Field       | Type    | Description                       |
|-------------|---------|-----------------------------------|
| id          | Integer | Unique identifier for the payment |
| user_id     | Integer | User's id                         |
| property_id | Integer | Property's id                     |
| amount      | Integer | Payment's amount                  |
| status      | String  | Payment's status                  |
| created_at  | Date    | Payment's created date            |
| updated_at  | Date    | Payment's updated date            |
