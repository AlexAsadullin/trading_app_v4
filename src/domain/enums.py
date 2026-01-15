from enum import StrEnum


class TokenErrorCode(StrEnum):
    expired = "expired"
    invalid = "invalid"


class TokenType(StrEnum):
    access_token = "access_token"
    refresh_token = "refresh_token"


class UserType(StrEnum):
    human = "human"
    ai = "ai"


class MessageType(StrEnum):
    text = "text"
    product_capsule = "product-capsule"
    economy_capsule = "economy-capsule"


class Environment(StrEnum):
    production = "production"
    staging = "staging"
    dev = "dev"
    local = "local"


class OfferRequestStatus(StrEnum):
    draft = "draft"
    rfq = "rfq"
    samples = "samples"
    to_buy = "to_buy"
    in_order = "in_order"
