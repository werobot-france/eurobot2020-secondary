let pwmInterface = new (require('../src/PWMInterface'))()

let main = async () => {
    await pwmInterface.init()
    pwmInterface.setEsc(12, 0)
    pwmInterface.setEsc(13, 0)
}

main()
