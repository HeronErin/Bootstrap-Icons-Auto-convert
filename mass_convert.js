const fs = require('fs');
const convert = require("./offline_converter.js")

process.stdin.resume();
process.stdin.setEncoding('utf8');

let inputData = '';

process.stdin.on('data', function (data) {
  inputData += data;
});
function fserr(err){
	if (err)
		console.error(err);
}
process.stdin.on('end', function () {
	let json = JSON.parse(inputData);
	for (let svg_output of json){
		let result = convert(svg_output[0]);
		if (result.error){
			console.error(result.error);
			continue;
		}
		if (result.warnings){
			fs.writeFile(svg_output[1]+".warnings.md", result.warnings, 'utf8', fserr);
		}
		fs.writeFile(svg_output[1], result.code, 'utf8', fserr);
		fs.writeFile(svg_output[2], svg_output[0], 'utf8', fserr);
	}
});