const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB1', {baudRate: 9600})
const StringDecoder = new (require('string_decoder').StringDecoder)('utf8');

port.on('error', function(err) {
  console.log('Error: ', err.message)
})

port.on('data', (data) => {
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


