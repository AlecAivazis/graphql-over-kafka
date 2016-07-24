def summarize_mutation_io(name, type, required=False):
    """
        This function returns the standard summary for mutations inputs
        and outputs
    """
    return dict(
        name=name,
        type=type,
        required=required
    )