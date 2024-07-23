
#copy over html,css,js and templates
echo "Deploying built resources..."
mkdir -p ../omero_vitessce/templates/omero_vitessce/
mkdir -p ../omero_vitessce/static/

# Cleanup
rm ../omero_vitessce/templates/omero_vitessce/index.html
rm -r ../omero_vitessce/static/*

#
cp build/index.html ../omero_vitessce/templates/omero_vitessce/
cp -r build/static/* ../omero_vitessce/static/
