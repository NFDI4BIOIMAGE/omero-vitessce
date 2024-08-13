from django import forms


class ConfigForm(forms.Form):

    def __init__(self, file_names, file_urls,
                 img_names, img_urls, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)

        self.text_choices = [i for i in zip(file_urls, file_names)]
        self.image_choices = [i for i in zip(img_urls, img_names)]

        self.text_choices.insert(0, ('', '---'))

        # No empty default, we alway want an image in the config
        self.fields["image"] = forms.ChoiceField(
                choices=self.image_choices, required=True)

        # For other fields it is OK not to have an image
        self.image_choices.insert(0, ('', '---'))

        self.fields["segmentation"] = forms.ChoiceField(
                choices=self.image_choices, required=False)
        self.fields["cell identities"] = forms.ChoiceField(
                choices=self.text_choices, required=False)
        self.fields["expression"] = forms.ChoiceField(
                choices=self.text_choices, required=False)
