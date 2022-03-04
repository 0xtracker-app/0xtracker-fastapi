from databases import Database


class PostGresDataBase:
    client: Database = None


postdb = PostGresDataBase()


async def get_postgres_database() -> Database:
    return postdb