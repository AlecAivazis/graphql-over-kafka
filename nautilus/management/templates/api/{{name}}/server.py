# external imports
import nautilus

class {{name.title()}}Service(nautilus.APIGateway):

    # Warning: This key should not be shared anywhere. Be careful when
    #          comittting this service to version control to move this value
    #          to an environment variable
    secret_key = '{{secret_key}}'
