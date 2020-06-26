const process = require('process')
const Navigation = require('./src/Navigation')

let wait = timeout => {
  return new Promise(resolve => {
    setTimeout(resolve, timeout)
  })
}

let confirm = (message = "Confirm?") => {
  return new Promise(resolve => {
    process.stdin.setEncoding('utf-8')
    console.log(message)
    process.stdin.on('data', () => {
      resolve()
    })
  })
}

let pwmInterface = new (require('./src/PWMInterface'))()
let navigation = new Navigation(pwmInterface)

let app = async () => {
  await pwmInterface.init()

  navigation.northTranslation(1)

  //await wait(1000)
  await confirm()
  //navigation.setSpeedFromAngle(45/2, 50)

  navigation.goTo(400, 400, 30, 50).then(() => {
    console.log('> Received the confirmation of a finished goto')
    navigation.stop()
  })

  /*
  navigation.northTranslation(40)

  await confirm()
  navigation.stop()
  */
}

process.on('SIGINT', async () => {
  console.log("> EXIT: Caught interrupt signal")
  navigation.stop()
  pwmInterface.stop()
  setTimeout(() => {
    console.log('STOP')
    process.exit()
  }, 1000)
})

app()
