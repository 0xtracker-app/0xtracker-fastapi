geysers = "query getGeysers {\n\tgeysers {\n    id\n  }\n}"

user_vaults = "query getUserVault ($user: ID!) {\n  \t\tuser(id: $user){\n      vaults {\n        id\n      }\n    }\n}"