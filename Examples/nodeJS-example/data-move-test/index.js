const fs = require("fs");

const data = require("./data.js");


console.log(data.names);
console.log(data.age);

fs.writeFile("./text.txt", data.names.toString(), () => {
    console.log("First name was written");
});

