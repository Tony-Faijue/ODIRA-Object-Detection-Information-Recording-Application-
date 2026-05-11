const { writeFile, existsSync, mkdirSync} = require('fs');

//Target directory and file path to write the environment.ts file
const dirPath = './src/envrionments';
const targetPath = `${dirPath}/environment.ts`;

if(!existsSync(dirPath)){
    mkdirSync(dirPath, {recursive: true});
    console.log(`Creadted directory: ${dirPath}`);
}

//Use the env variable in production otherwise the default
const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:9998';
//Data config to be written in the environment.ts file
const envConfigFile = `
export const environment = {
    production: ${!!process.env.BACKEND_URL},
    ProcessImageURL: '${backendUrl}'
};`;

writeFile(targetPath, envConfigFile, function(err){
    if(err) { 
        console.error('Error writing file:', err); 
        process.exit(1);
    }
    console.log(`Successfully generated ${targetPath} with URL: ${backendUrl}`);
});