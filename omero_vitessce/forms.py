import datetime

from django import forms


class ConfigForm(forms.Form):
    """ Form used to collect the parameters used to
        automatically generate a config file for Vitessce
    """

    default_cell_id_col = "cell_id"
    default_cell_label_col = "label"
    default_embedding_x_col = "UMAP_1"
    default_embedding_y_col = "UMAP_2"
    default_molecule_id = "id"
    default_molecule_label = "gene"
    default_molecule_x_col = "x"
    default_molecule_y_col = "y"

    def __init__(self, file_names, file_urls,
                 img_names, img_urls, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)

        self.text_choices, self.image_choices = self.prepare_choices(
                file_names, file_urls, img_names, img_urls)

        filename = self.make_config_file_name()

        self.fields["config_file_name"] = forms.CharField(
                empty_value=filename, strip=True,
                min_length=1, max_length=40, required=False)

        # No empty default, we alway want an image in the config
        self.fields["image"] = forms.ChoiceField(
                choices=self.image_choices[1:], required=True)

        self.fields["segmentation"] = forms.ChoiceField(
                choices=self.image_choices, required=False)

        self.fields["cell_identities"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["cell_id_column"] = forms.CharField(
                empty_value=ConfigForm.default_cell_id_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["cell_label_column"] = forms.CharField(
                empty_value=ConfigForm.default_cell_label_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["expression"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["embeddings"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["embedding_x"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_x_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["embedding_y"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_y_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["molecules"] = forms.ChoiceField(
                choices=self.text_choices, required=False)

        self.fields["molecule_id"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_id, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["molecule_label"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_label, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["molecule_x"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_x_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["molecule_y"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_y_col, strip=True,
                min_length=1, max_length=20, required=False)

        self.fields["histograms"] = forms.BooleanField(initial=True,
                                                       required=False)
        self.fields["heatmap"] = forms.BooleanField(initial=True,
                                                    required=False)
        self.fields["status"] = forms.BooleanField(initial=False,
                                                   required=False)
        self.fields["description"] = forms.BooleanField(initial=False,
                                                        required=False)

        # Set default values for CharField fields
        self.fields["config_file_name"].initial = filename
        self.fields["cell_id_column"].initial = ConfigForm.default_cell_id_col
        self.fields["cell_label_column"].initial = ConfigForm.default_cell_label_col
        self.fields["embedding_x"].initial = ConfigForm.default_embedding_x_col
        self.fields["embedding_y"].initial = ConfigForm.default_embedding_y_col
        self.fields["molecule_id"].initial = ConfigForm.default_molecule_id
        self.fields[
                "molecule_label"].initial = ConfigForm.default_molecule_label
        self.fields["molecule_x"].initial = ConfigForm.default_molecule_x_col
        self.fields["molecule_y"].initial = ConfigForm.default_molecule_y_col

    def make_config_file_name(self):
        """ Creates the default config file name with a timestamp:
        VitessceConfig-yyyy.mm.dd_hhmmss.json
        """
        ts = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")
        filename = "VitessceConfig-" + ts + ".json"
        return filename

    def prepare_choices(self, file_names, file_urls, img_names, img_urls):
        """ Makes the lists of images and attached files for the form
        """
        self.text_choices = [i for i in zip(file_urls, file_names)]
        self.image_choices = [i for i in zip(img_urls, img_names)]

        self.text_choices.insert(0, ('', '---'))
        self.image_choices.insert(0, ('', '---'))

        return self.text_choices, self.image_choices
