// Render html...
let json_configs = PARAMS.JSON_CONFIGS
let html_text = `
            <div>.json configuration files:</div>
            <ul>
                ${json_configs.map(c => `<li>${c.Name}})</li>`).join("")}
            </ul>`;

document.getElementById('configs').innerHTML = html_text;
