class ModelAccess(object):

    # the string used as the key in the database (e.g. "foo_bar")
    key_string = None

    # the string meant to be human-readable (e.g. "Foo Bar")
    name = None

    # constructor, which should only be called once and then provide unlimited
    # uses of the model
    def __init__(self):
        raise NotImplementedError

    # INPUT: a Python dictionary representing all of the information about the patient
    #        that we have in the database. This function should extract the necessary
    #        information, and then run that information through the model.
    #        {
    #            "_id": "<ID number>",
    #            "name": "<name>",
    #            "age": "<age>",
    #            "gender": "<gender>",
    #            "chiefComplaint": "<complaint>",
    #            "admissionNote": "<admission note>"
    #        }
    # OUTPUT: the output of the model. The format details aren't important for now, as
    #        long as it makes sense.
    def get_result(self, patient):
        raise NotImplementedError

    # INPUT: a Python dictionary representing all of the information about the patient
    #        that we have in the database. This function should ensure that the patient
    #        can be run through the model (e.g. If we're trying to process a chest x-ray,
    #        this should only return True if the patient has a chest x-ray in their file
    # OUTPUT: boolean.
    # NOTE: for now, this is uncalled, and therefore optional
    def is_valid(self, patient):
        raise NotImplementedError
