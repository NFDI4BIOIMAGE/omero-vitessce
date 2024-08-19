import datetime

from django import forms


class ConfigForm(forms.Form):
    """ Form used to collect the parameters used to
        automatically generate a config file for Vitessce
    """

    default_cell_id_col = "cell_id"
    default_label_col = "label"
    default_embedding_x_col = "UMAP_1"
    default_embedding_y_col = "UMAP_2"

    def __init__(self, file_names, file_urls,
                 img_names, img_urls, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)

        self.text_choices, self.image_choices = self.prepare_choices(
                file_names, file_urls, img_names, img_urls)

        filename = self.make_config_file_name()

        self.fields["config file name"] = forms.CharField(
                empty_value=filename, strip=True,
                min_length=1, max_length=40, required=False)

        # No empty default, we alway want an image in the config
        self.fields["image"] = forms.ChoiceField(
                choices=self.image_choices[1:], required=True)

        self.fields["segmentation"] = forms.ChoiceField(
                choices=self.image_choices, required=False)

        self.fields["cell identities"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["cell id column"] = forms.CharField(
                empty_value=ConfigForm.default_cell_id_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["label column"] = forms.CharField(
                empty_value=ConfigForm.default_label_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["expression"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["embeddings"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["embedding x"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_x_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["embedding y"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_y_col, strip=True,
                min_length=1, max_length=20, required=False)

        # Set default values for CharField fields
        self.fields["config file name"].initial = filename
        self.fields["cell id column"].initial = ConfigForm.default_cell_id_col
        self.fields["label column"].initial = ConfigForm.default_label_col
        self.fields["embedding x"].initial = ConfigForm.default_embedding_x_col
        self.fields["embedding y"].initial = ConfigForm.default_embedding_y_col

    def make_config_file_name(self):
        """ Creates the default config file name with a timestamp:
        VitessceConfig-yyyy.mm.dd_hhmmss.json.txt
        """
        ts = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")
        filename = "VitessceConfig-" + ts + ".json.txt"
        return filename

    def prepare_choices(self, file_names, file_urls, img_names, img_urls):
        """ Makes the lists of images and attached files for the form
        """
        self.text_choices = [i for i in zip(file_urls, file_names)]
        self.image_choices = [i for i in zip(img_urls, img_names)]

        self.text_choices.insert(0, ('', '---'))
        self.image_choices.insert(0, ('', '---'))

        return self.text_choices, self.image_choices
