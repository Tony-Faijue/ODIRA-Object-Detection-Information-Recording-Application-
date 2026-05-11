const { writeFile} = require('fs');

//Directory to write the environment.ts file
const targetPath = `./src/environments/environment.ts`;
//Use the env variable in production otherwise the default
const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:9998';
//Data config to be written in the environment.ts file
const envConfigFile = `
export const environment = {
    production: ${!!process.env.BACKEND_URL},
    ProcessImageURL: '${backendUrl}'
};`;

writeFile(targetPath, envConfigFile, function(err){
    if(err) { console.log(err); }
    console.log(`Successfully generated ${targetPath} with URL: ${backendUrl}`);
});