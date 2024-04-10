

// Construct the API projects URL
var projectsUrl = PARAMS.API_BASE_URL + 'm/projects/';

// Filter projects by Owner to only show 'your' projects
projectsUrl += '?owner=' + PARAMS.EXP_ID;

fetch(projectsUrl).then(rsp => rsp.json())
    .then(data => {
        let projectCount = data.meta.totalCount;
        let projects = data.data;

        // Render html...
        let html = `
            <div>Total: ${projectCount} projects...</div>
            <ul>
                ${projects.map(p => `<li>${p.Name} (ID: ${p['@id']})</li>`).join("")}
            </ul>`;

        document.getElementById('projects').innerHTML = html;
    });
