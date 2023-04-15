"""Module for AnimalShelter class"""
from pymongo import MongoClient, errors
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult


class AnimalShelter:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self,
                 username: str,
                 password: str,
                 port: int = 27017,
                 auth_src_db: str = 'admin') -> None:
        """AnimalShelter constructor"""
        try:
            auth_source = f'authSource={auth_src_db}' if auth_src_db is not None else ''
            # Initializing the MongoClient using parameters
            self.client = MongoClient(f'mongodb://{username}:{password}'
                                      f'@localhost:{port}/?'
                                      f'{auth_source}')
        except errors.ConnectionFailure:
            print('Unable to initialize connection')
        try:
            # Load the aac shelter outcome database
            self.database = self.client['AAC']
            self.collection = self.database['animals']
        except errors.CollectionInvalid:
            print("Unable to load 'AAC' database")

    def create(self, data: dict) -> bool:
        """Attempts to add a document to the database"""
        create_successful = None
        # If data has a value, attempt to insert document in the db
        if data is not None:
            try:
                # Returns true if document added, otherwise returns false
                create_successful = self.collection.insert_one(data)
            except errors.WriteError:
                print(f'Unable to create {data}')
        # If data has no value, throw an exception
        else:
            raise TypeError('Nothing to save, because data parameter is empty')
        # Returns True if document was created successfully, otherwise returns False
        return create_successful.acknowledged

    def read(self, query: str = None) -> Cursor:
        """Search db for query and returns any results"""
        return self.collection.find(query, {"_id": False})

    def update(self, key: dict, data: dict) -> UpdateResult:
        """Search db for documents matching key and update with data argument"""
        return self.collection.update_many(key, data)

    def delete(self, key: dict) -> DeleteResult:
        """Search db for documents matching key and deletes them"""
        return self.collection.delete_many(key)
