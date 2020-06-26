module.exports.wait = timeout => {
  return new Promise(resolve => {
    setTimeout(resolve, timeout)
  })
}

module.exports.confirm = () => new Promise(resolve => {
  process.stdin.setEncoding('utf-8')
  console.log('Confirm ?')
  process.stdin.on('data', resolve)
})