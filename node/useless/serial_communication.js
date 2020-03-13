const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB0', {baudRate: 9600})
const StringDecoder = new (require('string_decoder').StringDecoder)('utf8');


setTimeout(() => {
  port.write('PING\n', (err) => {
    if (err) {
      return console.log('Error on write: ', err.message)
    }
    console.log('message written')
    port.removeAllListeners('data')
    port.on('data', (data) => {
      console.log(data.toString())
    })
  })
}, 2000)


// Open errors will be emitted as an error event
port.on('error', function(err) {
  console.log('Error: ', err.message)
})

