const process = require('process') 
const pty = require('node-pty')
const address = "DC:0C:2D:5F:09:F8"
const ptyProcess = pty.spawn("bluetoothctl", [], {
  name: 'xterm-color',
  cols: 80,
  rows: 30,
  cwd: process.env.HOME,
  env: process.env
})
ptyProcess.on('data', function(data) {
  process.stdout.write(data)
  if (data.indexOf('Connection successful') !== -1) {
    console.log()
    console.log('Connection is considered as successful')
    ptyProcess.kill()
    process.exit()
  }
})
ptyProcess.write('devices\n')
ptyProcess.write('connect ' + address + '\n')


