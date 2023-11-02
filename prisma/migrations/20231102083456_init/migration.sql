-- CreateEnum
CREATE TYPE "TokenType" AS ENUM ('reset');

-- CreateEnum
CREATE TYPE "PaymentType" AS ENUM ('cash', 'ewallet');

-- CreateEnum
CREATE TYPE "RentalStatus" AS ENUM ('pending', 'approved', 'declined', 'canceled');

-- CreateEnum
CREATE TYPE "Status" AS ENUM ('pending', 'paid', 'declined');

-- CreateEnum
CREATE TYPE "PropertyType" AS ENUM ('house', 'studio', 'one_bedroom', 'two_bedroom');

-- CreateTable
CREATE TABLE "users"
(
    "id"           SERIAL       NOT NULL,
    "property_id"  INTEGER,
    "email"        TEXT         NOT NULL,
    "first_name"   TEXT         NOT NULL,
    "last_name"    TEXT         NOT NULL,
    "password"     TEXT         NOT NULL,
    "phone_number" TEXT         NOT NULL,
    "admin"        BOOLEAN      NOT NULL DEFAULT false,
    "created_at"   TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"   TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "users_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "properties"
(
    "id"          SERIAL           NOT NULL,
    "price"       DOUBLE PRECISION NOT NULL,
    "name"        TEXT             NOT NULL,
    "description" TEXT             NOT NULL,
    "type"        "PropertyType"   NOT NULL,
    "address"     TEXT             NOT NULL,
    "city"        TEXT             NOT NULL,
    "state"       TEXT             NOT NULL,
    "zip"         TEXT             NOT NULL,
    "created_at"  TIMESTAMP(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"  TIMESTAMP(3)     NOT NULL,
    "tenant_id"   INTEGER,

    CONSTRAINT "properties_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "properties_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "images"
(
    "id"          SERIAL       NOT NULL,
    "property_id" INTEGER      NOT NULL,
    "url"         TEXT         NOT NULL,
    "created_at"  TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"  TIMESTAMP(3) NOT NULL,

    CONSTRAINT "images_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "images_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "reviews"
(
    "id"          SERIAL       NOT NULL,
    "user_id"     INTEGER      NOT NULL,
    "property_id" INTEGER      NOT NULL,
    "rating"      INTEGER      NOT NULL,
    "comment"     TEXT         NOT NULL,
    "created_at"  TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"  TIMESTAMP(3) NOT NULL,

    CONSTRAINT "reviews_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "rentals"
(
    "id"          SERIAL         NOT NULL,
    "user_id"     INTEGER        NOT NULL,
    "property_id" INTEGER        NOT NULL,
    "start_date"  TIMESTAMP(3)   NOT NULL,
    "end_date"    TIMESTAMP(3)   NOT NULL,
    "status"      "RentalStatus" NOT NULL DEFAULT 'pending',
    "created_at"  TIMESTAMP(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"  TIMESTAMP(3)   NOT NULL,

    CONSTRAINT "rentals_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "rentals_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "notifications"
(
    "id"         SERIAL       NOT NULL,
    "user_id"    INTEGER      NOT NULL,
    "message"    TEXT         NOT NULL,
    "seen"       BOOLEAN      NOT NULL DEFAULT false,
    "created_by" TEXT         NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "seen_at"    TIMESTAMP(3) NOT NULL,

    CONSTRAINT "notifications_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "notifications_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "payments"
(
    "id"         SERIAL           NOT NULL,
    "user_id"    INTEGER          NOT NULL,
    "rental_id"  INTEGER          NOT NULL,
    "type"       "PaymentType"    NOT NULL DEFAULT 'cash',
    "amount"     DOUBLE PRECISION NOT NULL,
    "status"     "Status"         NOT NULL DEFAULT 'pending',
    "created_at" TIMESTAMP(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3)     NOT NULL,

    CONSTRAINT "payments_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "payments_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "access_tokens"
(
    "id"         SERIAL       NOT NULL,
    "user_id"    INTEGER      NOT NULL,
    "token"      TEXT         NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "access_tokens_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "access_tokens_id_seq" RESTART WITH 1000;

-- CreateTable
CREATE TABLE "email_tokens"
(
    "id"         SERIAL       NOT NULL,
    "email"      TEXT         NOT NULL,
    "token"      TEXT         NOT NULL,
    "type"       "TokenType"  NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "email_tokens_pkey" PRIMARY KEY ("id")
);

ALTER SEQUENCE "email_tokens_id_seq" RESTART WITH 1000;

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users" ("email");

-- CreateIndex
CREATE UNIQUE INDEX "properties_tenant_id_key" ON "properties" ("tenant_id");

-- CreateIndex
CREATE UNIQUE INDEX "payments_rental_id_key" ON "payments" ("rental_id");

-- CreateIndex
CREATE UNIQUE INDEX "access_tokens_token_key" ON "access_tokens" ("token");

-- CreateIndex
CREATE UNIQUE INDEX "email_tokens_token_key" ON "email_tokens" ("token");

-- AddForeignKey
ALTER TABLE "properties"
    ADD CONSTRAINT "properties_tenant_id_fkey" FOREIGN KEY ("tenant_id") REFERENCES "users" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "images"
    ADD CONSTRAINT "images_property_id_fkey" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "reviews"
    ADD CONSTRAINT "reviews_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "reviews"
    ADD CONSTRAINT "reviews_property_id_fkey" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "rentals"
    ADD CONSTRAINT "rentals_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "rentals"
    ADD CONSTRAINT "rentals_property_id_fkey" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "notifications"
    ADD CONSTRAINT "notifications_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "payments"
    ADD CONSTRAINT "payments_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "payments"
    ADD CONSTRAINT "payments_rental_id_fkey" FOREIGN KEY ("rental_id") REFERENCES "rentals" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "access_tokens"
    ADD CONSTRAINT "access_tokens_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "email_tokens"
    ADD CONSTRAINT "email_tokens_email_fkey" FOREIGN KEY ("email") REFERENCES "users" ("email") ON DELETE CASCADE ON UPDATE CASCADE;
