# third party imports
import graphene

def graphql_type_from_summary(summary, connections):
    # the name of the type
    name = summary['name']
    # the fields of the type
    fields = {
        field['name']: getattr(graphene, field['type'])() \
                                    for field in summary['fields']
    }
    # add the connections to the model
    # for connection in connec
    connections = {
        field['name']: graphene.List(field['connection']['to']['service']) \
                                    for field in connections
    }
    # print(connections)
    # merge the two field dictionaries
    class_fields = {
        **fields,
        **connections
    }

    graphql_type = type(name, (graphene.ObjectType,), class_fields)
    graphql_type._service_name = name

    # create the class record for the model
    return graphql_type
