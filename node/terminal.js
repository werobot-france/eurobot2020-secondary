const SerialPort = require('serialport')
const process = require('process')

if (process.argv[2] === undefined) {
    console.log('ERR: You must provide a device path (ex: /dev/ttyUSB0) as an argument!')
    process.exit()
}

let path = process.argv[2]

const port = new SerialPort(path, {baudRate: 9600})

port.on('error', function(err) {
  console.log('Error: ', err.message)
})

port.on('data', (data) => {
   /*if (data.toString().indexOf('Pos') > -1) {
      return;
   }*/	
   process.stdout.write(data)
})

function prompt(question, callback) {
    var stdin = process.stdin,
        stdout = process.stdout;

    stdin.resume();
    stdout.write(question);

    stdin.once('data', function (data) {
        callback(data.toString().trim());
    });
}

main = () => {
prompt('', data => {
   port.write(data+"\n")
   main() 
})
}

main()