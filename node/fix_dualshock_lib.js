const fs = require('fs')

let path = "./node_modules/dualshock/mapping/ds4.js"
let content = fs.readFileSync(path).toString()


content = content.replace('dev.write(msg, true);', 'dev.write(msg);')

fs.writeFileSync(path, content)

console.log('Fixed!')