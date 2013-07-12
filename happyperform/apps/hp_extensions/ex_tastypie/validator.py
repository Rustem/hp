from tastypie.validation import CleanedDataFormValidation as OldCleanedDataFormValidation
from hp_extensions.utils import document_to_dict


class CleanedDataFormValidation(OldCleanedDataFormValidation):

    def form_args(self, bundle):
        data = bundle.data

        if data is None:
            data = {}

        kwargs = {'data': {}}

        if hasattr(bundle.obj, 'pk'):
            kwargs.update({
                "instance": bundle.obj,
                "data": document_to_dict(bundle.obj)})
        kwargs['data'].update(data)
        return kwargs
