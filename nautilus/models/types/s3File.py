# external imports
from sqlalchemy import Text, TypeDecorator
from graphene.core.types.scalars import String
# local imports
from nautilus.api import convert_sqlalchemy_type

class S3File(TypeDecorator):
    """
        This type decorator takes a python file and uploads it to the service's bucket
        (specified in the config). When retrieving the value from the database, a
        string will be returned with a pre-signed url for universal-access of the file.
    """
    impl = Text
    bucketDirectory = '' # this will get prepended to the
    deliminator = ':'

    def process_result_value(self, value, dialect):
        """
            Upload the given file to s3 and turn it into the necessary data to persist
            an s3 location given a python File object. The location of the file is persisted
            in the database as a string of the form <bucket><self.deliminator><key>.
        """
        if value is not None:
            # get the service resource
            s3 = boto3.resource('s3')
            # the name of the bucket
            bucket = currentApp.config['AWS_BUCKET']

            # grab the name of the file
            filename = value.name
            # if there is a bucket directory specified,
            if self.bucketDirectory:
                filename = "{}/{}".format(self.bucketDirectory, filename)

            # upload the file to s3
            s3.upload_file(filename, bucket, filename)

            # store the s3 file location in a retrievable manner
            return "{}{}{}".format(bucket, self.deliminator, filename)


    def process_bind_param(self, value, dialect):
        """
            Generate a pre-signed url for the s3 file designated by assuming its of the form
            <bucket><self.deliminator><key>.
        """
        if value is not None:
            # parse the databse value
            [bucket, key] = value.split(self.deliminator)

            # return the presigned url
            return boto3.resource('s3').generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucket,
                    'Key': key
                }
            )


# Graphene Support

@convert_sqlalchemy_type.register(S3File)
def convert_column_to_string(type, column):
    """ Covert the column to a string. """
    return String(description=column.doc)
