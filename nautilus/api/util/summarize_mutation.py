def summarize_mutation(mutation_name, event, inputs, outputs, isAsync=False):
    """
        This function provides a standard representation of mutations to be
        used when services announce themselves
    """
    return dict(
        name=mutation_name,
        event=event,
        isAsync=isAsync,
        inputs=inputs,
        outputs=outputs,
    )