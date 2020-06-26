const fs = require('fs')

setInterval(() => {
  console.log(fs.readFileSync('/sys/class/gpio/gpio16/value').toString().charAt(0) === 1)
}, 10)

