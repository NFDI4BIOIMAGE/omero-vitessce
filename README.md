OMERO.omero_vitessce
=======================

OMERO Vitessce multimodal data viewer.

Installation
============

Install `omero_vitessce` in mode as follows:

    # within your python venv:
    cd omero-vitessce
    pip install -e .

Add the app to the `omero.web.apps` setting:

    omero config append omero.web.apps '"omero_vitessce"'

Add `omero_vitessce` as a tab in the right-hand-side panel:

    omero config append omero.web.ui.right_plugins '["Vitessce", "omero_vitessce/webclient_plugins/right_plugin.vitessce.js.html", "vitessce_tab"]'

Add the omero web address (replace ´'"http://localhost:4080"'´ with your address):

    omero config set omero.web.omero_vitessce.serveraddress '"http://localhost:4080"'
    
Now restart OMERO.web as normal for the configuration above to take effect.

Usage
============
### Right-hand-side panel:
- Prexisting config files
- Autogenerating config file:

  
### Open-with:

COMING SOON!

Development
----------------

## Sources

- cookiecutter-omero-webapp: https://github.com/ome/cookiecutter-omero-webapp
- `react_webapp` from omero-web-apps-examples: https://github.com/ome/omero-web-apps-examples/tree/master/react-webapp
- Vitessce python package (will be used for generating config files) http://python-docs.vitessce.io/

## React web app

### omero_vitessce web app

We serve a custom version of the vitesce app: http://vitessce.io/

The app sets up a vitessce view configured through a text file in json format: http://vitessce.io/docs/view-config-json/

The configuration file is taken from the `?config` url parameter.

### Installation

This project was created with [Create React App](https://github.com/facebook/create-react-app).

You can run this project in development mode or as an OMERO.web Django app.

To get started:

    cd vitessce_app
    npm install

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.


### `npm run build`

Builds the app for production to the `build` folder and copies the
html and static files to the Django app in `vitessce app`. See the [deploy_build.sh]() script.<br>

You also need to install the app into your `omero-web` environment:

    # cd to the root of the repo
    pip install -e .

You will need to have the app configured in your OMERO.web install:

      omero config append omero.web.apps '"omero_vitessce"'
      omero config append omero.web.ui.right_plugins '["Vitessce", "omero_vitessce/webclient_plugins/right_plugin.vitessce.js.html", "vitessce_tab"]'
      omero config set omero.web.omero_vitessce.serveraddress '"http://localhost:4080"'

It bundles React in production mode and optimizes the build for the best performance.

See the Create React App section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

