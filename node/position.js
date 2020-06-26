const child_process = require('child_process')

let watcher = child_process.spawn("python3", ["PositionWatcher.py", "-T"])

watcher.stdout.on('data', d => {
  let content = d.toString()

  if (content.indexOf("ack") !== "a") {
    console.log("Posititon watcher python has loaded the target positions")
  }

  console.log(content)

  if (content.indexOf("done") !== -1) {
    console.log("Done!")
  }

})

targetX = 0
targetY = 100
threadhold = 20
watcher.stdin.write(targetX.toString() + ";" + targetY.toString() + ";" + threadhold.toString() + "\n")
