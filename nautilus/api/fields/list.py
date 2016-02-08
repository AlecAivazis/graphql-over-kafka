# external imports
from graphene import Field
from graphene import List as GrapheneList

def List(target, **kwds):
    return Field(GrapheneList(target), **kwds)
