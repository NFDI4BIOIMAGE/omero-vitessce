import datetime

from django import forms


class ConfigForm(forms.Form):
    """ Form used to collect the parameters used to
        automatically generate a config file for Vitessce
    """

    # Set default values for CharField fields
    default_cell_id_col = "cell_id"
    default_cell_label_col = "label"
    default_embedding_x_col = "UMAP_1"
    default_embedding_y_col = "UMAP_2"
    default_molecule_id = "id"
    default_molecule_label = "gene"
    default_molecule_x_col = "x"
    default_molecule_y_col = "y"

    # Set help_text values for all fields

    config_file_name_help = "Name of the config file to use, \
            a '.json' extension is added if missing."
    image_help = "OMERO Image to view."
    segmentation_help = "Label image to overlay on the image, \
            pixel values correspond to cell identities."
    cell_identities_help = ".csv file with at least 2 columns: \
            Cell id column and Label column defined in the 2 fields below."
    cell_id_help = "Name of the Cell id column used in \
            'Cell identities', 'Expression', 'Embeddings'."
    cell_label_help = "Name of the Label used in Cell identities, \
            uesed e.g. to distinguish different cell types."
    expression_help = ".csv file with the Cell id column all other columns \
            are considered as expression values and should be numerical."
    embeddings_help = ".csv file with the Cell id column, \
            the Embedding x and Embedding y \
            columns defined in the 2 fields below."
    embeddings_x_help = "Name of the Embedding x used in Embeddings."
    embeddings_y_help = "Name of the Embedding y used in Embeddings."
    molecules_help = ".csv file with at least 4 columns: Molecule id, \
            label, x, y (headers in the fields below)."
    molecule_id_help = "Name of the Molecule id column used in Molecules."
    molecule_label_help = "Name of the Molecule label \
            column used in Molecules."
    molecule_x_help = "Name of the Molecule x column used in Molecules."
    molecule_y_help = "Name of the Molecule y column used in Molecules."
    histograms_help = "Add 3 plots showing: The number of transcripts per \
            cell, the number of cells in each set, \
            gene expression in each set."
    heatmap_help = "Adds an heatmap."
    status_help = "Adds a status panel to display info on the selected cell."
    description_help = "Adds a description panel to display info on the \
            dataset/image (taken from the description field)."

    def __init__(self, file_names, file_urls,
                 img_names, img_urls, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)

        self.text_choices, self.image_choices = self.prepare_choices(
                file_names, file_urls, img_names, img_urls)

        filename = self.make_config_file_name()

        self.fields["config_file_name"] = forms.CharField(
                empty_value=filename, strip=True,
                min_length=1, max_length=40, required=False,
                help_text=ConfigForm.config_file_name_help)

        # No empty default, we alway want an image in the config
        self.fields["image"] = forms.ChoiceField(
                choices=self.image_choices[1:], required=True,
                help_text=ConfigForm.image_help)

        # Cell data
        self.fields["segmentation"] = forms.ChoiceField(
                choices=self.image_choices, required=False,
                help_text=ConfigForm.segmentation_help)

        self.fields["cell_identities"] = forms.ChoiceField(
                choices=self.text_choices, required=False,
                help_text=ConfigForm.cell_identities_help)

        self.fields["cell_id_column"] = forms.CharField(
                empty_value=ConfigForm.default_cell_id_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.cell_id_help)

        self.fields["cell_label_column"] = forms.CharField(
                empty_value=ConfigForm.default_cell_label_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.cell_label_help)

        self.fields["expression"] = forms.ChoiceField(
                choices=self.text_choices, required=False,
                help_text=ConfigForm.expression_help)

        self.fields["embeddings"] = forms.ChoiceField(
                choices=self.text_choices, required=False,
                help_text=ConfigForm.embeddings_help)

        self.fields["embedding_x"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_x_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.embeddings_x_help)

        self.fields["embedding_y"] = forms.CharField(
                empty_value=ConfigForm.default_embedding_y_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.embeddings_y_help)

        # Molecule data
        self.fields["molecules"] = forms.ChoiceField(
                choices=self.text_choices, required=False,
                help_text=ConfigForm.molecules_help)

        self.fields["molecule_id"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_id, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.molecule_id_help)

        self.fields["molecule_label"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_label, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.molecule_label_help)

        self.fields["molecule_x"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_x_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.molecule_x_help)

        self.fields["molecule_y"] = forms.CharField(
                empty_value=ConfigForm.default_molecule_y_col, strip=True,
                min_length=1, max_length=20, required=False,
                help_text=ConfigForm.molecule_y_help)

        # Additional views
        self.fields["histograms"] = \
            forms.BooleanField(initial=True, required=False,
                               help_text=ConfigForm.histograms_help)
        self.fields["heatmap"] = \
            forms.BooleanField(initial=True, required=False,
                               help_text=ConfigForm.heatmap_help)
        self.fields["status"] = \
            forms.BooleanField(initial=False, required=False,
                               help_text=ConfigForm.status_help)
        self.fields["description"] = \
            forms.BooleanField(initial=False, required=False,
                               help_text=ConfigForm.description_help)

        # Set default values for CharField fields
        self.fields["config_file_name"].initial = filename
        self.fields["cell_id_column"].initial = ConfigForm.default_cell_id_col
        self.fields["cell_label_column"].initial = \
            ConfigForm.default_cell_label_col
        self.fields["embedding_x"].initial = ConfigForm.default_embedding_x_col
        self.fields["embedding_y"].initial = ConfigForm.default_embedding_y_col
        self.fields["molecule_id"].initial = ConfigForm.default_molecule_id
        self.fields["molecule_label"].initial = \
            ConfigForm.default_molecule_label
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
