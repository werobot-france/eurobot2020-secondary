const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB0', {baudRate: 115200})
const StringDecoder = new (require('string_decoder').StringDecoder)('utf8');

function parseResponse(data) {
        let decodedData = StringDecoder.write(data)
        let responseType = decodedData.split(': ')[0]
        return decodedData
        let payload = decodedData.split(': ')[1].replace('\r\n', '')
        return {
            responseType,
            payload
        }
}

setTimeout(() => {
port.write('PING\n', (err) => {
  if (err) {
    return console.log('Error on write: ', err.message)
  }
  console.log('message written')
})
}, 2000)


// Open errors will be emitted as an error event
port.on('error', function(err) {
  console.log('Error: ', err.message)
})

port.on('data', (data) => {
   console.log(parseResponse(data))
})
