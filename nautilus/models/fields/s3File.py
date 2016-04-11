# external imports
import tempfile
import mimetypes
from nautilus.models import Field

class S3File(Field):
    """
        This type decorator takes a python file and uploads it to the service's bucket
        (specified in the config). If a string is given instead, this field will parse
        the string for image information and create a temporary file to upload. When
        retrieving the value from the database, a string will be returned with a
        pre-signed url for universal-access of the file.
    """
    db_field = 'varchar'
    folder = '' # this will get prepended to the file path
    deliminator = ':'

    def db_value(self, value, dialect):
        """
            Upload the given file to s3 and turn it into the necessary data to persist
            an s3 location given a python File object. The location of the file is persisted
            in the database as a string of the form <bucket><self.deliminator><key>.
        """
        if value is not None:

            # we might need to create a temporary file and check for it later
            created_temp_file = False

            # if the new value is a string
            if isinstance(value, str):
                # we need to turn it into a file so create an empty one
                value = tempfile.NamedTemporaryFile(delete=True)

                # treat the value like a base 64 encoded file and separate the relevant data
                [head, file_contents] = value.split(',')
                mimetype = head.split(';')[0].split(':')[1]
                extension = mimetypes.guess_extension(mimetype)

                # set the file name
                value.name = "{}{}".format(name, extension)
                # write the file contents
                value.write(standard_b64decode(file_contents))

                # make sure we clear the temporary file
                created_temp_file = True

            # now that the value is hopefully a file
            try:
                # make sure that's the case
                assert isinstance(value, tempfile.NamedTemporaryFile), (
                    'S3File can only accept files or strings.'
                )

                # get the s3 service resource
                s3 = boto3.resource('s3')
                # the name of the bucket
                bucket = current_app.config['AWS_BUCKET']

                # grab the name of the file
                filename = value.name
                # the target location to upload the file
                target_file = "{}/{}".format(self.folder, filename) if self.bucket \
                                                                        else filename
                # upload the file to s3
                s3.upload_file(filename, bucket, target_file)

            # cleanup after uploading
            finally:
                # if we created a temporary file
                if created_temp_file:
                    # close and delete the file
                    value.close()

            # store the s3 file location in a retrievable manner
            return "{}{}{}".format(bucket, self.deliminator, filename)


    def python_value(self, value, dialect):
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
