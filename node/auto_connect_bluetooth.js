var pty = require('node-pty');
 
var ptyProcess = pty.spawn("bluetoothctl", [], {
  name: 'xterm-color',
  cols: 80,
  rows: 30,
  cwd: process.env.HOME,
  env: process.env
});
 
ptyProcess.on('data', function(data) {
  process.stdout.write(data);
});
 
ptyProcess.write('devices\n');

ptyProcess.write('connect DC:0C:2D:5F:09:F8\n');

