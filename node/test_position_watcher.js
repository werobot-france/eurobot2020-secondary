
const watcher = new (require('./src/PositionWatcher'))()

watcher.on('positionUpdated', (x, y, theta) => {
  console.log(x, y, theta)
})
watcher.init()