module.exports = class ScreenInterface {
  constructor(params) {
    this.arduinoInterface = params.arduinoInterface
  }

  clear() {
    this.arduinoInterface.sendCommand('LCD_CLEAR')
  }

  setBacklight(intensity) {
    this.arduinoInterface.sendCommand('LCD_BACKLIGHT', [intensity])
  }

  init() {
    this.clear()
    this.setBacklight(255)
  }

  printFirst(text) {
    this.arduinoInterface.sendCommand('LCD_FIRST', [0, 0, 0, text])
  }

  printSecond(text) {
    this.arduinoInterface.sendCommand('LCD_SECOND', [0, 0, 0, text])
  }

  print(textComponents) {
    this.printFirst(textComponents[0])
    this.printSecond(textComponents[1])
  }
}